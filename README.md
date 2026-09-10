# Data Science Programming — Fall Coding Exercises

**Seoul National University** · 데이터사이언스를 위한 프로그래밍 실습

[![tests](https://github.com/k1seul/datascience-programming/actions/workflows/tests.yml/badge.svg)](https://github.com/k1seul/datascience-programming/actions/workflows/tests.yml)

매주 토픽 하나를 정하고, **C / C++ / Python** 세 언어로 문제를 푼다.
언어가 무엇이든 채점은 **전부 pytest** 로 돌아간다 — C 와 C++ 소스는 테스트가 직접
공유 라이브러리로 빌드해서 `ctypes` 로 호출한다.

```sh
uv sync                                 # 처음 한 번
uv run runner.py list                   # 현황
uv run runner.py show 1 detect_cycle    # 문제 설명
uv run runner.py test 1                 # 채점
```

## 폴더 구조

`주차_토픽 / 언어 / 난이도_문제이름` 으로 묶는다.

```
exercises/week_01_linked_list/
  README.md                            주차 개요 — 토픽과 과제 목록
  c/
    impl_singly_linked_list/
      problem.md                       문제 설명 · 시그니처 · 제약
      list.h                           공개 API (고치지 않는다)
      solution.c                       ← 여기를 채운다
      tests.py                         채점 테스트 (고치지 않는다)
  cpp/
    easy_remove_duplicates/
    medium_reverse_in_k_groups/
  python/
    easy_reverse_list/
    medium_detect_cycle/
```

디렉터리 이름에서 pytest 마커가 자동으로 붙는다 — 언어는 부모 폴더(`c` `cpp` `python`),
난이도는 이름 앞머리(`impl` `easy` `medium` `hard`). 그래서 이렇게 골라 돌릴 수 있다.

```sh
uv run pytest -m "cpp and medium"
uv run pytest -m c --tb=short
```

## 제출 파일에는 무엇이 들어 있나

풀 때 필요한 것만 들어 있다 — **구현할 함수**와, 손대면 안 되는 **주어진 타입** 정도.

```python
# python/medium_detect_cycle/solution.py
class Node:               # 주어진 노드 타입 — 고치지 않는다
    __slots__ = ("value", "next")
    ...

def detect_cycle(head: Node | None) -> Node | None:
    """사이클이 시작되는 노드. 없으면 None."""
    raise NotImplementedError  # TODO
```

`TODO` 가 남아 있으면 `list` 가 그 과제를 **미착수**로 표시한다. 자세한 설명·제약·예시는
전부 옆의 `problem.md` 에 있다.

## 명령

| 명령 | 하는 일 |
|---|---|
| `uv run runner.py list` | 주차별 과제와 채점 결과 요약 (`--fast` 면 착수 여부만) |
| `uv run runner.py show 1 [과제]` | 문제 설명 출력 (과제를 빼면 주차 개요) |
| `uv run runner.py test [주차]` | 채점. `--lang cpp`, `--task detect_cycle`, `-k 표현식` 으로 좁힌다 |
| `uv run runner.py submit 1` | 제출용 zip 만들기 (`submissions/`) |
| `uv run runner.py ci` | CI 채점 — 미착수는 실패로 치지 않는다 |
| `uv run runner.py new --topic "..."` | 다음 주차 뼈대 생성 |

주차와 과제는 편한 대로 부르면 된다. 주차는 `1`, `week_01`, `linked_list` 다 되고,
과제는 `detect_cycle` 처럼 이름만 대도 되고 `python/medium_detect_cycle` 로 정확히 짚어도 된다.

## C / C++ 는 어떻게 채점되나

1. 테스트가 `harness.native_lib(소스)` 를 부른다.
2. 소스가 바뀌었으면 `cc` / `c++` 로 `-shared -fPIC -O2 -Wall -Wextra` 빌드 →
   `build/native/` 에 캐시한다. 컴파일이 깨지면 컴파일러 출력이 그대로 실패 메시지로 나온다.
3. `ctypes` 로 심볼을 불러 파이썬에서 직접 호출한다.

그래서 C++ 쪽 제출 함수는 `extern "C"` 로 노출해야 한다. 배열을 주고받는 문제는
`int f(const int *values, int n, ..., int *out, int out_capacity)` 규약을 쓰고,
`harness.list_out_call` 이 이걸 파이썬 리스트 호출로 감싸 준다. 반환값이 음수면 오류다.

컴파일러가 없는 환경에서는 해당 테스트가 실패가 아니라 **skip** 된다.

포인터를 잘못 이으면 무한 루프가 나기 쉬워서 테스트마다 **20초 타임아웃**이 걸려 있다
(`pytest-timeout`, thread 방식이라 C 안에서 도는 루프도 잡는다). 걸리면 어느 줄에서
돌고 있었는지 스택이 찍히니 그걸 보면 된다.

## GitHub 에 올리면 자동으로 채점된다

`.github/workflows/tests.yml` 이 push 와 pull request 마다 돈다. 포크해서 쓰는
다른 사람의 저장소에서도, 남이 보낸 PR 에서도 똑같이 동작한다 — 별도 설정이 필요 없다.

연습 저장소라 **안 푼 문제 때문에 빨간불이 되지는 않는다.**

| | 언제 | CI |
|---|---|---|
| ✅ 통과 | 테스트가 다 통과 | 초록 |
| ⬜ 미착수 | `TODO` 가 그대로 남아 있음 | 초록 (아직 안 푼 것뿐) |
| ❌ 실패 | 손댔는데 테스트가 깨짐 | **빨강** |
| 💥 중단됨 | 무한 루프 / 세그폴트로 멈춤 | **빨강** |

결과는 과제별 표로 Actions 실행 요약 페이지에 붙는다. 같은 판정을 로컬에서도 볼 수 있다.

```sh
uv run runner.py ci        # 종료 코드: 실패나 중단이 하나라도 있으면 1
```

린트(`ruff check`, `ruff format --check`)도 같이 돈다. 맨 위 배지가 그 결과다 —
포크해서 쓴다면 배지 주소의 `k1seul/datascience-programming` 을 자기 저장소로 바꾸면 된다.

## 제출 파일 만들기 (eTL 등)

주차별로 **내가 쓴 코드만** 모아 zip 으로 묶는다. 채점 테스트(`tests.py`)와
`__init__.py` 는 빠지고, 컴파일에 필요한 `list.h` 같은 파일은 따라간다.

```sh
uv run runner.py submit 1 --name 2020-12345
# submissions/week_01_linked_list_2020-12345.zip
#   week_01_linked_list_2020-12345/c/impl_singly_linked_list/list.h
#   week_01_linked_list_2020-12345/c/impl_singly_linked_list/solution.c
#   week_01_linked_list_2020-12345/cpp/easy_remove_duplicates/solution.cpp
#   ...
```

압축 전에 한 번 채점해서 결과를 보여 주고, `TODO` 가 남은 과제가 있으면 경고한다
(막지는 않는다). 풀린 타래만 내려면 `--task`, 문제 설명도 같이 넣으려면 `--with-problem`,
채점을 건너뛰려면 `--no-check`.

GitHub 에서도 만들 수 있다 — Actions 탭 → **submit** → Run workflow 에서 주차를
고르면 zip 이 아티팩트로 올라온다. 다른 컴퓨터에서 받아 그대로 제출하면 된다.

`submissions/` 는 `.gitignore` 에 들어 있어서 저장소에 올라가지 않는다.

## 새 주차 시작하기

```sh
uv run runner.py new --topic "이진 탐색 트리" --slug binary_search_tree
uv run runner.py new --topic "정렬" --slug sorting \
  --tasks c/impl_merge_sort,python/easy_kth_largest,python/medium_sort_colors
```

`--tasks` 는 `<언어>/<난이도>[_문제이름]` 목록이다. 기본값은
`c/impl,cpp/easy,cpp/medium,python/easy,python/medium` — 문제 이름이 아직이면
난이도만 두고 나중에 폴더 이름만 바꿔도 된다.

만들고 나서 할 일은 각 `problem.md` 를 채우고, `tests.py` 의 빈 케이스 목록에
채점 케이스를 적는 것. `solution.*` 는 `TODO` 가 남은 채로 둔다.

## 규칙 몇 가지

- `tests.py` 와 `list.h` 처럼 "고치지 않는다" 고 적힌 파일은 건드리지 않는다.
  테스트를 고쳐서 통과시키면 그 주는 통째로 의미가 없다.
- 문제마다 붙은 **생각해 볼 것** 은 답을 적어 두는 편이 낫다. 다음에 같은 자료구조를
  만났을 때 되살아나는 건 코드가 아니라 그 메모다.
- 막히면 언어를 바꿔 같은 주의 다른 과제를 먼저 풀어 보라. 대개 같은 아이디어다.

## 요구 사항

- Python 3.13+ (`uv` 로 관리)
- C / C++ 컴파일러 (`cc`, `c++` — 없으면 해당 과제만 skip)
- `CC` / `CXX` 환경변수로 컴파일러를 바꿀 수 있다
