from cfb import *
from rc6 import *

if __name__ == '__main__':
    # file for encoding and decoding result
    f_enc = open("encoded_file", "w")
    f_dec = open("decoded_file", "w")
    # getting encryption key from user input
    user_key = get_key(RC6_KEY_BYTES_SIZE)
    # splitting original file into blocks of fixed size, which will be encoded
    file_blocks = split_bin_file_to_blocks("original_file", CFB_BYTES_BLOCK_SIZE)
    # starting encryption with cipher feedback mode
    IV, encrypted = cfb_cipher_mode_encrypt(file_blocks, user_key)
    print("Encrypted successfully, see encoded_file")
    f_enc.write(encrypted)
    decrypted = cfb_cipher_mode_decrypt(encrypted, user_key, IV)
    print("Decrypted successfully, see decoded_file")
    f_dec.write(decrypted)
