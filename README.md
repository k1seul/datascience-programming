# Data Science Programming — Fall Coding Exercises

**Seoul National University** · 데이터사이언스를 위한 프로그래밍 실습

[![tests](https://github.com/k1seul/datascience-programming/actions/workflows/tests.yml/badge.svg)](https://github.com/k1seul/datascience-programming/actions/workflows/tests.yml)

매주 토픽을 하나씩 정해서 **C, C++, Python** 세 언어로 문제를 풉니다.
어떤 언어로 풀든 채점은 **모두 pytest** 로 이루어집니다.
C 와 C++ 코드도 테스트가 알아서 공유 라이브러리로 빌드한 다음 `ctypes` 로 불러서 확인하기 때문에,
따로 컴파일해서 실행해 볼 필요가 없습니다.

## 설치

### 1. 저장소 받기

```sh
git clone https://github.com/k1seul/datascience-programming.git
cd datascience-programming
```

### 2. uv 설치하기

이 저장소는 파이썬 환경을 [uv](https://docs.astral.sh/uv/) 로 관리합니다.
파이썬을 따로 설치하지 않으셔도 uv 가 알아서 3.13 버전을 받아 줍니다.

**macOS / Linux**

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

설치가 끝나면 `~/.local/bin` 에 uv 가 들어갑니다.
같은 터미널에서 바로 쓰려면 아래 한 줄을 실행하시고, 아니면 터미널을 새로 여시면 됩니다.

```sh
source $HOME/.local/bin/env
```

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**패키지 관리자를 쓰시는 경우**

```sh
brew install uv        # macOS (Homebrew)
pipx install uv        # pipx
pip install uv         # 이미 파이썬이 있다면
```

설치가 되었는지 확인해 주세요. 버전 번호가 찍히면 성공입니다.

```sh
uv --version
# uv 0.11.8 (또는 그 이상)
```

잘 안 되면 [uv 설치 문서](https://docs.astral.sh/uv/getting-started/installation/) 를 참고하시면 됩니다.

### 3. 환경 만들기

```sh
uv sync
```

파이썬 3.13 과 pytest, ruff 를 받아서 `.venv/` 에 설치합니다. 처음 한 번만 하시면 됩니다.
이후 `uv run ...` 으로 실행하면 이 환경이 자동으로 쓰입니다.

### 4. C, C++ 컴파일러 확인

```sh
cc --version
c++ --version
```

없어도 괜찮습니다. 그 경우 C, C++ 과제는 실패가 아니라 **skip** 으로 처리되고
파이썬 과제는 그대로 푸실 수 있습니다. 설치하시려면 아래와 같이 하시면 됩니다.

```sh
sudo apt install build-essential   # Ubuntu, Debian
xcode-select --install             # macOS
```

Windows 에서는 WSL 을 쓰시는 편이 가장 편합니다.

## 이제 이렇게 씁니다

```sh
uv run runner.py list                   # 지금 과제가 어떤 상태인지 봅니다
uv run runner.py show 1 detect_cycle    # 문제 설명을 읽습니다
uv run runner.py test 1                 # 채점합니다
```

프로그래밍이 처음이거나 세 언어 중 낯선 게 있다면
[Week 00 — 기초 다지기](exercises/week_00_basics/README.md) 의 자료부터 보시면 좋습니다.

## 폴더 구조

`주차_토픽 / 언어 / 난이도_문제이름` 순서로 정리되어 있습니다.

```
exercises/week_01_linked_list/
  README.md                            이번 주 개요와 추천 읽을거리
  c/
    impl_singly_linked_list/
      problem.md                       문제 설명과 시그니처, 제약 조건
      list.h                           함수 규약 (수정하지 않습니다)
      solution.c                       ← 여기에 답을 쓰시면 됩니다
      tests.py                         채점 테스트 (수정하지 않습니다)
  cpp/
    easy_remove_duplicates/
    medium_reverse_in_k_groups/
  python/
    easy_reverse_list/
    medium_detect_cycle/
```

폴더 이름에서 pytest 마커가 자동으로 붙습니다.
언어는 부모 폴더 이름(`c`, `cpp`, `python`)에서, 난이도는 폴더 이름 앞부분(`impl`, `easy`, `medium`, `hard`)에서 가져옵니다.
덕분에 원하는 것만 골라서 돌릴 수 있습니다.

```sh
uv run pytest -m "cpp and medium"
uv run pytest -m c --tb=short
```

## 답안 파일에는 무엇이 들어 있나요

문제를 푸는 데 필요한 것만 들어 있습니다.
**구현할 함수**와, 수정하면 안 되는 **주어진 타입** 정도입니다.

```python
# python/medium_detect_cycle/solution.py
class Node:               # 주어진 노드 타입입니다. 수정하지 마세요.
    __slots__ = ("value", "next")
    ...

def detect_cycle(head: Node | None) -> Node | None:
    """사이클이 시작되는 노드를 반환합니다. 없으면 None 입니다."""
    raise NotImplementedError  # TODO
```

`TODO` 가 남아 있으면 `list` 명령이 그 과제를 **미착수**로 표시합니다.
자세한 설명과 제약 조건, 예시는 모두 옆에 있는 `problem.md` 에 적어 두었습니다.

## 명령 정리

| 명령 | 하는 일 |
|---|---|
| `uv run runner.py list` | 주차별 과제와 채점 결과를 한눈에 봅니다 (`--fast` 를 붙이면 착수 여부만) |
| `uv run runner.py show 1 [과제]` | 문제 설명을 출력합니다 (과제 이름을 빼면 주차 개요) |
| `uv run runner.py test [주차]` | 채점합니다. `--lang cpp`, `--task detect_cycle`, `-k 표현식` 으로 범위를 좁힐 수 있습니다 |
| `uv run runner.py submit 1` | 제출용 zip 을 만듭니다 (`submissions/` 에 생깁니다) |
| `uv run runner.py ci` | CI 와 같은 방식으로 채점합니다 (미착수는 실패로 보지 않습니다) |
| `uv run runner.py new --topic "..."` | 다음 주차 폴더를 만듭니다 |

주차와 과제는 편한 대로 부르시면 됩니다.
주차는 `1`, `week_01`, `linked_list` 가 모두 같은 뜻이고,
과제는 `detect_cycle` 처럼 이름만 말해도 되고 `python/medium_detect_cycle` 로 정확히 짚어도 됩니다.

## C 와 C++ 는 어떻게 채점되나요

1. 테스트가 `harness.native_lib(소스)` 를 부릅니다.
2. 소스가 바뀌었으면 `cc` 나 `c++` 로 `-shared -fPIC -O2 -Wall -Wextra` 옵션을 주어 빌드하고,
   결과를 `build/native/` 에 저장해 둡니다. 컴파일이 안 되면 컴파일러가 낸 메시지가 그대로 실패 사유로 보입니다.
3. `ctypes` 로 함수를 불러서 파이썬에서 직접 호출합니다.

그래서 C++ 답안의 함수는 `extern "C"` 로 노출해 주셔야 합니다.
내부에서 STL 을 쓰는 것은 얼마든지 괜찮고, 채점기가 부르는 함수 하나만 C 규약을 지키면 됩니다.

배열을 주고받는 문제는 `int f(const int *values, int n, ..., int *out, int out_capacity)` 형태로 통일했고,
`harness.list_out_call` 이 이것을 파이썬 리스트 호출처럼 감싸 줍니다. 반환값이 음수면 오류로 봅니다.

컴파일러가 없는 환경에서는 해당 테스트가 실패가 아니라 **skip** 으로 처리되니 걱정하지 않으셔도 됩니다.

연결 리스트를 다루다 보면 포인터를 잘못 이어서 무한 루프에 빠지는 일이 흔합니다.
그래서 테스트마다 **20초 타임아웃**을 걸어 두었습니다 (`pytest-timeout`, thread 방식이라 C 안에서 도는 루프도 잡아 줍니다).
타임아웃에 걸리면 어느 줄에서 돌고 있었는지 스택이 함께 출력되니 그 줄을 먼저 보시면 됩니다.

## GitHub 에 올리면 자동으로 채점됩니다

`.github/workflows/tests.yml` 이 push 와 pull request 마다 실행됩니다.
포크해서 쓰는 다른 분의 저장소에서도, 누군가 보낸 PR 에서도 똑같이 동작하고 따로 설정할 것은 없습니다.

연습용 저장소이다 보니 **아직 안 푼 문제 때문에 빨간불이 되지는 않게** 해 두었습니다.

| | 언제 | CI |
|---|---|---|
| ✅ 통과 | 테스트를 모두 통과했을 때 | 초록 |
| ⬜ 미착수 | `TODO` 가 그대로 남아 있을 때 | 초록 (아직 풀지 않았을 뿐이니까요) |
| ❌ 실패 | 답을 썼는데 테스트가 깨질 때 | **빨강** |
| 💥 중단됨 | 무한 루프나 세그폴트로 멈췄을 때 | **빨강** |

결과는 과제별 표로 Actions 실행 요약 페이지에 붙습니다. 같은 판정을 로컬에서도 볼 수 있습니다.

```sh
uv run runner.py ci        # 실패나 중단이 하나라도 있으면 종료 코드 1
```

린트(`ruff check`, `ruff format --check`)도 함께 돕니다.
맨 위 배지가 그 결과이고, 포크해서 쓰신다면 배지 주소의 `k1seul/datascience-programming` 부분만 자기 저장소로 바꾸면 됩니다.

## 제출 파일 만들기 (eTL 등)

주차별로 **직접 작성한 코드만** 모아서 zip 으로 묶어 줍니다.
채점 테스트(`tests.py`)나 `__init__.py` 는 빠지고, 컴파일에 필요한 `list.h` 같은 파일은 함께 들어갑니다.

```sh
uv run runner.py submit 1 --name 2020-12345
# submissions/week_01_linked_list_2020-12345.zip
#   week_01_linked_list_2020-12345/c/impl_singly_linked_list/list.h
#   week_01_linked_list_2020-12345/c/impl_singly_linked_list/solution.c
#   week_01_linked_list_2020-12345/cpp/easy_remove_duplicates/solution.cpp
#   ...
```

압축하기 전에 한 번 채점해서 결과를 보여 드리고, `TODO` 가 남은 과제가 있으면 알려 드립니다 (막지는 않습니다).
푼 것만 골라 내려면 `--task`, 문제 설명도 같이 넣으려면 `--with-problem`,
채점을 건너뛰려면 `--no-check` 를 붙이시면 됩니다.

GitHub 에서도 만들 수 있습니다.
Actions 탭에서 **submit** 워크플로를 고르고 Run workflow 를 누르면 zip 이 아티팩트로 올라오니,
다른 컴퓨터에서 받아 그대로 제출하시면 됩니다.

`submissions/` 폴더는 `.gitignore` 에 들어 있어서 저장소에는 올라가지 않습니다.

## 새 주차 만들기

```sh
uv run runner.py new --topic "이진 탐색 트리" --slug binary_search_tree
uv run runner.py new --topic "정렬" --slug sorting \
  --tasks c/impl_merge_sort,python/easy_kth_largest,python/medium_sort_colors
```

`--tasks` 에는 `<언어>/<난이도>[_문제이름]` 을 쉼표로 이어서 적습니다.
기본값은 `c/impl,cpp/easy,cpp/medium,python/easy,python/medium` 이고,
문제 이름을 아직 정하지 못했다면 난이도만 적어 두었다가 나중에 폴더 이름만 바꾸어도 됩니다.

만든 다음에는 각 `problem.md` 를 채우고, `tests.py` 의 빈 케이스 목록에 채점 케이스를 적으면 됩니다.
`solution.*` 는 `TODO` 가 남은 채로 두세요.

## 몇 가지 약속

- `tests.py` 와 `list.h` 처럼 "수정하지 않습니다" 라고 적힌 파일은 그대로 두세요.
  테스트를 고쳐서 통과시키면 그 주의 연습이 의미가 없어집니다.
- 문제마다 붙어 있는 **생각해 볼 것** 에는 짧게라도 답을 적어 두시길 권합니다.
  나중에 같은 자료구조를 다시 만났을 때 훨씬 빨리 기억이 돌아옵니다.
- 막히면 언어를 바꿔서 같은 주의 다른 과제를 먼저 풀어 보세요. 대개 같은 아이디어를 묻고 있습니다.

## 필요한 것 정리

- **Python** 3.13 이상 (uv 가 알아서 설치해 줍니다)
- **uv** ([설치 방법](#2-uv-설치하기))
- **C, C++ 컴파일러** (`cc`, `c++`). 없으면 해당 과제만 skip 되니 파이썬 과제는 그대로 진행됩니다.
  다른 컴파일러를 쓰고 싶으시면 `CC`, `CXX` 환경변수로 지정하실 수 있습니다
