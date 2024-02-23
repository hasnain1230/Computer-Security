#!/usr/bin/python3

import argparse
import sys


def create_table(rows, columns, extra_cols):
    table = [
        [b''] * columns for _ in range(rows + (1 if extra_cols else 0))
    ]

    return table


def decrypt(ciphertext, key, blocksize):
    columns = len(key) # Number of columns in the table
    sorted_key = sorted([(char, i) for i, char in enumerate(key)]) # Sort the key and store the index of each character

    blocks = [ciphertext[i: i + blocksize] for i in
              range(0, len(ciphertext), blocksize)]  # Split the ciphertext into blocks

    plaintext = bytearray()

    for block in blocks:
        if len(block) < blocksize:
            rows = len(block) // columns
            extra_cols = len(block) % columns
        else:
            rows = blocksize // columns
            extra_cols = blocksize % columns

        table = create_table(rows, columns, extra_cols)

        # Fill the table column-wise according to the sorted key sequence
        count = 0

        for character, index in sorted_key:
            for i in range(rows + (1 if index < extra_cols else 0)):
                if count < len(block):
                    table[i][index] = block[count:count+1]
                    count += 1

        for row in table:
            plaintext.extend(b''.join(row))

    return plaintext


def check_blocksize(blocksize):
    blocksize = int(blocksize)
    if blocksize < 1:
        raise argparse.ArgumentTypeError('Block size must be at least 1')
    return blocksize


def main():
    parser = argparse.ArgumentParser(prog='ctdecrypt',
                                     description='Pad-free Columnar Transposition Cipher Decryption for binary files')
    parser.add_argument('-b', '--blocksize', type=check_blocksize, default=16, help='Block size for the cipher')
    parser.add_argument('-k', '--key', required=True, help='Key for the cipher')
    parser.add_argument('ciphertext_file', nargs='?', help='File to decrypt', default=sys.stdin.buffer, type=argparse.FileType('rb'))

    args = parser.parse_args()

    if args.ciphertext_file == sys.stdin.buffer:
        ciphertext = sys.stdin.buffer.read()
    else:
        ciphertext = args.ciphertext_file.read()

    plaintext = decrypt(ciphertext, args.key, args.blocksize)

    # Output the plaintext as binary
    sys.stdout.buffer.write(plaintext)


if __name__ == '__main__':
    main()
