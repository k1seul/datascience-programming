# Week 02 — 해싱 (Hashing)

이번 주 토픽은 해싱입니다.
"값을 보고 자리를 바로 계산한다"는 하나의 아이디어가 어디까지 쓰이는지 따라가 봅니다.

C 에서는 **값이 곧 인덱스가 되는 가장 단순한 형태**부터 시작하고,
C++ 와 Python 에서는 그 위에 얹힌 집합과 맵을 실제 문제에 써 봅니다.

| 과제 | 언어 | 난이도 | 내용 |
|---|---|---|---|
| [`c/easy_find_duplicates`](c/easy_find_duplicates/problem.md) | C | 쉬움 | 0~99 에서 중복 찾기 (직접 주소 표) |
| [`cpp/easy_intersection`](cpp/easy_intersection/problem.md) | C++ | 쉬움 | 두 배열의 교집합 (hash set) |
| [`cpp/medium_subarray_sum`](cpp/medium_subarray_sum/problem.md) | C++ | 중간 | 합이 k 인 부분 배열 개수 (prefix sum + hash map) |
| [`python/easy_counting`](python/easy_counting/problem.md) | Python | 쉬움 | 빈도 세기 세 가지 |
| [`python/medium_longest_consecutive`](python/medium_longest_consecutive/problem.md) | Python | 중간 | 가장 긴 연속 수열 (hash set) |

## 채점하기

```sh
uv run runner.py test 2                            # 다섯 과제를 모두 채점합니다
uv run runner.py test 2 --lang cpp                 # 언어별로 골라서 채점합니다
uv run runner.py test 2 --task find_duplicates     # 한 과제만 채점합니다
```

## 이번 주의 흐름

```
값 = 인덱스   →   집합으로 존재 확인   →   맵으로 개수 세기   →   맵으로 지나온 것 기억
   C 과제          C++ 쉬움                Python 쉬움          C++ 중간, Python 중간
```

C 과제의 `int seen[100]` 은 사실 **해시 함수가 `hash(x) = x` 이고 충돌이 없는 해시 테이블**입니다.
여기서 값의 범위가 넓어지거나 값이 문자열이 되면 그 배열을 그대로 쓸 수 없고,
그때부터 진짜 해시 함수와 충돌 처리가 필요해집니다.
C++ 과제에서 `seen[value]` 대신 `unordered_set` 을 쓰는 이유가 바로 그것입니다.

## 추천 읽을거리

- [Hashing Data Structure — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/hashing-data-structure/)
  해시 테이블 전반을 훑어 주는 글입니다. 해시 함수, 충돌, 체이닝과 개방 주소법까지 한 페이지에 있습니다.
- [VisuAlgo — Hash Table](https://visualgo.net/en/hashtable)
  값을 넣을 때 어느 칸으로 가는지, 충돌이 나면 어떻게 되는지 애니메이션으로 보여 줍니다.
- [cppreference — `std::unordered_map`](https://en.cppreference.com/w/cpp/container/unordered_map),
  [Python 공식 문서 — `dict`](https://docs.python.org/3/library/stdtypes.html#dict)
  이번 주에 쓰는 도구의 정확한 명세입니다.

## 더 풀어 볼 문제 (LeetCode)

과제를 다 풀고 더 연습하고 싶으시면 아래 문제들을 권합니다.
꼭 다 풀어야 하는 것은 아니고, 약한 유형을 골라 두세 문제만 해 보셔도 충분합니다.

### Checking for existence

집합에 넣어 두고 "이미 봤나"만 묻는 가장 단순한 형태입니다.

| | 문제 | 난이도 |
|---|---|---|
| 217 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Easy |
| 1436 | [Destination City](https://leetcode.com/problems/destination-city/) | Easy |
| 1496 | [Path Crossing](https://leetcode.com/problems/path-crossing/) | Easy |

1496 번은 좌표 한 쌍이 열쇠가 됩니다. 숫자가 아닌 것을 어떻게 집합에 넣을지 생각해 보세요.

### Counting

세어 두고 그 개수를 다시 재료로 쓰는 문제들입니다. 뒤로 갈수록 세는 것 자체보다
**언제 세고 언제 지우는지**가 중요해집니다.

| | 문제 | 난이도 |
|---|---|---|
| 1748 | [Sum of Unique Elements](https://leetcode.com/problems/sum-of-unique-elements/) | Easy |
| 1207 | [Unique Number of Occurrences](https://leetcode.com/problems/unique-number-of-occurrences/) | Easy |
| 1512 | [Number of Good Pairs](https://leetcode.com/problems/number-of-good-pairs/) | Easy |
| 451 | [Sort Characters By Frequency](https://leetcode.com/problems/sort-characters-by-frequency/) | Medium |
| 930 | [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/) | Medium |
| 567 | [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Medium |
| 1695 | [Maximum Erasure Value](https://leetcode.com/problems/maximum-erasure-value/) | Medium |

1207 번은 "개수를 센 결과를 다시 센다"는 점이 재미있습니다.
1512 번은 다 세고 나면 짝의 개수가 공식 하나로 나옵니다. 일일이 세지 마세요.

### General

한쪽 값과 다른 쪽 값을 **짝지어 기억하는** 문제들입니다. 집합이 아니라 맵이 필요한 이유죠.

| | 문제 | 난이도 |
|---|---|---|
| 205 | [Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/) | Easy |
| 290 | [Word Pattern](https://leetcode.com/problems/word-pattern/) | Easy |
| 1657 | [Determine if Two Strings Are Close](https://leetcode.com/problems/determine-if-two-strings-are-close/) | Medium |

205 번과 290 번은 같은 아이디어를 문자와 단어에 각각 적용한 문제입니다.
둘 다 **양쪽 방향**을 확인해야 한다는 함정이 있습니다. 한쪽만 보면 틀립니다.

---

이번 주 과제와 짝이 되는 문제들이 있습니다.
217 번은 C 과제와 같은 질문을 값 범위 제한 없이 묻고, 1748 번과 1207 번은 Python 쉬움 과제의
빈도 세기를 그대로 씁니다. **930 번은 C++ 중간 과제와 같은 기법**(누적 합 + 해시 맵)이라,
`subarray_sum` 을 풀고 나서 바로 이어 풀면 좋습니다.

## 이번 주에 익혀 두면 좋은 것

- 배열을 인덱스로 찾는 것과 해시로 찾는 것이 **왜 둘 다 O(1)** 인지
- 해시 맵을 쓸 자리를 알아보는 감각 — "이미 본 것을 기억해야 한다" 가 나오면 대개 해시입니다
- 누적 합처럼 **문제를 바꿔 놓아야** 해시가 쓸모 있어지는 경우 (C++ 중간 과제)
