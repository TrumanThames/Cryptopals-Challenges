import os
import sys


def hexor(hex_str0, hex_str1):
    b_str0 = int(hex_str0, 16)
    b_str1 = int(hex_str1, 16)
    x_str = b_str0 ^ b_str1
    h_str = hex(x_str)
    print(h_str[2:])
    return(h_str[2:])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Abort Abort, there are children on board!!!!!!")
        sys.exit()
    hex_str0 = sys.argv[1]
    hex_str1 = sys.argv[2]

    if (len(hex_str0) != len(hex_str1)):
        print("Abort abort!!")
        sys.exit()

    hexor(hex_str0, hex_str1)
