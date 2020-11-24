from ecb_cbc_oracle import is_ecb
import sys
from brk_rxc import b64_to_bytes
import ecb_cbc_oracle
from decrypt_aes_ecb import encrypt as encrypt_ecb

rand_key = ecb_cbc_oracle.gen_bytes(16)

unknwntxt = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

def encrypt_text_and_something_else(text, unkwn):
    #takes text as a bytearray and unkwn as text encoded in base64
    #and encrypts them with aes ecb mode
    atext = text+bytes(b64_to_bytes(unkwn))
    ctext = encrypt_ecb(atext, rand_key)
    return ctext

def check_block_length():
    l0 = len(encrypt_text_and_something_else("A".encode(), unknwntxt))
    for i in range(2,999):
        l1 = len(encrypt_text_and_something_else(("A"*i).encode(), unknwntxt))
        if(l0 != l1):
            return l1-l0
    return None

def is_this_ecb():
    text = ("A"*2000).encode()
    return is_ecb(encrypt_text_and_something_else(text, unknwntxt))

def find_ith_char(i, blocksize, found_already, encryptor=encrypt_text_and_something_else):
    #assumes that found_already is a string of length i
    #must have access to the encrypting function
    blk = int((i)/blocksize)
    n_append =(blocksize-1) - (i%blocksize)
    text = ("A"*n_append).encode()
    ctext = encryptor(text, unknwntxt)
    if len(ctext) < (blocksize*(blk+1)):
        #print("Reached end of ciphertext")
        return None
    cblock = ctext[blocksize*blk:blocksize*(blk+1)]
    #print("cblock = "+str(cblock))
    for j in range(0,256):
        if(i < (blocksize-1)):
            append = ("A"*(blocksize-1-i)).encode()+found_already
        else:
            append = found_already[i-(blocksize-1):]
        append = append+bytes([j])
        ctext = encryptor(append, unknwntxt)
        cblock0 = ctext[0:blocksize]
        if(cblock0 == cblock):
            #ring a ding ding, we found the next character
            return bytes([j])
    #print("exhausted Bytes to try, giving up I guess")
    return None

def find_chars(encryptor=encrypt_text_and_something_else):
    if (is_this_ecb() == False):
        print("AAAhh, apparently it's not ECB!!!!")
        return None
    blocksize = check_block_length()
    #print("blocksize = "+str(blocksize))
    found_allerede = b''
    i=0
    while(True):
        ith_chr = find_ith_char(i, blocksize, found_allerede, encryptor)
        if ith_chr == None:
            return found_allerede
        found_allerede += ith_chr
        #print(ith_chr)
        i += 1
