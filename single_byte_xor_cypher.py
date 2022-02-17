import os
import sys



#if(len(sys.argv) < 2):
#    print("Needs one argument")
#    sys.exit()


def freq_ya(text):
    freq_dict = {}
    for c in text:
        if c in freq_dict:
            freq_dict[c] += 1
        else:
            freq_dict.setdefault(c, 1)
    so_by_val = sorted(freq_dict.items(), key=lambda x:x[1], reverse=True)


def count_chars(text):
    count = 0
    bads = [92,38,36,37,124,33]
    for b in text:
        if(b <= 90 and b >= 65):
            count += 1
        elif(b <= 122 and b >= 97):
            count += 1
        elif(b == 32):
            count += 2
        elif(b >= 0 and b <= 31):
            count -= 8
        elif(b >= 48 and b <= 57):
            count += 1
        elif(b == 39):
            count += 1
        elif(b in bads):
            count -= 4
        elif(b >= 128):
            count -= 8
        if(b == 101):
            count += 1
    return count


def score(text):
    count = 0
    bads = [92,38,36,37,124,33]
    for b in text:
        if(b <= 90 and b >= 65):
            count += 2
        elif(b <= 122 and b >= 97):
            count += 2
        elif(b == 32):
            count += 2
        elif(b >= 0 and b <= 31):
            count -= 0
        elif(b >= 48 and b <= 57):
            count += 1
        elif(b == 39):
            count += 1
        elif(b in bads):
            count -= 0
        elif(b >= 128):
            count -= 0
        if(b == 101):
            count += 1
    return count


def singlebyte(h_str, bytez=False, sol=0):
    arrayo = {}
    for  i in range(0,256):
        text = int(h_str, 16) ^ int(((bin(i)[2:])).zfill(8)*int((len(h_str))/2), 2)
        h_txt = hex(text)[2:].zfill(len(h_str))
        #print(h_txt)
        act_text = bytes.fromhex(h_txt)
        act_text = [int(c) for c in act_text]
        arrayo.setdefault(i, (count_chars(act_text), act_text))
        #arrayo is a dict with keys of the xor key, and values (score, text) tuples

    so_arrayo = sorted(arrayo.items(), key=lambda x:x[1][0], reverse=True)

    #print(so_arrayo[:20])
    #print(type(so_arrayo[0][1][1]))
    #print(str(so_arrayo[0][1][1]))
    if bytez:
        return(so_arrayo[sol][1][0],(so_arrayo[sol][1][1]),so_arrayo[sol][0])
    else:
        return(so_arrayo[sol][1][0],"".join([chr[x] for x in so_arrayo[sol][1][1]]),so_arrayo[sol][0])

#singlebyte(sys.argv[1])
