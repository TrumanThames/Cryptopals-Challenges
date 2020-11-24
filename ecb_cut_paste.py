import sys
import ecb_cbc_oracle
from functools import reduce
from random import randint
from decrypt_aes_ecb import encrypt as encrypt_ecb
from decrypt_aes_ecb import decrypt as decrypt_ecb
from ecb_cbc_oracle import gen_bytes

uids = set({})

def profile_for(email):
    #takes an email and encodes with a userid and role removes = and &
    sanit = [c for c in email if ((c != '=') and (c != '&'))]
    semail = reduce(lambda x,y:x+y, sanit)
    i = randint(10,10)
    while(i in uids):
        #I was thinking about making a user id database
        #type deal but it think that is needlessly complicated
        i+=randint(1,38)
    return "email="+semail+"&uid="+str(i)+"&role=user"

def parse(prof_info):
    #takes a profile encoded as above and returns the dict
    d = {}
    sep = prof_info.split('&')
    for stuff in sep:
        kv = stuff.split('=')
        d[kv[0]] = kv[1]
    d['uid'] = int(d['uid'])
    return d

rand_key = gen_bytes(16)

def encrypt_prof(email, key=rand_key):
    return encrypt_ecb(profile_for(email).encode(), key)

def unpad(text):
    l = len(text)
    end_chr = text[l-1]
    if (end_chr >= 1 and end_chr <= 16):
        return text[:l-end_chr]
    return text

def decrypt_prof(ctext, key=rand_key):
    raw = decrypt_ecb(ctext, key, False)
    unraw = (unpad(raw)).decode('utf-8')
    return parse(unraw)

def attacker_make_admin(email, encr=encrypt_prof):
    #Creates a ciphertext with a user as an admin
    ctext = encr(email)
    firstn = "email="+email+"uid="
    #align the part after &role= with the start of the last block
    uid =10
    target = "email="+email+"&uid="+uid+"&role=admin"
    num_bytes = len(email)
    return
