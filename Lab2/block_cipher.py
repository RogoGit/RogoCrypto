from cfb import *
from rc6 import *

if __name__ == '__main__':
    # getting encryption key from user input
    user_key = get_key(RC6_KEY_BYTES_SIZE)
    # splitting original file into blocks of fixed size, which will be encoded
    file_blocks = split_bin_file_to_blocks("original_file", CFB_BYTES_BLOCK_SIZE)
    # starting encryption with cipher feedback mode
    IV, encrypted = cfb_cipher_mode_encrypt(file_blocks, user_key)
    cfb_cipher_mode_decrypt(encrypted, user_key, IV)
