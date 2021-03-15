class Curve:

    # the curve equation is as follows: y^2 = x^3 + ax + b (mod p),
    # so we have to fill a, b, p parameters to create elliptic curve
    def __init__(self, a, b, p):
        self.a = a
        self.b = b,
        self.p = p
