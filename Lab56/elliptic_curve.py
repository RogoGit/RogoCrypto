from point import Point
from curve import Curve
from encoding_result import EncodingResult
from elliptic_curve_arithm import elliptic_curve_sum


# encoding word with elliptic curve with given key, gen point and random k numbers
def encode(word, curve, g_point, key, k_list):
    for symbol_point_num in range(0, len(word)):
        k = k_list[symbol_point_num]
        # creating points for encoding result
        encoded_p1 = g_point
        encoded_p2 = key
        # calculating k * G
        for i in range(0, k-1):
            encoded_p1 = elliptic_curve_sum(curve, encoded_p1, g_point)
        # calculating Pm + kPb
        for i in range(0, k-1):
            encoded_p2 = elliptic_curve_sum(curve, encoded_p2, key)
        encoded_p2 = elliptic_curve_sum(curve, word[symbol_point_num], encoded_p2)
        # getting final encoded point
        encoded = EncodingResult(encoded_p1, encoded_p2)
        print(encoded)


# main func
if __name__ == '__main__':
    e_curve = Curve(-1, 1, 751)  # according to task we use y^2 = x^3 - x + 1 (mod 751),
    gen_point = Point(0, 1)  # point we use to start generation
    k_values = [2, 19, 4, 8, 2, 2, 16, 10, 2]  # random k values for letters encoding
    open_key = Point(725, 195)  # according to task key is P(725,195)
    # word to encode is 'ренессанс'
    letters = [
        Point(243, 87),  # р
        Point(234, 587),  # е
        Point(238, 576),  # н
        Point(234, 587),  # е
        Point(243, 664),  # с
        Point(243, 664),  # с
        Point(228, 271),  # а
        Point(238, 576),  # н
        Point(243, 664)  # с
    ]
    encode(letters, e_curve, gen_point, open_key, k_values)
