class Point:

    # class representing point on elliptic curve with coordinates
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # checking if two points are the same point
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # printing point
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)
