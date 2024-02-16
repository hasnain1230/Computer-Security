#!/usr/bin/python3

import argparse
import sys


def encrypt(plaintext, key, blocksize):
    # Determine the number of columns from the length of the key
    columns = len(key)

    # Sort the key to determine the reading sequence
    sorted_key = sorted([(char, i) for i, char in enumerate(key)])

    blocks = [plaintext[i: i + blocksize] for i in range(0, len(plaintext), blocksize)]

    # Encrypt each block
    ciphertext = ""
    for block in blocks:
        # Create the table
        table = [''] * columns
        for i, char in enumerate(block):
            col = i % columns
            table[col] += char

        # Read the table column-wise according to the sorted key sequence
        for _, index in sorted_key:
            ciphertext += table[index]

    return ciphertext


def main():
    parser = argparse.ArgumentParser(prog='ctencrypt',
                                     description='Pad-free Columnar Transposition Cipher Encryption')
    # Add an optional -b or --blocksize argument
    parser.add_argument('-b', '--blocksize', type=int, default=16, help='Block size for the cipher')
    # Add a required -k or --key argument
    parser.add_argument('-k', '--key', required=True, help='Key for the cipher')
    # Add an optional plaintext argument-- if not provided, read from stdin
    parser.add_argument('plaintext', nargs='?', help='File to encrypt ; leave empty to read file from stdin',
                        default=sys.stdin, type=argparse.FileType('r'))

    args = parser.parse_args()

    if args.plaintext == sys.stdin:
        plaintext = sys.stdin.read()
    else:
        plaintext = args.plaintext.read()

    ciphertext = encrypt(plaintext, args.key, args.blocksize)

    print(ciphertext)


if __name__ == '__main__':
    main()
