from __future__ import print_function
from playcrypto import encrypt, decrypt
import sys

HELP_MESSAGE = """Playfair implementation by Ruben van der Ham, 2592271\n
Usage: playfair.py [mode] key [plaintext/ciphertext]
mode:
\t -e: encrypts plaintext by the specified key
\t -d: decrypts ciphertext by the specified key
\t -h: displays this help message   """

FAILURE_MESSAGE = "Error occured: {}\n\nFor help information run 'python playfair.py -h'"

def parse_args():
    #Check for parameters
    argc = len(sys.argv)
    if argc < 4 and sys.argv[1] != "-h":
        raise Exception("Not enough parameters")
    if argc > 4 and sys.argv[1] != "-h":
        raise Exception("Too much parameters")
    mode = {
        "-e":encrypt,
        "-d":decrypt,
        "-h":return_help
    }
    try:
        return mode[sys.argv[1]]
    except ValueError:
        raise Exception('Mode not found')


def print_fail(exception):
    fail_message = "Unknown error"
    if(exception):
        fail_message = str(exception)
    return str.format(FAILURE_MESSAGE,fail_message)

def return_help():
    return HELP_MESSAGE

def main():
    try:
        func = parse_args()
    except Exception as e:
        print(print_fail(e))
        exit(1)

    #run the function/mode
    if func == return_help:
        result = func()
    else:
        try:
            result = func(sys.argv[2],sys.argv[3])
        except Exception as e:
            print(print_fail(e))
            exit(1)

    print(result)



if __name__ == '__main__':
    main()