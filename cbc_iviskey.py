import cbc_decrypt
from ecb_cbc_oracle import gen_bytes

key = gen_bytes(16)
iv = key
def smoke_3_blocks(text, k=key):
    #We are intentionally encrypting in cbc with iv=key
    #NOT secure at all. The point is to implement an exploiter as it were
    if len(text) < 33:
        print("is not at least 3 blocks :(")
        return None
    return cbc_decrypt.encrypt_cbc(text, k, k, 16)

def receive(ctext, k=key):
    ptext = cbc_decrypt.decrypt_cbc(ctext, k, k, 16)
    for c in ptext:
        if c > 127:
            raise ValueError(ptext)
    return True

def modlify(ctext):
    if len(ctext) < 48:
        print("oh no!, the ctext isn't long enough :{")
        return None
    K = b''
    m_ctext = ctext[0:16]+(b'\x00'*16)+ctext[0:16]
    try:
        receive(m_ctext)
    except ValueError as val:
        ptext = (val.args)[0]
        K = cbc_decrypt.bytes_xor(ptext[0:16], ptext[32:48])
    return K


