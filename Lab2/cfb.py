import random
from rc6 import *


# generate random initial vector for cfb, size must be in bits
def initial_vector_gen(size):
    return ''.join(random.SystemRandom().choice("0" + "1") for _ in range(size))


# main cfb encrypt function
def cfb_cipher_mode_encrypt(file_blocks, key):
    # creating random initial vector for encrypting
    IV = initial_vector_gen(BYTES_BLOCK_SIZE * 8)
    IV_orig = IV
    # generating rc6 key extension for block encryption
    key_table = generate_key_table(key, RC6_KEY_BYTES_SIZE, BYTES_BLOCK_SIZE / 4)
    # our plain open (not encrypted) text is a list of file chunks
    P = file_blocks
    # print(P)
    # chunks of encrypted
    C = [0] * len(file_blocks)
    # blocks in cbf have j size in bits, IV size is b
    j = CFB_BYTES_BLOCK_SIZE * 8
    b = BYTES_BLOCK_SIZE * 8
    # encryption
    for i in range(0, len(P)):
        encrypted_iv = rc6_block_encrypt(IV, BYTES_BLOCK_SIZE, key_table)
        # print("Encr_iv " + encrypted_iv)
        left_bits_iv = string_to_bin_blocks(encrypted_iv, int(b/j))[0]
        C[i] = int(P[i], 2) ^ int(left_bits_iv, 2)  # converting from "11000010" str to int
        # doing left shit, replacing last j bits with C[i]
        IV = int(IV, 2)
        IV = rol(IV, j, b)
        iv_bin = str(string_to_bin_blocks(convert_one_and_zeros_to_str(str(bin(IV))), 1)[0])
        c_bin = str(string_to_bin_blocks(convert_one_and_zeros_to_str(str(bin(C[i]))), 1)[0])
        iv_bin = iv_bin[:-j] + c_bin
        IV = iv_bin
    # print(C)
    final_msg = "".join(chr(i) for i in C)
    # print("ENCRYPTED_RES: " + final_msg + " " + str(len(final_msg)))
    return IV_orig, final_msg


# main cfb decryption function
def cfb_cipher_mode_decrypt(encrypted, key, IV_orig):
    # converting encrypted string to bin chunks
    enc_blocks = string_to_bin_blocks(encrypted, len(encrypted))
    IV = IV_orig
    # generating rc6 key extension for block encryption
    key_table = generate_key_table(key, RC6_KEY_BYTES_SIZE, BYTES_BLOCK_SIZE / 4)
    # our encrypted text is a list of chunks
    C = enc_blocks
    # chunks of plain text, which we need to decrypt
    P = [0] * len(enc_blocks)
    # blocks in cbf have j size in bits, IV size is b
    j = CFB_BYTES_BLOCK_SIZE * 8
    b = BYTES_BLOCK_SIZE * 8
    # encryption
    for i in range(0, len(C)):
        encrypted_iv = rc6_block_encrypt(IV, BYTES_BLOCK_SIZE, key_table)
        # print("Decr_iv " + encrypted_iv)
        left_bits_iv = string_to_bin_blocks(encrypted_iv, int(b/j))[0]
        P[i] = int(C[i], 2) ^ int(left_bits_iv, 2)  # converting from "11000010" str to int
        # doing left shit, replacing last j bits with C[i]
        IV = int(IV, 2)
        IV = rol(IV, j, b)
        iv_bin = str(string_to_bin_blocks(convert_one_and_zeros_to_str(str(bin(IV))), 1)[0])
        c_bin = str(string_to_bin_blocks(convert_one_and_zeros_to_str(str(bin(int(C[i], 2)))), 1)[0])
        iv_bin = iv_bin[:-j] + c_bin
        IV = iv_bin
    # print(P)
    final_msg = "".join(chr(i) for i in P)
    # print("DECRYPTED_RES: " + final_msg)
    return final_msg
