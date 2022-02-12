import random, sys
from cbc_decrypt import encrypt_cbc
from detect_ecb import score
from decrypt_aes_ecb import encrypt as encrypt_ecb
from brk_rxc import b64_to_bytes

def gen_bytes(size=16):
    i = random.randint(0,2**(size*8))
    return i.to_bytes(size, 'big')


def randbytes(low=5, hi=11):
    i = random.randint(low, hi)
    x = random.randint(0,2**(8*i))
    return x.to_bytes(i, 'big')


def encryption_oracle(text):
    #Appends some bytes to the beginning and end of txt
    #Encrypts randomly with either ecb or cbc with a random key and iv
    #text is expected to be a bytearray
    text = randbytes()+text+randbytes()
    key = gen_bytes(16)
    flip = random.randint(0,2)
    if flip:
        print("I chose: CBC")
        return encrypt_cbc(text, key, iv=gen_bytes(16))
    else:
        print("I chose: ECB")
        return encrypt_ecb(text, key)


def blist(ctext):
    return [i for i in ctext]


def is_ecb(ctext):
    #turning ctext into a list of bytes because I coded score when I was using that type
    byte_list_ctext = blist(ctext)
    sco = score(byte_list_ctext)
    #print("The score is: "+str(sco))
    if sco < 63:
        #print("I guess it is ECB!!!")
        return True
    else:
        #print("I guess it is CBC!!!")
        return False


if __name__=="__main__":
    if(len(sys.argv) < 2):
        print("Ya gotta give me some text to encode yo, maybe kinda long, also it would need to have repeated phrases and patterns and whatnot.")
        sys.exit()
    text = sys.argv[1]
    if((len(sys.argv)>=3) and (sys.argv[2] == 'b64')):
        text = bytes(b64_to_bytes(text))
    else:
        text = text.encode()
    for i in range(0,15):
        ctext = encryption_oracle(text)
        is_ecb(ctext)
