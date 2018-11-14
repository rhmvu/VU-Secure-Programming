#!/usr/bin/env python

# Name: Ruben van der Ham
# VU net id: rhm270
# Student number: 2592271
# Email: 2592271@student.vu.nl

from __future__ import print_function
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import  PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Signature import PKCS1_v1_5 as SignatureCipher
from base64 import b64decode,b64encode
import sys , os, struct


HELP_MESSAGE = """Vault implementation by Ruben van der Ham\n
Signing usage: vault.py <mode> <path-to-file> <path-to-public-key> <path-to-signature>
Encryption usage: vault.py <mode> <path-to-file> <password> <iv>
mode:
\t -s: Signs file hash with private key
\t -v: Verifies encrypted filehash with public key (needs path to signature arg)

\t -e: Encrypts file with password and iv
\t -d: Decrypts file with password and iv

\t -h: displays this help message   """

FAILURE_MESSAGE = "Error occurred: {}\n\nFor help information run 'python vault.py -h'"

AES_BLOCKSIZE = 32 #32 bytes == 128 bits


def parse_args():
    # Check for parameters
    argc = len(sys.argv)
    if argc == 1:
        raise Exception("Not enough parameters")
    mode = {
        "-s": sign_file,
        "-v": verify_signature,
        "-e": encrypt_file,
        "-d": decrypt_file,
        "-h": print_help
    }
    if argc < 4 and sys.argv[1] != "-h":
        raise Exception("Not enough parameters")
    if argc > 5 and sys.argv[1] != "-h":
        raise Exception("Too much parameters")
    try:
        return mode[sys.argv[1]]
    except ValueError:
        raise Exception('Mode not found')


def print_fail(exception):
    fail_message = "Unknown error"
    if exception:
        fail_message = str(exception)
    return str.format(FAILURE_MESSAGE, fail_message)


def print_help():
    print(HELP_MESSAGE)


def read_contents(filepath):
    with open(filepath, "r") as f:
        return f.read()


def sha256_file(file_path):
    bin_file = read_contents(file_path)
    sha = SHA256.new()
    sha.update(bin_file)
    return sha


def sign_file(file_path, privkey_path):
    str_privkey = read_contents(privkey_path)

    key_priv = RSA.importKey(str_privkey)
    sha = sha256_file(file_path)
    cipher = SignatureCipher.new(key_priv)
    cipher_text = cipher.sign(sha)

    print(b64encode(str(cipher_text)))


def verify_signature(file_path,pubkey_path, sig_path):
    str_pubkey = read_contents(pubkey_path)
    encoded_sig = read_contents(sig_path)

    key_pub = RSA.importKey(str_pubkey)
    encrypted_sig = b64decode(encoded_sig)
    sha = sha256_file(file_path)
    cipher = SignatureCipher.new(key_pub)

    if cipher.verify(sha, encrypted_sig):
        exit(0)
    else:
        exit(1)

def encrypt_file(file_path, password,iv):


    # get iv and pad to 16 bytes if necessary
    bytes_iv = bytearray.fromhex(iv).zfill(16)
    # convert password to 32 bytes, 256 bit key
    bytes_password = bytearray.fromhex(password).zfill(32)
    file_size = os.path.getsize(file_path)

    aes = AES.new(bytes(bytes_password), AES.MODE_CBC, bytes(bytes_iv))

    with open(file_path, "r") as file:
        while file_size >= 16:
            block = file.read(16)
            file_size -= 16
            print(aes.encrypt(block), end="")

        # apply padding to last block if needed
        if 0 < file_size < 16:
            block = bytearray(file.read(file_size))
            for i in range(0, (16 - file_size)):
                block.append(int(16 - file_size))
            print(aes.encrypt(bytes(block)), end="")


def decrypt_file(file_path, password,iv):
    # get iv and pad to 16 bytes if necessary
    bytes_iv = bytearray.fromhex(iv).zfill(16)
    # convert password to 32 bytes, 256 bit key
    bytes_password = bytearray.fromhex(password).zfill(32)

    file_size = os.path.getsize(file_path)
    if file_size == 0:
        raise Exception("File empty")
        exit(1)

    aes = AES.new(bytes(bytes_password), AES.MODE_CBC, bytes(bytes_iv))

    with open(file_path, "r") as file:
        while file_size > 16:
            block = file.read(16)
            file_size -= 16
            print(aes.decrypt(block),end="")

        # read last block and check for padding:
        block = file.read(file_size)
        decrypted_block = aes.decrypt(block)
        try:
            # try to grab last char/byte as decimal
            last_byte = ord(bytes(decrypted_block[file_size-1]))
            # Compare all padding bytes to their expected value
            if 0 < last_byte < file_size:
                start_padding_bytes = file_size-last_byte
                for i in range(start_padding_bytes, file_size):
                    if ord(decrypted_block[i]) != last_byte:
                        print(decrypted_block,end="")
                        return
        except ValueError as e:
            print(e)
            # not parsable as decimal, thus no padding
            print(decrypted_block,end="")
            return

        print(decrypted_block[:start_padding_bytes],end="")


def main():
    try:
        func = parse_args()
    except Exception as e:
        print(print_fail(e))
        exit(1)

    # run the function/mode
    try:
        if func == print_help:
            func()
        elif func == sign_file:
            func(sys.argv[2], sys.argv[3])
        else:
            func(sys.argv[2], sys.argv[3], sys.argv[4])
    except Exception as e:
       print(print_fail(e))
       exit(1)


if __name__ == '__main__':
    main()