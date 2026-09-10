# Week 00 — 기초 다지기 (Basics)

이번 주는 풀어야 할 문제가 없습니다.
대신 세 언어의 바탕이 되는 내용과, 이 저장소를 굴리는 데 쓰는 도구에 익숙해지는 시간입니다.

아래 자료를 전부 읽으실 필요는 없습니다.
자신 없는 부분만 골라서 보시고, 다음 주부터 문제를 푸시면 됩니다.

## 먼저 환경부터 확인해 주세요

uv 설치부터 컴파일러 확인까지는 [저장소 README 의 설치 안내](../../README.md#설치) 에
단계별로 적어 두었습니다. 아래 두 명령이 문제없이 돌아가면 준비가 끝난 것입니다.

```sh
uv sync                   # 파이썬 환경과 pytest, ruff 를 설치합니다
uv run runner.py list     # 과제 목록이 보이면 성공입니다
```

`cc` 나 `c++` 가 없어도 괜찮습니다. 그 경우 C, C++ 과제는 실패가 아니라 **skip** 으로 처리되고
파이썬 과제는 그대로 풀 수 있습니다.

## 언어별로 이번 학기에 쓰는 부분

| 언어 | 주로 쓰는 곳 | 익숙해지면 좋은 것 |
|---|---|---|
| C | 자료구조를 바닥부터 직접 만드는 과제 | 포인터, `malloc` 과 `free`, 구조체, 헤더와 컴파일 |
| C++ | 알고리즘을 구현하되 메모리는 직접 다루는 과제 | `new` 와 `delete`, 참조, 클래스, `extern "C"` |
| Python | 알고리즘의 뼈대를 빠르게 확인하는 과제 | 리스트와 딕셔너리, 클래스, 타입 힌트, pytest |

---

## C

C 에서는 포인터가 거의 전부입니다.
다른 문법은 필요할 때 찾아봐도 되지만, **주소와 값의 구분**만큼은 이번 주에 정리해 두시면
다음 주부터 훨씬 편해집니다.

- [Beej's Guide to C Programming](https://beej.us/guide/bgc/)
  전문이 무료로 공개되어 있습니다. 농담이 섞인 문체지만 내용은 아주 탄탄합니다.
  - [8장 Pointers](https://beej.us/guide/bgc/html/split/pointers.html) 이 장 하나만 제대로 읽어도 큰 도움이 됩니다.
- [Learn-C.org](https://www.learn-c.org/)
  브라우저에서 바로 코드를 고쳐 가며 볼 수 있는 짧은 튜토리얼입니다.
- [GeeksforGeeks C](https://www.geeksforgeeks.org/c/c-programming-language/)
  문법이 갑자기 기억나지 않을 때 찾아보기 좋습니다.
- [cppreference (C)](https://en.cppreference.com/w/c)
  표준 라이브러리의 정확한 명세입니다. [`malloc`](https://en.cppreference.com/w/c/memory/malloc) 페이지부터 보시면 됩니다.
- [Valgrind 빠른 시작](https://valgrind.org/docs/manual/quick-start.html)
  메모리 누수를 눈으로 확인하고 싶을 때 쓰는 도구입니다.

## C++

C 를 어느 정도 안다는 전제로, **C 와 달라지는 부분**만 골라 보셔도 충분합니다.

- [LearnCpp.com](https://www.learncpp.com/)
  무료 교재 중에서 가장 체계적으로 정리되어 있습니다.
  - [포인터 소개](https://www.learncpp.com/cpp-tutorial/introduction-to-pointers/)
  - [`new` 와 `delete` 로 동적 할당하기](https://www.learncpp.com/cpp-tutorial/dynamic-memory-allocation-with-new-and-delete/)
- [cppreference (C++)](https://en.cppreference.com/w/)
  [클래스](https://en.cppreference.com/w/cpp/language/classes),
  [`std::forward_list`](https://en.cppreference.com/w/cpp/container/forward_list) 페이지를 참고하시면 됩니다.
- [cplusplus.com reference](https://cplusplus.com/reference/)
  cppreference 가 빡빡하게 느껴질 때 대안으로 볼 만합니다.
- [GeeksforGeeks C++](https://www.geeksforgeeks.org/cpp/c-plus-plus/)

이 저장소의 C++ 과제는 채점기가 `ctypes` 로 함수를 부르기 때문에 `extern "C"` 로 노출해야 합니다.
안에서 STL 을 쓰는 것은 전혀 문제가 없고, 채점기가 부르는 함수 하나만 C 규약을 지키면 됩니다.

## Python

- [공식 튜토리얼](https://docs.python.org/3/tutorial/) ([한국어 번역](https://docs.python.org/ko/3/tutorial/))
  3장부터 5장까지가 이번 학기에 가장 자주 쓰는 내용입니다.
- [표준 라이브러리 목차](https://docs.python.org/3/library/index.html)
  어떤 기능이 이미 있는지 한 번 훑어 두면 직접 만들 일이 줄어듭니다.
- [typing](https://docs.python.org/3/library/typing.html)
  과제 코드가 타입 힌트로 명세를 알려 줍니다. 직접 쓰지 않더라도 읽을 줄만 알면 됩니다.
- [Automate the Boring Stuff](https://automatetheboringstuff.com/)
  프로그래밍 자체가 처음이시라면 여기서 시작하시길 권합니다.

## 도구

- [uv](https://docs.astral.sh/uv/) ([시작하기](https://docs.astral.sh/uv/getting-started/))
  이 저장소의 파이썬 환경을 관리합니다.
- [pytest](https://docs.pytest.org/en/stable/) ([시작하기](https://docs.pytest.org/en/stable/getting-started.html))
  채점이 모두 pytest 로 돌아갑니다. 테스트를 직접 짜기보다는 **실패 메시지를 읽는 법**이 중요합니다.
- [Ruff](https://docs.astral.sh/ruff/)
  린트와 코드 포맷을 담당합니다.
- [Pro Git (한국어)](https://git-scm.com/book/ko/v2)
  1장부터 3장까지면 이번 학기에 필요한 만큼은 됩니다.

## 눈으로 보면 훨씬 빨리 이해됩니다

- [Python Tutor](https://pythontutor.com/)
  **C, C++, Python 모두** 지원합니다. 코드를 한 줄씩 실행하면서 메모리와 포인터가
  어떻게 연결되는지 그림으로 보여 주기 때문에, 연결 리스트를 처음 만들 때 특히 도움이 됩니다.
- [VisuAlgo — Linked List](https://visualgo.net/en/list)
  자료구조 연산을 애니메이션으로 보여 줍니다.
- [Compiler Explorer](https://godbolt.org/)
  작성한 C, C++ 코드가 어떤 어셈블리가 되는지 바로 볼 수 있습니다. 당장 필요하지는 않지만
  한 번 구경해 두면 감이 조금 달라집니다.

## 다음 주

[Week 01 — 연결 리스트](../week_01_linked_list/README.md) 부터 문제가 시작됩니다.
포인터가 아직 익숙하지 않다면 위의 Beej 8장과 Python Tutor 두 가지만이라도 먼저 보고 오시길 권합니다.
