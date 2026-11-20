// Self-check driver. Compile it and compare each line with the "Expected:" line under it:
//
//     c++ -std=c++17 -Wall -Wextra -o main main.cpp && ./main
//
// solution.hpp holds the whole solution, so main.cpp is the only file to compile.
// This file is yours: add any checks you like. The grader does not use it.

#include <iomanip>
#include <iostream>

#include "solution.hpp"

using namespace std;

int main() {
    cout << "== (a) Fraction ==\n";
    Fraction half(2, 4), third(1, 3);
    cout << half << "  " << Fraction(1, -2) << "  " << Fraction(6, 3) << "\n";
    cout << "Expected: 1/2  -1/2  2\n";

    cout << (half + third) << "  " << (half - third) << "  " << (half * third) << "\n";
    cout << "Expected: 5/6  1/6  1/6\n";

    cout << boolalpha << (half == Fraction(3, 6)) << " " << (half == third) << "\n";
    cout << "Expected: true false\n";

    cout << "\n== (b) Shapes ==\n";
    Rectangle rect(3, 4);
    Square square(3);
    Triangle tri(3, 5);
    cout << rect << "  " << square << "  " << tri << "\n";
    cout << "Expected: Rectangle(12.0)  Square(9.0)  Triangle(7.5)\n";

    cout << square.getWidth() << "x" << square.getHeight() << "\n";
    cout << "Expected: 3x3\n";

    // Through a Shape &: the right area() and name() only run when they are virtual.
    const Shape &some = square;
    cout << some.name() << " " << fixed << setprecision(1) << some.area() << "\n";
    cout << "Expected: Square 9.0\n";

    cout << (tri < square) << " " << (rect < square) << "\n";
    cout << "Expected: true false\n";
    return 0;
}
