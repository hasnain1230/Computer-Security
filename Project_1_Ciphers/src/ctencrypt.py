#!/usr/bin/python3

import argparse
import sys


def encrypt(plaintext, key, blocksize):
    columns = len(key)
    sorted_key = sorted([(char, i) for i, char in enumerate(key.encode())])

    blocks = [plaintext[i: i + blocksize] for i in range(0, len(plaintext), blocksize)]

    ciphertext = bytearray()
    for block in blocks:
        table = [bytearray() for _ in range(columns)]
        for i, byte in enumerate(block):
            table[i % columns].append(byte)

        for _, index in sorted_key:
            ciphertext.extend(table[index])

    return ciphertext


def check_blocksize(blocksize):
    blocksize = int(blocksize)
    if blocksize < 1:
        raise argparse.ArgumentTypeError('Block size must be at least 1')
    return blocksize


def main():
    parser = argparse.ArgumentParser(prog='ctencrypt',
                                     description='Pad-free Columnar Transposition Cipher Encryption for binary files')
    parser.add_argument('-b', '--blocksize', type=check_blocksize, default=16, help='Block size for the cipher')
    parser.add_argument('-k', '--key', required=True, help='Key for the cipher')
    parser.add_argument('input_file', nargs='?', help='File to encrypt', default=sys.stdin.buffer,
                        type=argparse.FileType('rb'))

    args = parser.parse_args()

    if args.input_file == sys.stdin.buffer:
        plaintext = sys.stdin.buffer.read()
    else:
        plaintext = args.input_file.read()

    ciphertext = encrypt(plaintext, args.key, args.blocksize)

    # Output the ciphertext as binary
    sys.stdout.buffer.write(ciphertext)

# TODO: Hasnain, please review this code and make sure you understand how it works.

if __name__ == '__main__':
    main()