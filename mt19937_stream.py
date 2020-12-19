import random
import mt19937 as mt



class bytestream:
    def __init__(self, seed):
        self.index = 4
        self.fourbyte = 0
        import mt19937 as mt0
        mt0.seed_mt(seed)
        self.__extract4 = mt0.extract_number
    def extract(self):
        if self.index >= 4:
            self.fourbyte = self.__extract4()
            self.index = 0
        b0 = ((self.fourbyte >> (8*(3-self.index)))&(0xFF))
        self.index += 1
        return b0


def mt_decr(ctext, key):
    #ctext is a bytearray
    b0 = bytestream(key)
    ptext = []
    for i in range(0, len(ctext)):
        ptext.append(ctext[i] ^ b0.extract())
    return bytes(ptext)

def mt_encr(ptext, key, isbytes = False):
    #ptext is a string, key is an int
    #mt_encr and mt_decr do the same thing but take different input types
    if isbytes: bptext = ptext
    else: bptext = ptext.encode()
    b0 = bytestream(key)
    ctext = []
    for i in range(0, len(ptext)):
        ctext.append(bptext ^ b0.extract())
    return bytes(ctext)

def rando_encr(ptext, isbytes = False):
    rkey = random.randint(0,2**16-1)
    preflen = random.randint(10,50)
    pref = [random.randint(0,255) for i in range(0,preflen)]
    if isbytes: bptext = ptext
    else: bptext = ptext.encode()
    return mt_decr(bytes(pref)+bptext, rkey)

def crack_rando_encr(ptext, ctext, isbytes = False):
    #finds the 16bit seed for the mt19937 encryption
    #where ptext was encrypted with rando_encr
    l0 = len(ptext)
    l1 = len(ctext)
    ind1 = int(l1/4)*4 - 4
    ind0 = ind1-l1
    if isbytes: bptext = ptext
    else: bptext = ptext.encode()
    b0 = int.from_bytes((bptext[ind0],bptext[ind0+1],bptext[ind0+2],bptext[ind0+3]), 'big')
    c0 = int.from_bytes((ctext[ind1],ctext[ind1+1],ctext[ind1+2],ctext[ind1+3]), 'big')
    r0 = b0^c0
    #this is only gonna work for sure if ptext is long enough, like at least 7 or 8 chrs
    for i in range(0,2**16):
        prn = 0
        mt.seed_mt(i)
        for j in range(0,int(ind1/4)+1):
            prn = mt.extract_number()
        if prn == r0:
            return i
    return None

def gen_pswd_rst_tkn(seed, ctext, n = 10):
    #generates an n*4 byte password reset token
    l0 = len(ctext)
    if (l0%4) == 0: #makes rlen = ceil(l0/4) but i didn't feel like using the math ceil function
        rlen = int(l0/4)
    else:
        rlen = int(l0/4)+1
    mt.seed_mt(seed)
    for i in range(0,rlen):
        mt.extract_number()
    tkn = []
    for i in range(0,n):
        bts = (mt.extract_number()).to_bytes(4, 'big')
        tkn += [bts[0],bts[1],bts[2],bts[3]]
    return bytes(tkn)

def check_pswd_tkn(seed, ctext, tkn):
    l1 = len(tkn)
    if (l1%4) != 0:
        return False
    l0 = len(ctext)
    if (l0%4) == 0:
        rlen = int(l0/4)
    else:
        rlen = int(l0/4)+1
    mt.seed_mt(seed)
    for i in range(0,rlen):
        mt.extract_number()
    for i in range(0,int(l1/4)):
        if int.from_bytes(tkn[i*4:i*4+4],'big') != mt.extract_number():
            return False
    return True





