#!/usr/bin/python3

import sys

BLOCK_SIZE = 16


def pseudo_random_generator(seed, a=1103515245, c=12345, m=256):
    while True:
        seed = (a * seed + c) % m
        yield seed


def sdbm(key):
    hash_value = 0
    for char in key:
        hash_value = char + (hash_value << 6) + (hash_value << 16) - hash_value
        hash_value &= 0xFFFFFFFFFFFFFFFF
    return hash_value


def shuffle_block(block, key):  # Shuffle the block using the key
    for i in range(BLOCK_SIZE):
        first = key[i] & 0xf
        second = (key[i] >> 4) & 0xf
        block[first], block[second] = block[second], block[first]  # Swap the elements at the first and second indices
    return block


def pad_block(block):
    padding_size = BLOCK_SIZE - len(block) # Calculate the padding size by subtracting the length of the block from the block size
    return block + bytes([padding_size] * padding_size) # Append the padding size to the block


def encrypt_block(block, prng, previous_block):
    keystream = bytes([next(prng) for _ in range(BLOCK_SIZE)]) # Generate a 16-byte key from the PRNG
    block = bytes(a ^ b for a, b in zip(block, previous_block)) # Apply XOR with the previous block
    shuffled_block = shuffle_block(list(block), keystream) # Shuffle the block with the 16-byte key

    return bytes(a ^ b for a, b in zip(shuffled_block, keystream)) # Apply XOR with the 16-byte key


def sbencrypt(password, plaintext_path, ciphertext_path):
    seed = sdbm(password.encode()) # Convert the password to bytes and hash it
    prng = pseudo_random_generator(seed) # Create a pseudo-random number generator with the hash as the seed
    iv = bytes([next(prng) for _ in range(BLOCK_SIZE)]) # Generate a 16-byte IV from the PRNG

    with open(plaintext_path, 'rb') as plaintext_file, open(ciphertext_path, 'wb') as ciphertext_file:
        previous_block = iv
        while True:
            block = plaintext_file.read(BLOCK_SIZE)
            if len(block) < BLOCK_SIZE:
                block = pad_block(block) # Pad the block if it is less than 16 bytes
                ciphertext_block = encrypt_block(block, prng, previous_block) # Encrypt the block
                ciphertext_file.write(ciphertext_block) # Write the ciphertext block to the output file
                break

            ciphertext_block = encrypt_block(block, prng, previous_block) # Encrypt the block
            ciphertext_file.write(ciphertext_block) # Write the ciphertext block to the output file
            previous_block = ciphertext_block # Set the previous block to the current ciphertext block


def main():
    if len(sys.argv) != 4:
        print("Usage: sbencrypt password plaintext ciphertext")
        sys.exit(1)

    _, password, plaintext_path, ciphertext_path = sys.argv
    sbencrypt(password, plaintext_path, ciphertext_path)


if __name__ == "__main__":
    main()
