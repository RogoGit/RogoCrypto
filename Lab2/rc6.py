import textwrap
import math
from consts import *
from helpers import *


# function to gen key S[0 ... 2r+3] from given user input key
# typed key must be RC6_KEY_BYTES_SIZE long
def generate_key_table(typed_key, key_size, reg_size):
    w = int(key_size / 4 * 8)  # key size in bits
    mod = 2 ** w    # reg size, will % with this value
    # creating L[0..c-1] from key
    u = reg_size / 8
    c = key_size / u
    L = []
    L_bin = split_bin_to_parts(''.join(format(ord(i), 'b').zfill(8) for i in typed_key), int(key_size), int(c/8))
    # print("L_bin: " + str(L_bin))
    for el in L_bin:
        el = int(el, 2)     # converting to decimal
        L.append(el)
    L.reverse()
    # print("L: " + str(L))
    # extended key table initialization
    S = (2 * RC6_ROUNDS_NUM + 4) * [0]
    p_w = P_32
    q_w = Q_32
    S[0] = p_w
    for i in range(1, 2 * RC6_ROUNDS_NUM + 4):
        S[i] = (S[i - 1] + q_w) % mod
    # key mixing
    A = B = i = j = 0
    v = 3 * max(c / 8, 2 * RC6_ROUNDS_NUM + 4)
    for index in range(0, v):
        A = S[i] = rol((S[i] + A + B) % mod, 3, reg_size * 8)
        B = L[int(j)] = rol((L[int(j)] + A + B) % mod, (A + B) % (reg_size * 8), (reg_size * 8))
        i = (i + 1) % (2 * RC6_ROUNDS_NUM + 4)
        j = (j + 1) % (c / 8)
    # returning extended key table
    # print("S: " + str(S))
    return S


# main rc6 encoding func - getting block and return encoded block
# S[0... 2r+3] - key tables
def rc6_block_encrypt(block, block_size_bytes, S):
    # splitting block to 4 equal parts for A, B, C, D reg
    block_parts = split_bin_to_parts(block, block_size_bytes, 4)
    A = int(block_parts[0], 2)
    B = int(block_parts[1], 2)
    C = int(block_parts[2], 2)
    D = int(block_parts[3], 2)
    # starting cipher
    w = int(block_size_bytes / 4 * 8)   # reg size in bits
    mod = 2 ** w
    log_w = int(math.log2(w))
    B = (B + S[0]) % mod
    D = (D + S[1]) % mod

    for i in range(1, RC6_ROUNDS_NUM + 1):
        t = rol((B * (2 * B + 1)) % mod, log_w, w)
        u = rol((D * (2 * D + 1)) % mod, log_w, w)
        A = (rol(A ^ t, u % w, w) + S[2 * i]) % mod
        C = (rol(C ^ u, t % w, w) + S[2 * i + 1]) % mod
        (A, B, C, D) = (B, C, D, A)

    A = (A + S[2 * RC6_ROUNDS_NUM + 2]) % mod
    C = (C + S[2 * RC6_ROUNDS_NUM + 3]) % mod

    # returning cipher
    encoded = [A, B, C, D]
    # print("ENC REG:" + str(encoded))
    return get_string_from_rc6_bin(encoded, w)


# main rc6 decoding func - getting block and return decoded block
# S[0... 2r+3] - key tables
def rc6_block_decrypt(block_parts, block_size_bytes, S):
    print(block_parts)
    A = int(block_parts[0], 2)
    B = int(block_parts[1], 2)
    C = int(block_parts[2], 2)
    D = int(block_parts[3], 2)
    # starting decryption
    w = int(block_size_bytes / 4 * 8)  # reg size in bits
    log_w = int(math.log2(w))
    mod = 2 ** w
    C = (C - S[2 * RC6_ROUNDS_NUM + 3]) % mod
    A = (A - S[2 * RC6_ROUNDS_NUM + 2]) % mod
    for j in range(1, RC6_ROUNDS_NUM + 1):
        i = RC6_ROUNDS_NUM + 1 - j
        (A, B, C, D) = (D, A, B, C)
        u = rol((D * (2 * D + 1)) % mod, log_w, w)
        t = rol((B * (2 * B + 1)) % mod, log_w, w)
        C = ror((C - S[2 * i + 1]) % mod, t % w, w) ^ u
        A = ror((A - S[2 * i]) % mod, u % w, w) ^ t
    D = (D - S[1]) % mod
    B = (B - S[0]) % mod

    # return decrypted
    decoded = [A, B, C, D]
    print("DEC REG:" + str(decoded))
    return get_string_from_rc6_bin(decoded, w)


