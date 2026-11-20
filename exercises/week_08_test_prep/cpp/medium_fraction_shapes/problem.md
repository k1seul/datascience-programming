# Week 08 / C++ (중간) — 분수와 도형 클래스

지금까지 C++ 과제는 함수 하나를 `extern "C"` 로 만드는 것이었습니다. 이번에는 **클래스**를 만듭니다.
논자시와 코딩 테스트의 C++ 문제는 거의 언제나 클래스 문제입니다.

| 소문항 | 클래스 | 연습하는 것 | 배점 |
|---|---|---|---|
| (a) | `Fraction` | 생성자, 연산자 오버로딩(`+`, `-`, `*`, `==`, `<<`) | 50 |
| (b) | `Shape`, `Rectangle`, `Square`, `Triangle` | 상속, 기반 클래스 생성자 호출, `virtual` | 50 |

## 파일

시험처럼 **헤더 파일 하나**(`solution.hpp`)에 클래스를 모두 작성합니다. 멤버와 함수 모양은 미리 적어 두었으니
`TODO` 를 채우면 됩니다.

| 파일 | 하는 일 |
|---|---|
| `solution.hpp` | **여러분이 작성하는 파일** |
| `main.cpp` | 직접 확인할 때 쓰는 파일. 마음대로 고쳐도 됩니다 |
| `shim.cpp` | 채점기가 쓰는 파일. 클래스를 파이썬에서 부를 수 있게 이어 줍니다. 고치지 마세요 |

**함수 이름, 매개변수, `const` 를 바꾸지 마세요.** `shim.cpp` 가 그대로 부르기 때문에 바꾸면 컴파일이 안 됩니다.

## (a) `Fraction` — 50점

분자 `num` 과 분모 `den` 으로 분수를 나타냅니다. **언제나 기약분수**로, **분모는 양수**로 저장합니다.

| 만들 때 | 저장되는 값 |
|---|---|
| `Fraction(2, 4)` | `1/2` |
| `Fraction(6, 3)` | `2/1` |
| `Fraction(1, -2)` | `-1/2` |
| `Fraction(-3, -9)` | `1/3` |
| `Fraction(0, 5)` | `0/1` |

연산 결과도 기약분수입니다.

```cpp
Fraction(1, 2) + Fraction(1, 3)     // 5/6
Fraction(1, 3) - Fraction(1, 2)     // -1/6
Fraction(2, 3) * Fraction(3, 4)     // 1/2
Fraction(1, 2) == Fraction(2, 4)    // true
```

`cout << f` 는 `num/den` 을 출력합니다. 분모가 1이면 분자만 출력합니다.

| 분수 | 출력 |
|---|---|
| `Fraction(1, 2)` | `1/2` |
| `Fraction(3, -4)` | `-3/4` |
| `Fraction(4, 2)` | `2` |
| `Fraction(0, 7)` | `0` |

분모는 0 이 들어오지 않습니다. 계산 중에 `int` 범위를 넘는 값도 들어오지 않습니다.

## (b) 도형 — 50점

```
            Shape              area(), name() : 순수 가상 함수
           /     \
     Rectangle   Triangle
         |
       Square                  Rectangle 의 area() 를 그대로 물려받음
```

| 클래스 | 생성자 | `area()` | `name()` |
|---|---|---|---|
| `Rectangle` | `Rectangle(width, height)` | `width × height` | `"Rectangle"` |
| `Square` | `Square(side)` | `Rectangle` 것을 그대로 씁니다 | `"Square"` |
| `Triangle` | `Triangle(base, height)` | `base × height ÷ 2` | `"Triangle"` |

- `Shape` 의 `area()` 와 `name()` 을 **순수 가상 함수**(`virtual ... = 0`)로 바꾸세요.
  그래야 `const Shape &` 로 받은 도형에서 각자의 `area()`, `name()` 이 불립니다.
- `Square` 는 **`Rectangle` 의 생성자를 불러서** 가로와 세로를 같은 값으로 채웁니다. `Square(5)` 의 `getWidth()` 와 `getHeight()` 는 둘 다 `5` 입니다.
- `area()` 는 `double` 입니다. `Triangle(3, 5)` 의 넓이는 `7` 이 아니라 `7.5` 입니다.

두 도형을 넓이로 비교하는 `<` 와, 출력용 `<<` 도 만듭니다. 둘 다 `const Shape &` 를 받으니 모든 도형에 쓸 수 있습니다.

```cpp
Triangle(3, 5) < Square(3)      // true   (7.5 < 9.0)
Square(2) < Rectangle(1, 4)     // false  (넓이가 같으면 작지 않습니다)

cout << Rectangle(3, 4);        // Rectangle(12.0)
cout << Square(3);              // Square(9.0)
cout << Triangle(3, 5);         // Triangle(7.5)
```

`<<` 는 `이름(넓이)` 를 출력하고, 넓이는 소수점 아래 **한 자리**입니다.

## 직접 확인하기

`solution.hpp` 에 모든 코드가 들어 있으니 `main.cpp` 하나만 컴파일하면 됩니다.
각 줄 아래의 `Expected:` 줄과 똑같이 나오면 됩니다.

```sh
cd exercises/week_08_test_prep/cpp/medium_fraction_shapes
c++ -std=c++17 -Wall -Wextra -o main main.cpp && ./main
```

## 채점

```sh
uv run runner.py test 8 --task fraction_shapes
```

채점기는 `shim.cpp` 를 컴파일합니다. `shim.cpp` 가 `solution.hpp` 를 `#include` 하므로, 컴파일 오류가 나면
오류 메시지에 `solution.hpp` 의 줄 번호가 나옵니다.

## 힌트

막힐 때 하나씩 펼쳐 보세요.

<details>
<summary>힌트 1 — 생성자에서 매개변수와 멤버의 이름이 같을 때</summary>

```cpp
Fraction(int num, int den) {
    num = num;          // 매개변수 num 에 자기 자신을 넣을 뿐, 멤버는 그대로입니다
}
```

멤버를 가리키려면 `this->num` 이라고 쓰거나, 초기화 목록을 씁니다.

```cpp
Rectangle(int width, int height) : width(width), height(height) {}
//                                  멤버(매개변수)
```

</details>

<details>
<summary>힌트 2 — 기약분수로 만들기</summary>

1. 분모가 음수이면 분자와 분모의 부호를 모두 바꿉니다.
2. 분자와 분모의 최대공약수 `g` 로 둘 다 나눕니다. 최대공약수는 유클리드 호제법으로 구합니다.

```cpp
int gcd(int a, int b) {        // a, b 는 0 이상
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}
```

분자가 음수일 수 있으니 `gcd` 에는 절댓값을 넘기세요. `gcd(0, 5)` 는 `5` 라서 `0/5` 는 `0/1` 이 됩니다.

생성자에서 이렇게 정리해 두면, 연산자는 공식대로 계산해서 `Fraction(분자, 분모)` 를 만들어 반환하기만 하면 됩니다.
정리는 생성자가 해 줍니다. `a/b + c/d = (ad + cb) / bd` 입니다.

</details>

<details>
<summary>힌트 3 — 상속과 순수 가상 함수</summary>

```cpp
class Shape {
public:
    virtual double area() const = 0;     // = 0 : 여기서는 만들지 않고, 자식이 반드시 만든다
    virtual string name() const = 0;
    virtual ~Shape() {}
};

class Square : public Rectangle {
public:
    Square(int side) : Rectangle(side, side) {}   // 부모 생성자를 초기화 목록에서 부릅니다
    string name() const override { return "Square"; }
};
```

`override` 는 쓰지 않아도 되지만, 쓰면 부모에 같은 모양의 가상 함수가 없을 때 컴파일러가 알려 줍니다.

</details>

<details>
<summary>힌트 4 — 소수점 한 자리로 출력하기</summary>

```cpp
#include <iomanip>

os << s.name() << "(" << fixed << setprecision(1) << s.area() << ")";
```

`fixed` 와 `setprecision(1)` 은 "소수점 아래 한 자리로 고정"이라는 뜻입니다. `9` 는 `9.0`, `7.5` 는 `7.5` 로 나옵니다.

</details>

## 자주 하는 실수

**`virtual` 을 빠뜨리기**

`Shape` 의 `area()` 가 가상 함수가 아니면, `const Shape &` 로 부를 때 `Shape` 의 `area()` 가 불립니다.
`Square` 로 직접 부르면 맞는데 `<` 와 `<<` 만 틀린다면 이 실수입니다.

**정수 나눗셈**

`base * height / 2` 는 정수끼리 나누니 `3 * 5 / 2` 가 `7` 이 됩니다. `2.0` 으로 나누세요.

**`Square` 에서 부모 생성자를 부르지 않기**

`Square(int side) : Rectangle(0, 0)` 을 그대로 두면 가로, 세로가 0 입니다.

**기약분수로 만들지 않고 `==` 비교하기**

`1/2` 와 `2/4` 는 같은 분수입니다. 생성자에서 기약분수로 정리해 두면 `==` 는 분자끼리, 분모끼리 비교하면 끝입니다.

## 더 생각해 볼 것

- `Fraction` 에 `operator/` 를 더한다면 0 으로 나누는 경우를 어떻게 처리해야 할까요?
- `Shape` 의 소멸자는 왜 `virtual` 일까요? `Shape *p = new Square(3); delete p;` 를 생각해 보세요.
