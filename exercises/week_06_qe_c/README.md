# Week 06 — 논자시 대비 C

이번 주는 **C 과제만 세 개**입니다. 논자시 코딩 시험의 C 문제와 같은 형식으로 만들었습니다.
논자시 C 문제는 거의 매번 **자료구조를 직접 만들고, 그 자료구조로 알고리즘 하나를 푸는** 문제입니다.

| 순서 | 과제 | 내용 | 예상 시간 |
|---|---|---|---|
| 1 | [`c/impl_circular_deque`](c/impl_circular_deque/problem.md) | 배열로 원형 덱을 만들고, 그 덱으로 작업 스케줄러 만들기 | 1~1.5시간 |
| 2 | [`c/impl_recent_list`](c/impl_recent_list/problem.md) | 이중 연결 리스트로 "최근 본 상품" 목록 만들기 | 1.5~2시간 |
| 3 | [`c/impl_graph_search`](c/impl_graph_search/problem.md) | 인접 리스트 그래프에서 BFS, DFS, 사이클 판정 | 2시간 |

**순서대로 푸세요.** 1번은 배열과 인덱스, 2번은 포인터를 다룹니다. 3번 그래프는 둘을 함께 씁니다.
간선은 2번처럼 연결 리스트로 들고 있고, BFS 의 큐는 1번처럼 배열로 만듭니다.

## 시험처럼 풀어 보기

[`exam/qe_practice_c.pdf`](exam/qe_practice_c.pdf) 는 이번 주 세 문제를 **시험지 형식**으로 묶은 문제지입니다.
실제 시험처럼 영어로 쓰여 있고, 힌트는 없습니다. 문제와 정답 조건은 각 과제의 `problem.md` 와 같습니다.

1. 타이머를 **3시간**에 맞추고, 문제지와 터미널만 띄워 둡니다. `problem.md` 와 힌트는 보지 않습니다.
2. 각 문제 폴더의 `solution.c` 만 고치고, `main.c` 로 확인합니다. 시험장처럼 **채점기는 돌리지 않습니다.**
3. 시간이 끝나면 `uv run runner.py test 6` 으로 채점합니다. 테스트 이름이 소문항(`test_a_`, `test_b_` …)으로
   시작하니, 문제지에 적힌 배점으로 소문항별 점수를 세어 보세요.
4. 틀린 소문항은 `problem.md` 의 힌트와 "자주 하는 실수"를 보면서 고칩니다.

논자시를 앞두고 있다면 문제지로 먼저 풀고 `problem.md` 로 복습하는 순서를 권합니다.
이 내용을 처음 배운다면 `problem.md` 와 힌트로 먼저 풀어도 됩니다. 3시간은 처음 푸는 사람에게는 빠듯하니,
시간을 넘기더라도 끝까지 풀고 걸린 시간을 적어 두세요.

## 채점하기

```sh
uv run runner.py test 6                          # 세 과제를 모두 채점합니다
uv run runner.py test 6 --task circular_deque    # 1번만
uv run runner.py test 6 --task recent_list       # 2번만
uv run runner.py test 6 --task graph_search      # 3번만
```

## 논자시 C 문제는 이렇게 나옵니다

이번 주 과제는 아래 특징을 그대로 따라 만들었습니다. 풀면서 시험장에서 할 일을 같이 연습해 두세요.

**① 헤더 파일이 주어지고, 고치면 안 됩니다.**
구조체가 헤더에 모두 공개되어 있습니다. 함수만 정해진 모양대로 채우면 됩니다.
구조체 안이 공개되어 있으니 채점하는 쪽도 `prev` 포인터나 `front` 값을 직접 들여다봅니다. 이번 주 채점기도 그렇게 합니다.

**② 소문항이 쌓여 있습니다.**
(a)에서 만든 함수를 (e)에서 씁니다. 앞 소문항이 틀리면 뒤 소문항도 줄줄이 틀리니,
**앞 소문항을 확실히 하고 넘어가세요.** 테스트 이름이 `test_a_`, `test_b_` 로 시작하니 소문항별로 확인할 수 있습니다.

**③ `main.c` 로 직접 확인합니다.**
시험장에는 pytest 가 없습니다. 주어진 `main.c` 를 같이 컴파일해서 실행하고, 결과를 `Expected:` 줄과 눈으로 비교합니다.
이번 주 과제마다 `main.c` 를 넣어 두었으니 이 방법에 익숙해지세요.

```sh
cd exercises/week_06_qe_c/c/impl_circular_deque
cc -Wall -Wextra -o main main.c solution.c && ./main
```

`main.c` 는 여러분 파일이니 확인하고 싶은 것을 마음대로 더 넣어도 됩니다. 컴파일해서 생긴 `main` 파일은 git 과 제출 파일에서 빠집니다.

**④ 출력 형식이 정해져 있습니다.**
`[3, 1, 4]` 와 `[3,1,4]` 는 다른 답입니다. 공백, 쉼표, 줄바꿈까지 문제에 적힌 대로 출력하세요.

**⑤ 디버그 출력을 남기면 감점입니다.**
풀면서 넣은 `printf` 는 제출 전에 모두 지우세요. 이번 주 채점기는 출력 함수가 아닌 함수가 무엇이든 출력하면 실패로 처리합니다.

**⑥ 해제 함수가 꼭 있습니다.**
`deque_free`, `recent_free`, `graph_free` 처럼 만든 것을 모두 돌려주는 함수입니다.
그리고 BFS 의 큐처럼 **함수 안에서 잠깐 쓰고 버리는 메모리**도 반환하기 전에 해제해야 합니다.

**⑦ 큐가 전역 변수로 주어지기도 합니다.**
구조체 대신 `int queue[MAX]; int front, rear;` 같은 전역 변수가 헤더에 있을 수 있습니다. 원리는 같습니다.
다만 전역 변수는 함수가 끝나도 값이 남아 있으니, **다시 쓰기 전에 `front` 와 `rear` 를 0 으로 되돌리는 것**을 잊지 마세요.

## 이번 주 채점기가 더 확인하는 것

지금까지의 과제는 반환값만 봤습니다. 이번 주에는 세 가지를 더 확인합니다.

| | 어떻게 확인하나요 | 걸리는 경우 |
|---|---|---|
| 구조체 | 구조체를 직접 읽어서 따라갑니다 | `prev` 를 안 고침, `tail` 이 엉뚱한 곳을 가리킴, 덱 원소를 옮김 |
| 출력 | 출력 함수가 낸 글자를 하나하나 비교합니다 | 형식이 다름, 다른 함수에 `printf` 가 남아 있음 |
| 메모리 | `malloc` 과 `free` 를 몇 번 불렀는지 셉니다 | 해제 함수가 일부만 해제함, 함수 안에서 만든 배열을 해제하지 않음 |

메모리는 채점할 때 `solution.c` 의 `malloc`, `calloc`, `realloc`, `free` 를 횟수를 세는 함수로 바꿔 끼워서 확인합니다.
여러분 코드는 평소처럼 쓰면 됩니다.

`main.c` 로 확인할 때도 메모리를 검사할 수 있습니다.

```sh
valgrind --leak-check=full ./main     # Linux, WSL
leaks --atExit -- ./main              # macOS
```

해제하지 않은 메모리나 해제한 메모리를 읽은 곳이 있으면 몇 번째 줄인지 알려 줍니다.

## 시험장 체크리스트

제출하기 전에 한 번씩 확인하세요.

- [ ] `-Wall -Wextra` 로 컴파일했을 때 경고가 하나도 없나요? 초기화하지 않은 변수나 값을 반환하지 않는 경로 같은 진짜 버그가 경고로 나옵니다.
- [ ] 비어 있을 때, 하나뿐일 때, 꽉 찼을 때를 모두 확인했나요? 틀리는 곳은 대부분 이 세 경우입니다.
- [ ] `free` 한 포인터를 그 뒤에 읽지 않나요?
- [ ] `malloc` 한 것은 모두 `free` 했나요?
- [ ] 디버그용 `printf` 를 모두 지웠나요?
- [ ] 출력 형식(공백, 쉼표, 줄바꿈)이 문제와 똑같나요?
- [ ] 헤더 파일은 그대로인가요?

## 참고 자료

- [Implementation of Circular Queue Using Array — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/introduction-to-circular-queue/)
  1번 과제. 나머지 연산으로 인덱스를 돌리는 방법을 그림으로 보여 줍니다.
- [Doubly Linked List Tutorial — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/doubly-linked-list/)
  2번 과제. 넣기, 지우기에서 포인터가 어떻게 바뀌는지 경우별로 정리되어 있습니다.
- [Breadth First Search](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/),
  [Depth First Search](https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/),
  [Detect Cycle in a Directed Graph](https://www.geeksforgeeks.org/dsa/detect-cycle-in-a-graph/) — GeeksforGeeks
  3번 과제의 (c), (d), (e)입니다.
- [Python Tutor — C](https://pythontutor.com/c.html)
  C 코드도 한 줄씩 실행하면서 포인터가 어디를 가리키는지 화살표로 보여 줍니다. 2번 과제에서 `prev` 가 헷갈릴 때 써 보세요.
- [Valgrind Quick Start](https://valgrind.org/docs/manual/quick-start.html)
  위의 `valgrind` 명령 결과를 읽는 방법입니다.

## 더 풀어 볼 문제 (LeetCode)

과제를 다 풀고 더 연습하고 싶다면 아래 문제를 풀어 보세요. 모두 C 로 풀 수 있습니다.

| | 문제 | 난이도 | 이번 주 과제와의 관계 |
|---|---|---|---|
| 622 | [Design Circular Queue](https://leetcode.com/problems/design-circular-queue/) | Medium | 1번 과제에서 앞쪽 넣기/뒤쪽 빼기를 뺀 것입니다 |
| 641 | [Design Circular Deque](https://leetcode.com/problems/design-circular-deque/) | Medium | 1번 과제의 덱과 같습니다 |
| 707 | [Design Linked List](https://leetcode.com/problems/design-linked-list/) | Medium | 인덱스로 넣고 지우는 연결 리스트입니다. 이중 연결 리스트로 풀어 보세요 |
| 146 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | 2번 과제에 해시 테이블을 더하면 됩니다 |
| 841 | [Keys and Rooms](https://leetcode.com/problems/keys-and-rooms/) | Medium | 3번 과제의 BFS 나 DFS 로 갈 수 있는 곳을 찾습니다 |
| 207 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | 3번 과제의 사이클 판정과 같습니다 |
