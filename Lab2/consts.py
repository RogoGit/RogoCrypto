BYTES_BLOCK_SIZE = 16     # bytes of block to cipher
W_REG_BYTES_SIZE = BYTES_BLOCK_SIZE / 4     # size of A, B, C, D registers of RC6 algo
RC6_ROUNDS_NUM = 20     # how many rounds of encryption we use in rc6
RC6_KEY_BYTES_SIZE = 16     # size of RC6 user key in byte
P_32 = 0xB7E15163   # commonly used P constant value for rc6 with W_REG = 32 bits
Q_32 = 0x9E3779B9   # commonly used Q constant value for rc6 with W_REG = 32 bits
CFB_BYTES_BLOCK_SIZE = 1     # bytes of CFB block (j value)
