import argparse
import sys


def encrypt(plaintext, key, blocksize):
    columns = len(key) # Number of columns in the table

    sorted_key = sorted([(char, i) for i, char in enumerate(key)]) # Sort the key and store the index of each character

    blocks = [plaintext[i: i + blocksize] for i in range(0, len(plaintext), blocksize)] # Break the plaintext into blocks

    ciphertext = bytearray()
    for block in blocks:
        table = [bytearray() for _ in range(columns)] # Create a table with a column for each character in the key
        for i, byte in enumerate(block):
            table[i % columns].append(byte)  # Append the byte to the appropriate column

        for _, index in sorted_key: # Append the bytes from the table to the ciphertext according to the sorted key sequence
            ciphertext.extend(table[index]) # Append the bytes from the table to the ciphertext

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


if __name__ == '__main__':
    main()