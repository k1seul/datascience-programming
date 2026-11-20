// Grader shim: exposes the classes in solution.hpp to the Python tests through ctypes.
// It belongs to the grader, like tests.py. You do not need to read or change it.

#include <cstring>
#include <sstream>
#include <string>

#include "solution.hpp"

namespace {

// Copy text into buf (always NUL-terminated) and return its full length.
int write_text(const std::string &text, char *buf, int cap) {
    if (cap > 0) {
        std::size_t n = text.size() < std::size_t(cap - 1) ? text.size() : std::size_t(cap - 1);
        std::memcpy(buf, text.data(), n);
        buf[n] = '\0';
    }
    return static_cast<int>(text.size());
}

void unpack(const Fraction &f, int *out_num, int *out_den) {
    *out_num = f.getNum();
    *out_den = f.getDen();
}

// kind 0: Rectangle(a, b), kind 1: Square(a), kind 2: Triangle(a, b)
template <typename F>
auto with_shape(int kind, int a, int b, F use) {
    if (kind == 0) {
        Rectangle r(a, b);
        return use(r);
    }
    if (kind == 1) {
        Square s(a);
        return use(s);
    }
    Triangle t(a, b);
    return use(t);
}

}  // namespace

extern "C" {

// ---- Fraction --------------------------------------------------------------

void fraction_make(int num, int den, int *out_num, int *out_den) {
    unpack(Fraction(num, den), out_num, out_den);
}

// op 0: a + b, op 1: a - b, op 2: a * b
void fraction_op(int op, int an, int ad, int bn, int bd, int *out_num, int *out_den) {
    Fraction a(an, ad), b(bn, bd);
    unpack(op == 0 ? a + b : op == 1 ? a - b : a * b, out_num, out_den);
}

int fraction_equal(int an, int ad, int bn, int bd) {
    return Fraction(an, ad) == Fraction(bn, bd) ? 1 : 0;
}

int fraction_text(int num, int den, char *buf, int cap) {
    std::ostringstream os;
    os << Fraction(num, den);
    return write_text(os.str(), buf, cap);
}

// ---- Shapes ----------------------------------------------------------------

// Called on the object's own type: Rectangle::area(), Triangle::area(), ...
double shape_area(int kind, int a, int b) {
    return with_shape(kind, a, b, [](const auto &s) { return s.area(); });
}

// Called through a const Shape &: only reaches the right function when it is virtual.
double shape_area_via_base(int kind, int a, int b) {
    return with_shape(kind, a, b, [](const Shape &s) { return s.area(); });
}

int shape_name(int kind, int a, int b, char *buf, int cap) {
    return write_text(with_shape(kind, a, b, [](const auto &s) { return s.name(); }), buf, cap);
}

int shape_name_via_base(int kind, int a, int b, char *buf, int cap) {
    return write_text(with_shape(kind, a, b, [](const Shape &s) { return s.name(); }), buf, cap);
}

int shape_less(int k1, int a1, int b1, int k2, int a2, int b2) {
    return with_shape(k1, a1, b1, [&](const Shape &left) {
        return with_shape(k2, a2, b2, [&](const Shape &right) { return left < right ? 1 : 0; });
    });
}

int shape_text(int kind, int a, int b, char *buf, int cap) {
    std::ostringstream os;
    with_shape(kind, a, b, [&](const Shape &s) {
        os << s;
        return 0;
    });
    return write_text(os.str(), buf, cap);
}

void square_sides(int side, int *width, int *height) {
    Square s(side);
    *width = s.getWidth();
    *height = s.getHeight();
}

}  // extern "C"
