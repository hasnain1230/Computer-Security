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


def unshuffle_block(block, key): # Undoes the shuffle from the encryption
    for i in range(BLOCK_SIZE - 1, -1, -1):
        first = key[i] & 0xf
        second = (key[i] >> 4) & 0xf
        block[first], block[second] = block[second], block[first]
    return block


def remove_padding(block): # Removes the padding from the block
    padding_size = block[-1]
    return block[:-padding_size]


def decrypt_block(block, prng, previous_block): # Decrypts the block
    keystream = bytes([next(prng) for _ in range(BLOCK_SIZE)])
    block = bytes(a ^ b for a, b in zip(block, keystream))
    unshuffled_block = unshuffle_block(list(block), keystream)

    return bytes(a ^ b for a, b in zip(unshuffled_block, previous_block))


def sbdecrypt(password, ciphertext_path, plaintext_path):
    seed = sdbm(password.encode())
    prng = pseudo_random_generator(seed)
    iv = bytes([next(prng) for _ in range(BLOCK_SIZE)])

    with open(ciphertext_path, 'rb') as ciphertext_file, open(plaintext_path, 'wb') as plaintext_file:
        previous_block = iv
        final_block = None

        while True:
            block = ciphertext_file.read(BLOCK_SIZE)
            if not block:
                if final_block:
                    plaintext_file.write(remove_padding(final_block))
                break

            decrypted_block = decrypt_block(block, prng, previous_block)
            if final_block:
                plaintext_file.write(final_block)

            previous_block = block
            final_block = decrypted_block


def main():
    if len(sys.argv) != 4:
        print("Usage: sbdecrypt password ciphertext plaintext")
        sys.exit(1)

    _, password, ciphertext_path, plaintext_path = sys.argv
    sbdecrypt(password, ciphertext_path, plaintext_path)


if __name__ == "__main__":
    main()
