import textwrap


# arg - block as string (like '111000000111...')
# ret - list of equal blocks from given block
def split_bin_to_parts(block, block_size, parts_num):    # block_size * 8 = block size in bits
    if len(block) < block_size * 8 / parts_num:
        return [block]
    return textwrap.wrap(block, int(block_size * 8 / parts_num))    # splitting into 4 equal parts (block_size / 4)


# creating string with binary representation of block
def get_block_binary_representation(block):
    res = ""
    for byte in block:
        # in binary representation num of 0 and 1 must always be the same, so use 08b to show exactly 8 digits
        res += str(format(int(byte), "08b"))
    return res


# in - rc6 registers list, out - string (encryption result)
def get_string_from_rc6_bin(reg_list, block_bit_size):
    res = ""
    for value in reg_list:
        bin_value = bin(value)[2:]   # deleting 0b prefix
        if len(bin_value) < block_bit_size:
            bin_value = "0" * (block_bit_size - len(bin_value)) + bin_value
        for i in range(0, 4):   # we splitting to 4 parts, because we have 4 regs in RC6
            res = res + chr(int(bin_value[i * int(block_bit_size / 4):(i + 1) * int(block_bit_size / 4)], 2))
    return res


# creating char string from strings like "001110011"
def convert_one_and_zeros_to_str(string):
    characters_list = textwrap.wrap(string, 8)
    res = ""
    for ch in characters_list:
        res += chr(int(ch, 2))
    return res


# convert input text into blocks of binary
# split to given number of blocks
def string_to_bin_blocks(text, blocks_num):
    bit_string = ""
    for ch in text:
        bit_string += str(format(ord(ch), "08b"))
    return split_bin_to_parts(bit_string, int(len(bit_string) / 8), blocks_num)


# creating list of fixed size blocks from file to encode
# return - list of binary blocks as strings
def split_bin_file_to_blocks(file_name, block_size):
    blocks_list = []
    file = open(file_name, "rb")
    block = file.read(block_size)
    blocks_list.append(get_block_binary_representation(block))
    while block:  # loop until the chunk is empty
        block = file.read(block_size)  # read the next chunk
        if not block:
            break
        blocks_list.append(get_block_binary_representation(block))
    file.close()
    # the last chunk may not have right size, so we add zeroes to fit block size
    block_size_bits = block_size * 8
    if len(blocks_list[-1]) < block_size_bits:
        blocks_list[-1] += str("0" * int((block_size_bits - len(blocks_list[-1]))))
    # getting blocks like '111011001..', the last one may not be block size length
    return blocks_list


# rotate right x (int), by n bits
def ror(x, n, reg_size):
    x = int(x)
    n = int(n)
    reg_size = int(reg_size)
    mask = (2 ** n) - 1    # mask to get lower bits to rotate
    masked_bits = x & mask
    return (x >> n) | (masked_bits << (reg_size - n))


# rotate left x (int), by n bits
def rol(x, n, reg_size):
    return ror(x, reg_size - n, reg_size)


# getting encryption key from stdin
def get_key(key_size):
    key = input("Enter key:")
    # we want the key to fit exact size, so we append spaces to the end until get required size in bytes
    key = (key + " " * (key_size - len(key)))[:key_size]
    return key
