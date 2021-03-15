from point import Point


class EncodingResult:

    # encoding result is {kG, Pm + kPb}, so it is represented as two points
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    # printing result
    def __str__(self):
        return "{{({0},{1}),({2},{3})}};".format(self.p1.x, self.p1.y, self.p2.x, self.p2.y)
