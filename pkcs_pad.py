import sys

def pad(t, size=16):
    #takes t as a bytearray
    l = len(t)
    a = l % (size)
    if a == 0:
        return t
    return t+(chr(size-a)*(size-a)).encode()

if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        print("need at least one argument, the bytes to be padded")
        print("optional second argument, the block size to pad to")
        sys.exit()
    text = sys.argv[1]
    if (len(sys.argv) >=3):
        block_size = int(sys.argv[2])
    else:
        block_size = 16
    ptext = pad(text.encode(), block_size)
    print(ptext)
