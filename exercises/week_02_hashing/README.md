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

## 이번 주에 익혀 두면 좋은 것

- 배열을 인덱스로 찾는 것과 해시로 찾는 것이 **왜 둘 다 O(1)** 인지
- 해시 맵을 쓸 자리를 알아보는 감각 — "이미 본 것을 기억해야 한다" 가 나오면 대개 해시입니다
- 누적 합처럼 **문제를 바꿔 놓아야** 해시가 쓸모 있어지는 경우 (C++ 중간 과제)
