# Week 08 — 코딩 테스트 대비 (DP · 덱 · C++ 클래스)

다음 코딩 테스트를 준비하는 연습 주차입니다. 시험처럼 **Python, C, C++ 한 문제씩**입니다.

| 과제 | 언어 | 연습하는 것 | 예상 시간 |
|---|---|---|---|
| [`python/medium_shift_schedule`](python/medium_shift_schedule/problem.md) | Python | 고르기 DP와 되짚기 (Week 07) | 40분 |
| [`c/medium_deque_windows`](c/medium_deque_windows/problem.md) | C | 원형 덱 (Week 06), 덱에 인덱스를 넣고 빼며 한 번에 훑기 | 40분~1시간 |
| [`cpp/medium_fraction_shapes`](cpp/medium_fraction_shapes/problem.md) | C++ | **클래스**: 연산자 오버로딩, 상속, `virtual` | 40분~1시간 |

**C++ 부터 보세요.** Python 과 C 는 Week 06, 07 에서 한 것을 다른 문제에 적용하는 것이지만,
C++ 클래스는 이번이 처음입니다. 아래 [C++ 클래스 한눈에 보기](#c-클래스-한눈에-보기)를 먼저 읽고 시작하세요.

## 채점하기

```sh
uv run runner.py test 8                           # 세 과제를 모두 채점합니다
uv run runner.py test 8 --task shift_schedule     # Python 만
uv run runner.py test 8 --task deque_windows      # C 만
uv run runner.py test 8 --task fraction_shapes    # C++ 만
```

## 시험처럼 풀어 보기

[`exam/qe_practice.pdf`](exam/qe_practice.pdf) 는 이번 주 세 문제를 **논자시 시험지 형식**으로 묶은 문제지입니다.
실제 시험처럼 영어로 쓰여 있고, 힌트는 없습니다. 문제와 정답 조건은 각 과제의 `problem.md` 와 같습니다.

1. 타이머를 **2시간 30분**에 맞추고, 문제지와 터미널만 띄워 둡니다. `problem.md` 와 힌트는 보지 않습니다.
2. 시험장처럼 **채점기는 돌리지 않고** 직접 확인합니다. 아래 명령은 저장소 맨 위 폴더에서 실행합니다.

   ```sh
   # Python: 파일을 연 채로 함수를 직접 불러 봅니다. 예) max_pay([3, 2, 5, 10, 7])
   uv run python -i exercises/week_08_test_prep/python/medium_shift_schedule/solution.py

   # C: 출력을 Expected: 줄과 비교합니다
   cd exercises/week_08_test_prep/c/medium_deque_windows
   cc -Wall -Wextra -o main main.c solution.c && ./main
   cd -

   # C++: solution.hpp 를 include 하는 main.cpp 하나만 컴파일합니다
   cd exercises/week_08_test_prep/cpp/medium_fraction_shapes
   c++ -std=c++17 -Wall -Wextra -o main main.cpp && ./main
   cd -
   ```

3. 시간이 끝나면 `uv run runner.py test 8` 로 채점하고, 문제지에 적힌 배점으로 소문항별 점수를 세어 보세요.
   C, C++ 테스트 이름은 소문항(`test_a_`, `test_b_` …)으로, Python 은 함수 이름(`test_max_pay`, `test_work_days`)으로 시작합니다.
4. 틀린 곳은 `problem.md` 의 힌트와 "자주 하는 실수"를 보면서 고칩니다.

C++ 클래스가 처음이라면 문제지보다 아래 요약과 `problem.md` 의 힌트를 먼저 보고 푸는 편이 낫습니다.

## C++ 클래스 한눈에 보기

C++ 과제에 필요한 문법만 모았습니다. 자세한 설명은 각 문제의 힌트에 있습니다.

### Constructor and initializer list

```cpp
class Rectangle {
protected:
    int width;
    int height;
public:
    Rectangle(int width, int height) : width(width), height(height) {}
    //                                  멤버(매개변수)
};
```

매개변수 이름이 멤버와 같을 때 생성자 본문에서 `width = width;` 라고 쓰면 아무 일도 일어나지 않습니다.
초기화 목록을 쓰거나 `this->width = width;` 로 쓰세요. **시험에서 가장 많이 틀리는 곳입니다.**

### `const` member function

```cpp
int getWidth() const { return width; }    // 이 함수는 객체를 바꾸지 않는다
```

`const Rectangle &` 로 받은 객체에서는 `const` 함수만 부를 수 있습니다. 연산자와 getter 에는 `const` 를 붙이는 습관을 들이세요.

### Operator overloading

```cpp
// 멤버 함수: a + b 는 a.operator+(b) 로 바뀝니다
Fraction operator+(const Fraction &other) const { ... }

// cout << f 는 클래스 밖의 함수로 만듭니다. 왼쪽이 cout 이기 때문입니다
ostream &operator<<(ostream &os, const Fraction &f) {
    os << f.getNum() << "/" << f.getDen();
    return os;                              // cout << a << b 처럼 이어 쓰려면 꼭 반환
}
```

### Inheritance and calling the parent constructor

```cpp
class Square : public Rectangle {
public:
    Square(int side) : Rectangle(side, side) {}   // 부모 몫은 부모 생성자가 채웁니다
};
```

### `virtual`

```cpp
class Shape {
public:
    virtual double area() const = 0;   // 순수 가상 함수: 자식이 반드시 만든다
    virtual ~Shape() {}
};

const Shape &s = Square(3);
s.area();      // virtual 이면 Square 의 area(), 아니면 Shape 의 area()
```

**부모 타입의 참조나 포인터로 부를 때** 실제 객체의 함수가 불리게 하려면 `virtual` 이 필요합니다.
`virtual` 을 빠뜨려도 컴파일은 되기 때문에 놓치기 쉽습니다.

## 덱의 두 가지 쓰임

C 과제의 (b), (c) 는 같은 덱을 다르게 씁니다.

```
(b) 뒤에서만 넣고 뺀다 = 스택                (c) 뒤에 넣고 앞에서 뺀다 = 큐

    push_back →  [ 2  4  5 ]                    push_back → [ 1  4  6 ] → pop_front
    pop_back  ←                                  (창 안의 음수)  (창을 벗어난 것)
    (아직 답을 못 정한 날들)
```

두 방법 모두 덱에 **값이 아니라 인덱스**를 넣습니다. 인덱스가 있어야 며칠 차이인지, 창을 벗어났는지 알 수 있습니다.
그리고 각 인덱스가 덱에 한 번 들어가고 한 번 나오기 때문에, 전체가 `O(n)` 에 끝납니다.

## 참고 자료

- [Constructors and initialization of derived classes — Learn C++](https://www.learncpp.com/cpp-tutorial/constructors-and-initialization-of-derived-classes/)
  부모 생성자를 초기화 목록에서 부르는 이유를 순서대로 설명합니다.
- [Virtual functions and polymorphism — Learn C++](https://www.learncpp.com/cpp-tutorial/virtual-functions/)
  `virtual` 이 있을 때와 없을 때 어떤 함수가 불리는지 예제로 비교합니다.
- [Overloading the I/O operators — Learn C++](https://www.learncpp.com/cpp-tutorial/overloading-the-io-operators/)
  `operator<<` 를 클래스 밖에 만드는 방법과 `return os;` 가 필요한 이유입니다.
- [First negative in every window of size k — GeeksforGeeks](https://www.geeksforgeeks.org/dsa/first-negative-integer-every-window-size-k/)
  C 과제 (c) 와 같은 문제입니다. 느린 풀이부터 덱 풀이까지 차례로 보여 줍니다.

## 더 풀어 볼 문제 (LeetCode)

과제를 다 풀고 더 연습하고 싶다면 아래 문제를 풀어 보세요.

| | 문제 | 난이도 | 이번 주 과제와의 관계 |
|---|---|---|---|
| 641 | [Design Circular Deque](https://leetcode.com/problems/design-circular-deque/) | Medium | C 과제 (a) 의 덱을 클래스로 만듭니다 |
| 739 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | C 과제 (b) 와 같습니다 |
| 155 | [Min Stack](https://leetcode.com/problems/min-stack/) | Medium | 클래스 안에 자료구조를 두고 메서드를 만드는 연습입니다 |
| 1472 | [Design Browser History](https://leetcode.com/problems/design-browser-history/) | Medium | 뒤로/앞으로 가기를 클래스로 만듭니다 |
| 740 | [Delete and Earn](https://leetcode.com/problems/delete-and-earn/) | Medium | Python 과제와 같은 고르기 DP 입니다. 먼저 같은 값끼리 모아 두면 보입니다 |
| 1696 | [Jump Game VI](https://leetcode.com/problems/jump-game-vi/) | Medium | DP 표를 채울 때 C 과제의 덱을 함께 씁니다. 이번 주 세 주제가 다 들어 있습니다 |
