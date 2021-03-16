from point import Point
from curve import Curve
from encoding_result import EncodingResult
from elliptic_curve_arithm import elliptic_curve_sum, elliptic_curve_point_inversion


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


# decoding cipher with elliptic curve and secret key (nb)
def decode(cipher_text, nb, curve):
    for encoded_symbol_num in range(0, len(cipher_text)):
        left_part = cipher_text[encoded_symbol_num].p1  # kG of ciphered symbol
        right_part = cipher_text[encoded_symbol_num].p2  # Pm + kPb of ciphered symbol
        # we decode as (Pm+kPb)-nb(kG), but -nb(kG) can be represented as nb(-kG),
        # so we find -kG
        inverse_left_part = elliptic_curve_point_inversion(curve, left_part)
        neg_nb_kg = inverse_left_part   # our -nb*(kG) = nb(-kG)
        for i in range(0, nb-1):
            neg_nb_kg = elliptic_curve_sum(curve, neg_nb_kg, inverse_left_part)
        # finding result as (Pm+kPb) + nb(-kG)
        decoded = elliptic_curve_sum(curve, right_part, neg_nb_kg)
        print(decoded)


# main func
if __name__ == '__main__':
    e_curve = Curve(-1, 1, 751)  # according to task we use y^2 = x^3 - x + 1 (mod 751),
    gen_point = Point(0, 1)  # point we use to start generation
    # encoding
    '''
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
    '''
    # decoding
    secret_key = 32  # secret key nb
    # cipher text we have to decode - represented as two points for symbol
    encoded_letters = [
        EncodingResult(Point(188, 93), Point(623, 166)),
        EncodingResult(Point(725, 195), Point(513, 414)),
        EncodingResult(Point(346, 242), Point(461, 4)),
        EncodingResult(Point(489, 468), Point(739, 574)),
        EncodingResult(Point(725, 195), Point(663, 476)),
        EncodingResult(Point(745, 210), Point(724, 522)),
        EncodingResult(Point(725, 195), Point(663, 476)),
        EncodingResult(Point(618, 206), Point(438, 40)),
        EncodingResult(Point(286, 136), Point(546, 670)),
        EncodingResult(Point(179, 275), Point(73, 72))
    ]
    decode(encoded_letters, secret_key, e_curve)
