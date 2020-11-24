def pad_val(text):
    if(len(text) == 0):
        raise Exception("This bytearray is flippin' empty yo!")
    x = text[-1]
    if(x > 16 or x == 0):
        raise Exception("This bytearray has a non-padding character at end")
    if(len(text) < x):
        raise Exception("This bytearray has invalid PKCS7 padding")
    if(text[len(text)-x:] != ((chr(x).encode())*x)):
        raise Exception("This bytearray has invalid PKCS7 padding")
    return text[:len(text)-x]
