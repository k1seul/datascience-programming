# Week 04 / C++ (쉬움) — 문자열을 재귀로

문자열도 연결 리스트처럼 재귀적으로 볼 수 있습니다.
"첫 글자 + 나머지 문자열" 이거나, "양 끝 두 글자 + 가운데 부분" 이거나요.

이번 과제는 인덱스를 좁혀 가며 문자열을 재귀로 처리하는 세 가지 연습입니다.

## 구현할 함수

```cpp
extern "C" int reverse_string(const char *s, char *out, int out_capacity);
extern "C" int count_vowels(const char *s);
extern "C" int is_subsequence(const char *a, const char *b);
```

| 함수 | 하는 일 | 반환값 |
|---|---|---|
| `reverse_string` | `s` 를 거꾸로 `out` 에 | 쓴 글자 수, 용량 부족이면 `-1` |
| `count_vowels` | 모음 개수 (대소문자 무시) | 개수 |
| `is_subsequence` | `a` 가 `b` 의 부분 수열인지 | `1` 또는 `0` |

```
reverse_string("hello")              ->  "olleh"  (5)
count_vowels("Programming")          ->  3        (o, a, i)
is_subsequence("ace", "abcde")       ->  1
is_subsequence("aec", "abcde")       ->  0
```

## 조건

- **세 함수 모두 재귀로 작성해야 합니다.** `for` 와 `while` 을 쓰지 마세요.
  채점기가 소스를 확인합니다.
- 모음은 `a e i o u` 이고 대소문자를 구분하지 않습니다. `cctype` 의 `tolower` 를 쓰면 편합니다.
- `out` 은 NUL 로 끝나야 합니다. 용량은 NUL 을 포함해 계산합니다.
  `"olleh"` 는 5글자이므로 `out_capacity` 가 최소 6이어야 합니다.
- 빈 문자열도 처리합니다. `reverse_string("")` 은 `0`, `count_vowels("")` 은 `0` 입니다.
- `is_subsequence("", anything)` 은 `1` 입니다. 빈 문자열은 모든 문자열의 부분 수열입니다.

## 부분 수열이란

`a` 의 글자들이 **순서를 지키면서** `b` 안에 차례로 나타나면 부분 수열입니다.
붙어 있지 않아도 됩니다.

```
"ace" 는 "abcde" 의 부분 수열   ->  a _ c _ e
"aec" 는 "abcde" 의 부분 수열이 아님  ->  a 다음에 e 를 찾으면 c 가 이미 지나갔다
```

## 힌트

세 함수가 좁혀 가는 방식이 조금씩 다릅니다.

| 함수 | 어떻게 쪼개나 |
|---|---|
| `count_vowels` | 첫 글자를 보고 세고, **나머지 문자열**을 재귀 |
| `reverse_string` | 나머지를 먼저 뒤집어 쓰고, **첫 글자를 마지막에** |
| `is_subsequence` | 두 문자열을 **동시에** 좁힌다. 첫 글자가 같으면 양쪽 모두 한 칸, 다르면 `b` 만 한 칸 |

`is_subsequence` 가 가장 재미있습니다. 기저 조건이 **두 개** 필요합니다.
`a` 를 다 썼으면 성공이고, `a` 가 남았는데 `b` 가 끝났으면 실패입니다. 순서가 중요합니다.

문자열 길이를 매번 `strlen` 으로 재지 말고, 보조 함수에 인덱스를 넘기는 쪽이 깔끔합니다.

```cpp
static int helper(const char *s, int i, ...);
```

## 채점

```sh
uv run runner.py test 4 --task recursive_string
```

## 생각해 볼 것

- `reverse_string` 에서 첫 글자를 **먼저** 쓰면 무엇이 나오나요? 직접 바꿔 보세요.
  Week 04 의 C 과제 `to_string_reverse` 와 같은 이야기입니다.
- `is_subsequence` 에서 첫 글자가 같을 때 "양쪽을 한 칸씩" 말고 "`b` 만 한 칸" 으로도
  가 볼 수 있습니다. 그렇게 해도 답이 맞을까요? 왜 그럴까요?
- 세 함수의 재귀 깊이는 문자열 길이에 비례합니다. 10만 글자 문자열이라면 어떻게 될까요?
