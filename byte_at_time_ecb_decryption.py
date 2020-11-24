from decrypt_aes_ecb import encrypt as encrypt_ecb
from decrypt_aes_ecb import decrypt as decrypt_ecb
from ecb_cbc_oracle import gen_bytes, is_ecb
from random import randint

def prefix():
    num = randint(13,33)
    return gen_bytes(num)

pref = prefix()
rankey = gen_bytes(16)
target = b'oklahoma is my homie, that makes it my broklahoma'


def encr_stuff(atkr_bts, tart):
    return encrypt_ecb(pref+atkr_bts+tart, rankey)

def atkr_access_encr(atkr_bts):
    return encr_stuff(atkr_bts, target)



def is_this_ecb(encr):
    bigidness = len(encr(''))
    return is_ecb(encr(("A"*bigidness).encode()))

def check_block_length(encr):
    l0 = len(encr("A".encode()))
    for i in range(2,9999):
        l1 = len(encr(("A"*i).encode()))
        if(l0 != l1):
            return l1-l0
    return None

def find_ith_char(i, nappend, ilook, c0, blocksize, found_allerede, encr):
    #found_allerede is a bytearray of size i, i is from 0 to blocksize-1
    #goal is align the 
    blk = int(i/blocksize)
    n = nappend - (i%blocksize)
    text = c0*n
    ct0 = encr(text)
    if(len(ct0) < ilook+1+blk):
        #we have reached the end of the ciphertext
        print("end O ciphertext")
        return None
    b0 = ct0[ilook-blocksize+1+blk*blocksize:ilook+1+blk*blocksize]
    if(i < (blocksize-1)):
        appen = c0*(nappend-i)+found_allerede
    else:
        appen = c0*(nappend-blocksize+1)+found_allerede[i-(blocksize-1):i]
    for j in range(0,256):
        append = appen+bytes([j])
        ctext = encr(append)
        cblock0 = ctext[ilook-blocksize+1:ilook+1]
        if(cblock0 == b0):
            #we've found the ith character I guess
            #print(chr(j))
            #print(b0)
            #print(chr(j))
            #print(cblock0)
            return bytes([j])
    #print("Caramel dreams")
    return None

def find_chars(nappend, ilook, c0, blocksize, encr):
    found_allerede = b''
    i=0
    while(True):
        ith_char = find_ith_char(i, nappend, ilook, c0, blocksize, found_allerede, encr)
        if ith_char == None:
            return found_allerede
        found_allerede += ith_char
        i += 1
    return None


def atkr(encr=atkr_access_encr):
    if (is_this_ecb(encr) != True):
        print("This appears to be not ECB!")
        return None
    blocksize = check_block_length(encr)
    if blocksize == None:
        return None
    nappend = None
    c0 = "\x02".encode()
    ct0 = encr(c0*(3*blocksize))
    blocks = int(len(ct0)/blocksize)
    for i in range(0,blocks-1):
        if(ct0[i*blocksize:(i+1)*blocksize] == ct0[(i+1)*blocksize:(i+2)*blocksize]):
            index = i+1
    bblock = ct0[index*blocksize:(index+1)*blocksize]
    for i in range(1,blocksize):
        ctn = encr(c0*(3*blocksize-i))
        if(ctn[index*blocksize:(index+1)*blocksize] != bblock):
            nappend = 3*blocksize-i
            break
    i0 = (index+1)*blocksize-1
    return find_chars(nappend, i0, c0, blocksize, encr)

