import aes_ctr as ctr
import random
from brk_rxc import b64_to_bytes
from functools import reduce

key = int.to_bytes(random.randint(0,2**128-1), 16, 'big')

nonce = int.to_bytes(random.randint(0,2**64-1), 8, 'big')

file0 = open('25.txt', 'r')

str0 = file0.read().replace('\n','')

bytez0 = bytes(b64_to_bytes(str0))

ctext0 = ctr.encrypt_ctr(key, nonce, bytez0)

def edit(ctext, key, offset, ntext, isbytes=False):
    #offset 0 means start of ctext, it is 0 indexed
    strtblk = int(offset/16)
    lstblk = int((offset+len(ntext)-1)/16)
    ptext = []
    if isbytes: pass
    else: ntext = ntext.encode()
    for i in range(strtblk,lstblk+1):
        ptext.append(ctr.decrypt_ctr_n(key, nonce, i, ctext[16*i:min(len(ctext),16*(i+1))]))
    unmodded = reduce(lambda x,y:x+y, ptext)
    modded = unmodded[:offset%16] + ntext + unmodded[offset%16+len(ntext):]
    m_ctext = []
    for i in range(strtblk,lstblk+1):
        m_ctext.append(ctr.encrypt_ctr_n(key, nonce, i, modded[16*(i-strtblk):min(len(modded),16*(i+1-strtblk))]))
    modded_ctext = reduce(lambda x,y:x+y, m_ctext)
    CCC = ctext[:16*strtblk] + modded_ctext + ctext[16*(lstblk+1):]
    return CCC

def edityo(ctext, offset, ntext, isbytes=False):
    return edit(ctext, key, offset, ntext, isbytes)

def brk_edit(ctext, editor):
    #given a ctext and this edit function, discover the plaintext
    ptext = []
    for i in range(0,len(ctext)):
        for j in range(0,256):
            m_ctext = editor(ctext, i, bytes([j]), True)
            if m_ctext == ctext:
                ptext.append(bytes([j]))
                break
    return reduce(lambda x,y:x+y, ptext)
