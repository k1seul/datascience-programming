/* Problem statement: problem.md
 *
 * Fill in every TODO. Do not rename the classes or change the signatures:
 * the grader (shim.cpp) and main.cpp use them. You may add private helpers.
 */

#ifndef WEEK08_SOLUTION_HPP
#define WEEK08_SOLUTION_HPP

#include <iomanip>
#include <iostream>
#include <string>

using namespace std;

/* Delete this define and every NOT_IMPLEMENTED below once you start writing.
 * The grader reads them as "not written yet"; anything else counts as a real answer. */
#define NOT_IMPLEMENTED (-1000)

/* Greatest common divisor of a and b (both >= 0). gcd(0, b) is b. Given; use it. */
inline int gcd(int a, int b) {
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}

/* ===== (a) Fraction ==================================================== */

class Fraction {
private:
    int num;    // numerator
    int den;    // denominator, always positive

public:
    /* Keep the fraction in lowest terms with a positive denominator:
       Fraction(2, 4) is 1/2, Fraction(1, -2) is -1/2, Fraction(0, 5) is 0/1.
       den is never 0. */
    Fraction(int num, int den) : num(NOT_IMPLEMENTED), den(1) {
        /* TODO */
    }

    int getNum() const { return num; }
    int getDen() const { return den; }

    Fraction operator+(const Fraction &other) const {
        /* TODO */
        return Fraction(NOT_IMPLEMENTED, 1);
    }

    Fraction operator*(const Fraction &other) const {
        /* TODO */
        return Fraction(NOT_IMPLEMENTED, 1);
    }

    bool operator==(const Fraction &other) const {
        /* TODO */
        return false;
    }
};

/* Prints num/den, or only num when den is 1: 1/2, -3/4, 2, 0 */
ostream &operator<<(ostream &os, const Fraction &f) {
    /* TODO */
    os << "NOT_IMPLEMENTED";
    return os;
}

/* ===== (b) Shapes ====================================================== */

class Shape {
public:
    /* TODO: make area() and name() pure virtual functions:
       virtual double area() const = 0;   and the same for name() */
    double area() const { return NOT_IMPLEMENTED; }
    string name() const { return "NOT_IMPLEMENTED"; }

    virtual ~Shape() {}
};

class Rectangle : public Shape {
protected:
    int width;
    int height;

public:
    Rectangle(int width, int height) : width(0), height(0) {
        /* TODO */
    }

    int getWidth() const { return width; }
    int getHeight() const { return height; }

    double area() const {
        /* TODO: width * height */
        return NOT_IMPLEMENTED;
    }

    string name() const {
        /* TODO: "Rectangle" */
        return "NOT_IMPLEMENTED";
    }
};

/* A square is a rectangle whose sides are equal. It keeps Rectangle's area(). */
class Square : public Rectangle {
public:
    Square(int side) : Rectangle(0, 0) {
        /* TODO: call Rectangle's constructor with the right sides instead */
    }

    string name() const {
        /* TODO: "Square" */
        return "NOT_IMPLEMENTED";
    }
};

/* Prints name(area) with one digit after the point: Rectangle(12.0), Square(9.0) */
ostream &operator<<(ostream &os, const Shape &s) {
    /* TODO */
    os << "NOT_IMPLEMENTED";
    return os;
}

#endif /* WEEK08_SOLUTION_HPP */
