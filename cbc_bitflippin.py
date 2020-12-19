from pkcs7_pad_val import pad_val
from cryptography.hazmat.primitives import padding
from ecb_cbc_oracle import gen_bytes
from cbc_decrypt import encrypt_cbc, decrypt_cbc
from byte_at_time_ecb_decryption import check_block_length

rankey = gen_bytes(16)
iv = gen_bytes(16)

def preapp(string):
    newstring = b"comment1\"=\"cooking%20MCs\";\"userdata\"=\""+string+b"\";\"comment2\"=\"%20like%20a%20pound%20of%20bacon"
    padder = padding.PKCS7(128).padder()
    pstring = padder.update(newstring) + padder.finalize()
    ctext = encrypt_cbc(pstring, rankey, iv)
    return ctext

def look_for(ctext, s_term):
    ptext = decrypt_cbc(ctext, rankey, iv)
    found = ptext.find(s_term)
    if found == -1:
        return False
    else:
        return True

def ceiling(z0, bas):
    #rounds z0 up to a multiple of bas, both integers
    #it seems this will work with negatives, it's just a
    # little odd the think of rounding up to a multiple
    #of negative as going down
    mod = z0%bas
    if mod == 0:
        return z0
    return z0-mod+bas

def xor(bs0, bs1):
    #xors bs0 and bs1, two bytearrays, if not the same length
    #it extends {not actually, but it pretends, it prextends :} the shorter one with zeros
    l0 = len(bs0)
    l1 = len(bs1)
    l = min(l0,l1)
    bs = [0]*l
    for i in range(0, l):
        bs[i] = bs0[i] ^ bs1[i]
    if l0 == l:
        return bytes(bs)+bs1[l:]
    elif l1 == l:
        return bytes(bs)+bs0[l:]

def flip_insert_crack(ins_txt, encr=preapp):
    # given encr, which encrypts with cbc the input text with some
    #random pre and post fixes after sanitizing the input, modify
    #the returned ciphertext so that the plaintext inculdes ins_txt
    #using the xor next block bit flip vulnerability in cbc mode of aes
    ctext_base = encr(b'')
    l0 = len(ctext_base)
    lins = len(ins_txt)
    blocksize = check_block_length(encr)
    lins1 = ceiling(lins, blocksize)
    insert = b'O'*(2*lins1+l0)
    ctext0 = encr(insert)
    xord = xor(ins_txt, b'O'*lins)
    ctext_ins = xor(ctext0, b'\x00'*(l0+lins1)+xord)
    return ctext_ins
