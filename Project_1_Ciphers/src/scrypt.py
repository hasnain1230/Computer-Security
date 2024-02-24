#!/usr/bin/python3

import sys


def pseudo_random_generator(seed, a=1103515245, c=12345, m=256): # Generator function for a pseudo-random number generator
    while True:
        seed = (a * seed + c) % m
        yield seed


def sdbm(key):
    hash_value = 0
    for char in key:
        hash_value = char + (hash_value << 6) + (hash_value << 16) - hash_value
        hash_value &= 0xFFFFFFFFFFFFFFFF
    return hash_value


def process_file(input_path, output_path, password):
    seed = sdbm(password.encode()) # Convert the password to bytes and hash it
    prng = pseudo_random_generator(seed) # Create a pseudo-random number generator with the hash as the seed

    print(f'using seed={seed} from password="{password}"')

    with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file: # Open the input and output files in binary mode
        while byte := input_file.read(1): # Read the input file one byte at a time
            output_file.write(bytes([byte[0] ^ next(prng)]))


def main():
    if len(sys.argv) != 4:
        print("Usage:")
        print("scrypt password plaintext ciphertext")
        print("scrypt password ciphertext plaintext")
        sys.exit(1)

    _, password, input_path, output_path = sys.argv
    process_file(input_path, output_path, password)


if __name__ == "__main__":
    main()