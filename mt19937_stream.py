import random




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
        b0 = ((self.fourbyte >> (8*self.index))&(0xFF))
        self.index += 1
        return b0


def mt_decr(ctext, key):
    #ctext is a bytearray
    b0 = bytestream(key)
    ptext = []
    for i in range(0, len(ctext)):
        ptext.append(ctext[i] ^ b0.extract())
    return bytes(ptext)

def mt_encr(ptext, key):
    #ptext is a string, key is an int
    #mt_encr and mt_decr do the same thing but take different input types
    bptext = ptext.encode()
    b0 = bytestream(key)
    ctext = []
    for i in range(0, len(ptext)):
        ctext.append(bptext ^ b0.extract())
    return bytes(ctext)

def rando_encr(ptext):
    rkey = random.randint(0,2**16-1)
    preflen = random.randint(10,50)
    pref = [random.randint(0,255) for i in range(0,preflen)]
    return mt_decr(bytes(pref)+ptext.encode(), rkey)
