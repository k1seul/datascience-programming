# Week 02 / Python (쉬움) — 빈도 세기

딕셔너리로 개수를 세는 세 가지 문제입니다. 해싱을 쓰는 가장 흔한 형태입니다.

```python
count_values([3, 1, 3, 3, 1])   # {3: 3, 1: 2}
first_unique("leetcode")        # "l"
is_anagram("anagram", "nagaram")  # True
```

## 구현할 함수

```python
def count_values(values: Iterable[int]) -> dict[int, int]: ...
def first_unique(text: str) -> str | None: ...
def is_anagram(left: str, right: str) -> bool: ...
```

| 함수 | 하는 일 |
|---|---|
| `count_values` | 값마다 몇 번 나왔는지 세어 딕셔너리로 |
| `first_unique` | 딱 한 번만 나오는 문자 중 **가장 먼저 나온** 것. 없으면 `None` |
| `is_anagram` | 두 문자열이 같은 문자를 같은 개수만큼 쓰는지 |

## 조건

- **`collections.Counter` 를 쓰지 마세요.** 딕셔너리로 직접 세어 보는 것이 이번 과제의 목적입니다.
  (채점기가 확인합니다.) 다 풀고 나서 `Counter` 로 바꿔 보면 무엇이 줄어드는지 보일 겁니다.
- 빈 입력도 처리해야 합니다. `count_values([])` 는 `{}`, `first_unique("")` 는 `None`,
  `is_anagram("", "")` 는 `True` 입니다.
- `first_unique` 는 문자열을 두 번 훑으면 됩니다. 한 번은 세고, 한 번은 찾습니다.
  세면서 동시에 찾으려고 하면 꼬입니다.
- 길이가 다른 두 문자열은 애너그램이 될 수 없습니다.

## 채점

```sh
uv run runner.py test 2 --task counting
```

## 생각해 볼 것

- `dict.get(key, 0)` 과 `if key in d` 중 어느 쪽이 읽기 편한가요?
  `collections.defaultdict` 를 쓰면 또 어떻게 달라질까요?
- `is_anagram` 을 세지 않고 `sorted(left) == sorted(right)` 로도 풀 수 있습니다.
  길이가 n 일 때 두 방법의 시간복잡도는 각각 얼마인가요?
- `first_unique` 에서 "가장 먼저 나온" 을 알 수 있는 이유는 무엇일까요?
  파이썬 딕셔너리가 넣은 순서를 기억한다는 사실과 관계가 있습니다.
