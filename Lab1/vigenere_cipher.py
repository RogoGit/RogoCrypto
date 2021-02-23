
# getting encryption keys set from stdin
def get_keys():
    keys = []
    while True:
        key_num = input("Enter keys num:")
        if key_num.isalpha() or int(key_num) < 1:
            print("Must have at least one key, key num must be numeric")
        else:
            break
    for i in range(int(key_num)):
        key = input("Key {0}:".format(i+1))
        keys.append(key)
    return keys


# as alphabet we use ASCII table
def create_alphabet_dict():
    return {i: chr(i) for i in range(128)}


# turn word into list of alphabet symbols indexes
def split_into_separate_codes(word, alphabet):
    codes_list = []
    for word_letter in word:
        for ascii_num, ascii_letter in alphabet.items():
            if ascii_letter == word_letter:
                codes_list.append(ascii_num)
    return codes_list


# getting looped key to fit msg
def get_looped_key(key, length):
    if len(key) == length:
        return key
    if len(key) > length:
        return key[0:length]
    return (key * (int(length / len(key)) + 1))[:length]


# after we gets encoded letters codes, we convert it to string
def get_string_from_codes(codes_list):
    return ''.join(chr(i) for i in codes_list)


# encoding function
def encode(msg, keys):
    alphabet = create_alphabet_dict()   # create alphabet (ascii)
    msg_codes_list = split_into_separate_codes(msg, alphabet)
    looped_keys = [get_looped_key(key, len(msg_codes_list)) for key in keys]
    looped_keys_codes = [split_into_separate_codes(looped_key, alphabet) for looped_key in looped_keys]

    encrypted_text_codes = []
    for i in range(len(msg_codes_list)):
        keys_codes_sum = 0
        for keys_codes_list in looped_keys_codes:
            keys_codes_sum = keys_codes_sum + keys_codes_list[i]
        encrypted_text_codes.append((msg_codes_list[i] + keys_codes_sum) % len(alphabet))

    print("Encrypted successfully")
    return get_string_from_codes(encrypted_text_codes)


# decoding function
def decode(encoded, keys):
    alphabet = create_alphabet_dict()   # create alphabet (ascii)
    encrypted_codes_list = split_into_separate_codes(encoded, alphabet)
    looped_keys = [get_looped_key(key, len(encrypted_codes_list)) for key in keys]
    looped_keys_codes = [split_into_separate_codes(looped_key, alphabet) for looped_key in looped_keys]

    decoded_text_codes = []
    for i in range(len(encrypted_codes_list)):
        keys_codes_sum = 0
        for keys_codes_list in looped_keys_codes:
            keys_codes_sum = keys_codes_sum + keys_codes_list[i]
        decoded_text_codes.append((encrypted_codes_list[i] - keys_codes_sum + len(alphabet)) % len(alphabet))

    print("Decrypted successfully")
    return get_string_from_codes(decoded_text_codes)


if __name__ == '__main__':
    f_orig = open("original_file", "r")
    f_enc = open("encoded_file", "w")
    f_dec = open("decoded_file", "w")
    given_keys = get_keys()
    encoded_data = encode(f_orig.read(), given_keys)
    f_enc.write(encoded_data)
    decoded = decode(encoded_data, given_keys)
    f_dec.write(decoded)

    f_dec.close()
    f_enc.close()
    f_orig.close()
