#!/usr/bin/env python3
"""Command line runner for the weekly exercises.

    uv run runner.py list                        # status of every week and task
    uv run runner.py show 1 detect_cycle         # print a problem statement
    uv run runner.py test 1 --lang c             # grade
    uv run runner.py new --topic "이진 탐색 트리" --slug binary_search_tree

All grading goes through pytest. This script is only a thin wrapper around it, so
`uv run pytest exercises/week_01_linked_list -m cpp` does exactly the same thing.

User facing output stays in Korean because the course material is in Korean; the code
itself (identifiers, comments, docstrings) is in English.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXERCISES = ROOT / "exercises"
SUBMISSIONS = ROOT / "submissions"
TEMPLATES = ROOT / "templates"

WEEK_RE = re.compile(r"^week_(\d+)(?:_(\w+))?$")

LANGUAGES = ["c", "cpp", "python"]
LANG_LABEL = {"c": "C", "cpp": "C++", "python": "Python"}
LANG_SUFFIX = {"c": ".c", "cpp": ".cpp", "python": ".py"}
DIFFICULTIES = ["impl", "easy", "medium", "hard"]
DIFFICULTY_LABEL = {"impl": "구현", "easy": "쉬움", "medium": "중간", "hard": "어려움"}
DEFAULT_TASKS = "c/impl,cpp/easy,cpp/medium,python/easy,python/medium"

# Where new weeks come from. A fork keeps this value, which is what lets `sync` wire up
# the upstream remote for someone who only clicked "Fork" and never touched git remotes.
UPSTREAM_URL = "https://github.com/k1seul/datascience-programming.git"
UPSTREAM_BRANCH = "main"
# Files that belong to the grader, never to a submission.
SUBMIT_SKIP = {"tests.py", "__init__.py", "conftest.py"}
STATUS_ICON = {
    "pass": "✅",
    "fail": "❌",
    "crash": "💥",
    "pending": "⬜",
    "skipped": "⏭️",
    "empty": "—",
}
STATUS_LABEL = {
    "pass": "통과",
    "fail": "실패",
    "crash": "중단됨 (무한 루프 / 세그폴트?)",
    "pending": "미착수",
    "skipped": "건너뜀",
    "empty": "테스트 없음",
}

USE_COLOR = sys.stdout.isatty()
GREEN, RED, YELLOW, DIM, BOLD = "32", "31", "33", "2", "1"


def paint(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def display_width(text: str) -> int:
    """Width in terminal columns, counting wide characters (Hangul, CJK) as two."""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad(text: str, width: int) -> str:
    return text + " " * max(0, width - display_width(text))


@dataclass(frozen=True)
class Task:
    """One `<week>/<language>/<difficulty>_<name>/` directory."""

    path: Path

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def language(self) -> str:
        return self.path.parent.name

    @property
    def difficulty(self) -> str:
        return self.name.partition("_")[0]

    @property
    def slug(self) -> str:
        """Problem name with the difficulty prefix stripped."""
        return self.name.partition("_")[2] or self.name

    @property
    def ref(self) -> str:
        return f"{self.language}/{self.name}"

    @property
    def difficulty_label(self) -> str:
        return DIFFICULTY_LABEL.get(self.difficulty, self.difficulty)

    @property
    def sources(self) -> list[Path]:
        suffix = LANG_SUFFIX.get(self.language, "")
        return [p for p in sorted(self.path.glob(f"*{suffix}")) if p.name != "tests.py"]

    def looks_unwritten(self) -> bool:
        """Cheap guess used by `list --fast`, which does not run the tests.

        The real verdict comes from grading: see read_junit. This only reads the source
        for the stub markers, so it cannot tell a half-finished task from an untouched one.
        """
        markers = ("NotImplementedError", "NOT_IMPLEMENTED")
        return any(
            any(marker in src.read_text(encoding="utf-8") for marker in markers)
            for src in self.sources
        )

    def matches(self, token: str) -> bool:
        token = token.strip("/")
        return token in {self.name, self.slug, self.ref, f"{self.language}/{self.slug}"}


def _task_order(task: Task) -> tuple[int, str]:
    known = task.difficulty in DIFFICULTIES
    rank = DIFFICULTIES.index(task.difficulty) if known else len(DIFFICULTIES)
    return rank, task.name


@dataclass(frozen=True)
class Week:
    path: Path

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def number(self) -> int:
        return int(WEEK_RE.match(self.name).group(1))

    @property
    def slug(self) -> str:
        return WEEK_RE.match(self.name).group(2) or ""

    @property
    def topic(self) -> str:
        """Read the topic from the part after the dash in the week README title."""
        readme = self.path / "README.md"
        if not readme.exists():
            return self.slug.replace("_", " ")
        for line in readme.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].split("—", 1)[-1].strip()
        return self.slug.replace("_", " ")

    def tasks(self, language: str | None = None) -> list[Task]:
        found: list[Task] = []
        for lang in LANGUAGES if language is None else [language]:
            lang_dir = self.path / lang
            if not lang_dir.is_dir():
                continue
            tasks = [Task(p) for p in lang_dir.iterdir() if (p / "tests.py").exists()]
            found += sorted(tasks, key=_task_order)
        return found


def weeks() -> list[Week]:
    if not EXERCISES.exists():
        return []
    found = [Week(p) for p in EXERCISES.iterdir() if p.is_dir() and WEEK_RE.match(p.name)]
    return sorted(found, key=lambda w: w.number)


def resolve_week(token: str) -> Week:
    """Accept '1', '01', 'week_01', 'week_01_linked_list' and 'linked_list' alike."""
    token = token.strip().strip("/")
    found = weeks()
    for week in found:
        if token in {week.name, week.slug, str(week.number), f"{week.number:02d}"}:
            return week
        if token.isdigit() and int(token) == week.number:
            return week
    known = ", ".join(w.name for w in found) or "(없음)"
    raise SystemExit(f"'{token}' 주차를 찾을 수 없습니다. 있는 주차: {known}")


def resolve_task(week: Week, token: str) -> Task:
    matched = [t for t in week.tasks() if t.matches(token)]
    if len(matched) == 1:
        return matched[0]
    known = ", ".join(t.ref for t in week.tasks())
    if not matched:
        raise SystemExit(f"'{token}' 과제를 찾을 수 없습니다. 있는 과제: {known}")
    raise SystemExit(f"'{token}' 이 여러 과제와 겹칩니다: {', '.join(t.ref for t in matched)}")


# pytest-timeout fires first per test; this is the backstop for when even that hangs.
GRADE_TIMEOUT = 300


def run_pytest(
    targets: list[Path], extra: list[str], quiet: bool = False
) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "pytest", *[str(t) for t in targets], *extra]
    if not quiet:
        return subprocess.run(cmd, cwd=ROOT)
    try:
        return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=GRADE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, returncode=124, stdout="", stderr="timeout")


# A stub signals "not written yet" by raising this; the marker is the behaviour itself,
# so it cannot survive a real implementation the way a leftover comment could.
NOT_IMPLEMENTED_MARK = "NotImplementedError"


def read_junit(report: Path) -> tuple[dict[str, int], bool]:
    """Return (counts, every failure is a NotImplementedError).

    The second value is what separates "not started" from "started and broken": a task
    whose only failures are NotImplementedError has simply not been written yet, while a
    single assertion failure among them means someone worked on it and broke something.
    """
    empty = dict.fromkeys(["tests", "failures", "errors", "skipped"], 0)
    if not report.exists():
        return empty, False
    root = ET.parse(report).getroot()
    suite = root.find("testsuite") if root.tag == "testsuites" else root
    if suite is None:
        return empty, False

    counts = {key: int(suite.get(key, 0)) for key in empty}
    problems = [
        node for case in suite.iter("testcase") for node in case if node.tag in ("failure", "error")
    ]
    only_stubs = bool(problems) and all(
        NOT_IMPLEMENTED_MARK in (node.get("message", "") + (node.text or "")) for node in problems
    )
    return counts, only_stubs


@dataclass(frozen=True)
class Result:
    """Grading result for a single task."""

    tests: int
    failures: int
    errors: int
    skipped: int
    returncode: int
    not_implemented: bool

    @property
    def bad(self) -> int:
        return self.failures + self.errors

    @property
    def passed(self) -> int:
        return self.tests - self.bad - self.skipped

    @property
    def status(self) -> str:
        """One of crash / empty / skipped / pass / pending / fail."""
        if self.returncode == 5:
            return "empty"
        # On a timeout (infinite loop) or a segfault pytest dies before writing a report.
        if self.returncode not in (0, 1) or (self.tests == 0 and self.returncode != 0):
            return "crash"
        if self.tests == 0:
            return "empty"
        if self.bad == 0:
            return "skipped" if self.skipped and self.passed == 0 else "pass"
        return "pending" if self.not_implemented else "fail"


def grade(task: Task) -> Result:
    """Grade a single task quietly.

    Reads exact counts from a junit-xml report instead of parsing pytest's summary line.
    """
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.xml"
        proc = run_pytest(
            [task.path],
            ["-q", "--tb=no", "-p", "no:cacheprovider", "--junit-xml", str(report)],
            quiet=True,
        )
        counts, only_stubs = read_junit(report)
    return Result(**counts, returncode=proc.returncode, not_implemented=only_stubs)


def format_result(result: Result) -> str:
    if result.status == "crash":
        return paint(STATUS_LABEL["crash"], RED)
    if result.status == "empty":
        return paint("테스트 없음", DIM)
    if result.status == "skipped":
        return paint("건너뜀", YELLOW)
    if result.status == "pass":
        return paint(f"통과 {result.passed}/{result.tests}", GREEN)
    if result.status == "pending":
        return paint(f"미착수 {result.passed}/{result.tests}", YELLOW)
    return paint(f"실패 {result.bad}개 (통과 {result.passed}/{result.tests})", RED)


def cmd_list(args: argparse.Namespace) -> int:
    found = weeks()
    if not found:
        print('아직 주차가 없습니다. `uv run runner.py new --topic "..."` 로 시작하세요.')
        return 0

    for week in found:
        print(paint(f"{week.name} — {week.topic}", BOLD))
        tasks = week.tasks()
        if not tasks:
            print(f"  (읽기 주차 — uv run runner.py show {week.number} 로 자료 목록)")
            continue
        for language in LANGUAGES:
            in_language = [t for t in tasks if t.language == language]
            if not in_language:
                continue
            print(f"  {paint(LANG_LABEL[language], DIM)}")
            for task in in_language:
                if args.fast:
                    unwritten = task.looks_unwritten()
                    status = paint("미착수", YELLOW) if unwritten else paint("작성됨", DIM)
                else:
                    status = format_result(grade(task))
                print(f"    {pad(task.name, 30)} {pad(task.difficulty_label, 6)} {status}")
        print()
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    week = resolve_week(args.week)
    if args.task:
        path = resolve_task(week, args.task).path / "problem.md"
    else:
        path = week.path / "README.md"
    if not path.exists():
        raise SystemExit(f"{path.relative_to(ROOT)} 가 없습니다")
    print(path.read_text(encoding="utf-8"))
    return 0


def cmd_test(args: argparse.Namespace) -> int:
    if args.week:
        week = resolve_week(args.week)
        targets = [resolve_task(week, args.task).path] if args.task else [week.path]
    elif args.task:
        raise SystemExit("--task 를 쓰려면 주차도 함께 지정하세요 (예: test 1 --task detect_cycle)")
    else:
        targets = [EXERCISES]

    extra: list[str] = []
    if args.lang:
        extra += ["-m", args.lang]
    if args.k:
        extra += ["-k", args.k]
    if args.verbose:
        extra.append("-v")
    extra += args.pytest_args

    proc = run_pytest(targets, extra)
    return 0 if proc.returncode in (0, 5) else proc.returncode


def cmd_ci(args: argparse.Namespace) -> int:
    """Grade for CI, failing only when a task someone worked on is broken.

    A task still carrying a TODO is not a failure: a CI that is always red because of
    unsolved exercises carries no signal.
    """
    targets = [resolve_week(args.week)] if args.week else weeks()
    if not targets:
        print("채점할 주차가 없습니다.")
        return 0

    rows: list[tuple[Week, Task, Result]] = []
    for week in targets:
        for task in week.tasks():
            rows.append((week, task, grade(task)))

    for week, task, result in rows:
        icon = STATUS_ICON[result.status]
        counts = f"{result.passed}/{result.tests}" if result.tests else "-"
        print(f"{icon} {week.name} · {task.ref:<40} {STATUS_LABEL[result.status]} {counts}")

    tally = {status: 0 for status in STATUS_ICON}
    for _, _, result in rows:
        tally[result.status] += 1
    broken = tally["fail"] + tally["crash"]
    print(
        f"\n통과 {tally['pass']} · 실패 {broken} · 미착수 {tally['pending']}"
        f" · 건너뜀 {tally['skipped']} (과제 {len(rows)}개)"
    )

    write_github_summary(rows, tally)
    return 1 if broken else 0


def write_github_summary(rows: list[tuple[Week, Task, Result]], tally: dict[str, int]) -> None:
    """Append a table to the GitHub Actions run summary (a no-op outside CI)."""
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if not target:
        return
    lines = [
        "## 채점 결과",
        "",
        f"통과 **{tally['pass']}** · 실패 **{tally['fail'] + tally['crash']}**"
        f" · 미착수 **{tally['pending']}**",
        "",
        "| | 주차 | 과제 | 언어 | 난이도 | 결과 |",
        "|---|---|---|---|---|---|",
    ]
    for week, task, result in rows:
        counts = f"{result.passed}/{result.tests}" if result.tests else "-"
        lines.append(
            f"| {STATUS_ICON[result.status]} | {week.name} | `{task.name}` "
            f"| {LANG_LABEL.get(task.language, task.language)} | {task.difficulty_label} "
            f"| {STATUS_LABEL[result.status]} {counts} |"
        )
    lines += ["", "⬜ 는 아직 구현하지 않은 과제라 실패로 치지 않습니다."]
    with open(target, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def cmd_submit(args: argparse.Namespace) -> int:
    """Build the submission zip: the submitted code only, without the grading tests."""
    week = resolve_week(args.week)
    tasks = [resolve_task(week, args.task)] if args.task else week.tasks()
    if not tasks:
        raise SystemExit(f"{week.name} 에 과제가 없습니다")

    if not args.no_check:
        print("채점 중...")
        for task in tasks:
            print(f"  {pad(task.ref, 42)} {format_result(grade(task))}")
        print()

    pending = [t for t in tasks if t.looks_unwritten()]
    if pending:
        print(paint(f"주의: 아직 구현하지 않은 과제 {len(pending)}개가 들어갑니다", YELLOW))
        for task in pending:
            print(f"  - {task.ref}")
        print()

    stem = week.name if not args.name else f"{week.name}_{args.name}"
    SUBMISSIONS.mkdir(exist_ok=True)
    archive = SUBMISSIONS / f"{stem}.zip"

    packed: list[str] = []
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for task in tasks:
            for path in sorted(task.path.rglob("*")):
                if path.is_dir() or "__pycache__" in path.parts:
                    continue
                if path.name in SUBMIT_SKIP:
                    continue
                if path.suffix == ".md" and not args.with_problem:
                    continue
                arcname = Path(stem) / path.relative_to(week.path)
                zf.write(path, arcname)
                packed.append(str(arcname))

    print(f"{archive.relative_to(ROOT)} ({archive.stat().st_size:,} B)")
    for name in packed:
        print(f"  {name}")
    return 0


def render(template: Path, mapping: dict[str, str]) -> str:
    text = template.read_text(encoding="utf-8")
    for key, value in mapping.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def slugify(text: str) -> str:
    slug = re.sub(r"\W+", "_", text.strip(), flags=re.ASCII).strip("_").lower()
    return slug


def parse_task_spec(spec: str) -> tuple[str, str]:
    """Turn 'cpp/medium_validate_bst' or 'cpp/medium' into (language, directory name)."""
    language, _, name = spec.strip().strip("/").partition("/")
    if language not in LANGUAGES:
        raise SystemExit(f"언어는 {', '.join(LANGUAGES)} 중 하나여야 합니다: {spec}")
    if not name:
        raise SystemExit(f"'<언어>/<난이도>[_문제이름]' 형식으로 적어 주세요: {spec}")
    if name.partition("_")[0] not in DIFFICULTIES:
        raise SystemExit(f"난이도는 {', '.join(DIFFICULTIES)} 중 하나여야 합니다: {spec}")
    return language, name


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    )
    if check and proc.returncode != 0:
        message = (proc.stderr or proc.stdout).strip()
        raise SystemExit(f"git {' '.join(args)} 가 실패했습니다:\n{message}")
    return proc


def canonical(url: str) -> str:
    """Normalise a remote URL so ssh and https forms of the same repo compare equal."""
    url = url.strip().removesuffix(".git")
    url = re.sub(r"^git@([^:]+):", r"https://\1/", url)
    return url.removeprefix("https://").removeprefix("http://").lower()


def upstream_remote() -> str:
    """Return the remote that new weeks come from, adding it when it is missing.

    Someone who cloned the course repository already has it as `origin`. Someone who
    forked has their own copy as `origin`, so a separate `upstream` remote is needed;
    forgetting that is the usual reason new weeks never show up.
    """
    remotes = {
        parts[0]: parts[1]
        for line in git("remote", "-v").stdout.splitlines()
        if "(fetch)" in line and (parts := line.split())
    }
    if "upstream" in remotes:
        return "upstream"
    if "origin" in remotes and canonical(remotes["origin"]) == canonical(UPSTREAM_URL):
        return "origin"
    git("remote", "add", "upstream", UPSTREAM_URL)
    print(f"upstream 리모트를 추가했습니다: {UPSTREAM_URL}\n")
    return "upstream"


def week_names() -> set[str]:
    return {week.name for week in weeks()}


def cmd_sync(args: argparse.Namespace) -> int:
    """Bring in newly published weeks without disturbing the answers already written."""
    if not (ROOT / ".git").exists():
        raise SystemExit("git 저장소가 아닙니다. clone 이나 fork 한 폴더에서 실행해 주세요.")

    dirty = git("status", "--porcelain").stdout.strip()
    if dirty and not args.check:
        print(paint("아직 커밋하지 않은 변경이 있습니다:", YELLOW))
        for line in dirty.splitlines()[:10]:
            print(f"  {line}")
        print("\n먼저 커밋하거나 잠시 치워 두고 다시 실행해 주세요.")
        print('  git add -A && git commit -m "작업 중"')
        print("  또는  git stash")
        return 1

    remote = upstream_remote()
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    print(f"{remote}/{UPSTREAM_BRANCH} 를 가져와서 현재 브랜치({branch})에 합칩니다.")
    git("fetch", remote, UPSTREAM_BRANCH)

    incoming = git("log", "--oneline", f"HEAD..{remote}/{UPSTREAM_BRANCH}").stdout.strip()
    if not incoming:
        print(paint("이미 최신입니다.", GREEN))
        return 0

    lines = incoming.splitlines()
    print(f"\n새로 올라온 커밋 {len(lines)}개:")
    for line in lines[:10]:
        print(f"  {line}")
    if len(lines) > 10:
        print(f"  ... 외 {len(lines) - 10}개")

    if args.check:
        print("\n(--check 라서 받아오지는 않았습니다. 그냥 `sync` 로 실행하면 반영됩니다.)")
        return 0

    before = week_names()
    merge = git("merge", f"{remote}/{UPSTREAM_BRANCH}", "-m", "새로 올라온 주차 반영", check=False)
    if merge.returncode != 0:
        conflicts = git("diff", "--name-only", "--diff-filter=U").stdout.split()
        print()
        print(paint("충돌이 났습니다. 아래 파일을 정리해야 합니다:", RED))
        for path in conflicts:
            print(f"  {path}")
        print("\n내가 쓴 답을 그대로 두려면:")
        for path in conflicts:
            print(f"  git checkout --ours {path}")
        print("  git add -A && git commit")
        print("\n되돌리려면:  git merge --abort")
        return 1

    added = sorted(week_names() - before)
    print()
    print(paint("반영했습니다.", GREEN))
    if added:
        print("\n새 주차:")
        for name in added:
            print(f"  {name}")
        first = sorted(added)[0]
        number = WEEK_RE.match(first).group(1).lstrip("0") or "0"
        print(f"\n  uv run runner.py show {number} 로 문제를 볼 수 있습니다.")
    print("\n  uv run runner.py list 로 현황을 확인해 보세요.")
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    existing = weeks()
    number = args.week or (existing[-1].number + 1 if existing else 1)
    slug = args.slug or slugify(args.topic)
    if not slug:
        raise SystemExit(
            "토픽이 한글이면 폴더 이름으로 쓸 --slug 를 함께 주세요 (예: --slug binary_search_tree)"
        )

    week_dir = EXERCISES / f"week_{number:02d}_{slug}"
    if week_dir.exists():
        raise SystemExit(f"{week_dir.relative_to(ROOT)} 가 이미 있습니다")

    specs = [parse_task_spec(s) for s in args.tasks.split(",") if s.strip()]
    base = {"week": f"{number:02d}", "week_num": str(number), "topic": args.topic, "slug": slug}

    week_dir.mkdir(parents=True)
    (week_dir / "__init__.py").write_text("", encoding="utf-8")
    rows = "\n".join(
        f"| [`{lang}/{name}`]({lang}/{name}/problem.md) | {LANG_LABEL[lang]} "
        f"| {DIFFICULTY_LABEL.get(name.partition('_')[0], '')} | (제목) |"
        for lang, name in specs
    )
    (week_dir / "README.md").write_text(
        render(TEMPLATES / "week_README.md.tmpl", {**base, "rows": rows}), encoding="utf-8"
    )

    for language, name in specs:
        lang_dir = week_dir / language
        lang_dir.mkdir(exist_ok=True)
        (lang_dir / "__init__.py").write_text("", encoding="utf-8")
        task_dir = lang_dir / name
        task_dir.mkdir()
        (task_dir / "__init__.py").write_text("", encoding="utf-8")
        difficulty = name.partition("_")[0]
        mapping = {
            **base,
            "task": f"{language}/{name}",
            "lang": language,
            "lang_label": LANG_LABEL[language],
            "difficulty": difficulty,
            "difficulty_label": DIFFICULTY_LABEL.get(difficulty, difficulty),
        }
        for template in sorted((TEMPLATES / f"task_{language}").glob("*.tmpl")):
            target = task_dir / template.name.removesuffix(".tmpl")
            target.write_text(render(template, mapping), encoding="utf-8")

    print(f"{week_dir.relative_to(ROOT)} 생성:")
    for path in sorted(week_dir.rglob("*")):
        if path.is_file() and path.name != "__init__.py":
            print(f"  {path.relative_to(ROOT)}")
    print(f"\n문제를 채운 뒤: uv run runner.py test {number}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="runner.py",
        description="주간 코딩 연습 — 현황 확인, 채점, 새 주차 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="주차/과제 현황")
    p_list.add_argument("--fast", action="store_true", help="테스트를 돌리지 않고 착수 여부만 표시")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="문제 설명 출력")
    p_show.add_argument("week", help="주차 (1, week_01, linked_list)")
    p_show.add_argument("task", nargs="?", help="과제 (detect_cycle, python/medium_detect_cycle)")
    p_show.set_defaults(func=cmd_show)

    p_test = sub.add_parser("test", help="채점")
    p_test.add_argument("week", nargs="?", help="주차 (생략하면 전체)")
    p_test.add_argument("--lang", choices=LANGUAGES, help="언어로 거르기")
    p_test.add_argument("--task", help="과제 하나만 (예: detect_cycle)")
    p_test.add_argument("-k", help="pytest -k 표현식")
    p_test.add_argument("-v", "--verbose", action="store_true")
    p_test.add_argument("pytest_args", nargs="*", help="pytest 로 그대로 넘길 인자")
    p_test.set_defaults(func=cmd_test)

    p_ci = sub.add_parser("ci", help="CI 채점 (미착수는 실패로 치지 않음)")
    p_ci.add_argument("week", nargs="?", help="주차 (생략하면 전체)")
    p_ci.set_defaults(func=cmd_ci)

    p_submit = sub.add_parser("submit", help="제출용 zip 만들기")
    p_submit.add_argument("week", help="주차 (1, week_01, linked_list)")
    p_submit.add_argument("--task", help="과제 하나만")
    p_submit.add_argument("--name", help="파일 이름 뒤에 붙일 이름/학번")
    p_submit.add_argument("--with-problem", action="store_true", help="problem.md 도 함께 넣기")
    p_submit.add_argument("--no-check", action="store_true", help="압축 전에 채점하지 않기")
    p_submit.set_defaults(func=cmd_submit)

    p_sync = sub.add_parser("sync", help="새로 올라온 주차 받아오기")
    p_sync.add_argument(
        "--check", action="store_true", help="받아오지 않고 무엇이 올라왔는지만 확인"
    )
    p_sync.set_defaults(func=cmd_sync)

    p_new = sub.add_parser("new", help="새 주차 뼈대 생성")
    p_new.add_argument("--topic", required=True, help="이번 주 토픽 (예: 이진 탐색 트리)")
    p_new.add_argument("--slug", help="폴더 이름에 쓸 영문 슬러그 (예: binary_search_tree)")
    p_new.add_argument("--week", type=int, help="주차 번호 (생략하면 마지막 + 1)")
    p_new.add_argument(
        "--tasks",
        default=DEFAULT_TASKS,
        help=f"쉼표로 구분한 '<언어>/<난이도>[_문제이름]' 목록 (기본: {DEFAULT_TASKS})",
    )
    p_new.set_defaults(func=cmd_new)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
