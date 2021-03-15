import sympy
from point import Point


# function to get P1(x,y) + P2(x,y) on elliptic curves
def elliptic_curve_sum(e_curve, p1, p2):
    lam = 0  # lambda - slope of the line through two points
    if p1 == p2:
        # p1 and p2 are the same point
        lam = (3 * pow(p1.x, 2) + e_curve.a) * sympy.mod_inverse(2 * p1.y, e_curve.p)
    else:
        # p1 and p2 are different
        lam = (p2.y - p1.y) * sympy.mod_inverse(p2.x - p1.x, e_curve.p)
    # finding resulting point
    x_res = (pow(lam, 2) - p1.x - p2.x) % e_curve.p
    y_res = (lam * (p1.x - x_res) - p1.y) % e_curve.p
    # returning resulting point
    res_point = Point(x_res, y_res)
    return res_point

