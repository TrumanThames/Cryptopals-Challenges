from ecb_cbc_oracle import gen_bytes
from aes_ctr import encrypt_ctr, decrypt_ctr
from brk_rxc import b64_to_bytes
from single_byte_xor_cypher import count_chars, score

rankey = gen_bytes(16)
nonce = b'\x00'*8

texts = [b'SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==',
b'Q29taW5nIHdpdGggdml2aWQgZmFjZXM=',
b'RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==',
b'RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=',
b'SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk',
b'T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
b'T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=',
b'UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
b'QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=',
b'T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl',
b'VG8gcGxlYXNlIGEgY29tcGFuaW9u',
b'QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==',
b'QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=',
b'QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==',
b'QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=',
b'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
b'VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==',
b'SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==',
b'SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==',
b'VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==',
b'V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==',
b'V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==',
b'U2hlIHJvZGUgdG8gaGFycmllcnM/',
b'VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=',
b'QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=',
b'VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=',
b'V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=',
b'SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==',
b'U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==',
b'U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=',
b'VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==',
b'QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu',
b'SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=',
b'VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs',
b'WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=',
b'SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0',
b'SW4gdGhlIGNhc3VhbCBjb21lZHk7',
b'SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=',
b'VHJhbnNmb3JtZWQgdXR0ZXJseTo=',
b'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=']

txts = [bytes(b64_to_bytes(t.decode())) for t in texts]

ctexts = [encrypt_ctr(rankey, nonce, txt) for txt in txts]

def candidates(ctexts):
    maxlen = max([len(l) for l in ctexts])
    if maxlen <=0 :
        return []
    ctxts_blk1 = [a[:16] for a in ctexts]
    cblk1 = [0]*16
    s = []
    for i in range(0,16):
        ct = []
        for j in range(0,256):
            counts = [j^t[i] for t in ctxts_blk1 if len(t) > i]
            ct += [(score(counts), j)]
        ct.sort(reverse=True, key=lambda x: x[0])
        s.append(ct[0:3])
    return s + candidates([c[16:] for c in ctexts])

def key_check(ctexts):
    cands = candidates(ctexts)
    ks = len(cands[0])
    keys = []
    for i in range(0,ks):
        keys += [[k[i][1] for k in cands]]
    return keys

def xor_dem(ctext, key):
    return [chr(ctext[i]^key[i]) for i in range(0,len(ctext))]

