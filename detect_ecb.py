import sys
from brk_rxc import hammingD

def score(bytez):
    l = len(bytez)
    segs = int(l/16)
    if segs == 0:
        return float('inf')
    sco = 0
    for i in range(0,segs-1):
        for j in range(i,segs):
            sco += hammingD(bytez[i*16:i*16+16],bytez[j*16:j*16+16], True)
    return sco/(segs**2)

if __name__ == "__main__":
    if(len(sys.argv) <= 1):
        print("need one argument with the text file to check detect ECB encoded string. One string per line, hex encoded")
        sys.exit()
    fname = sys.argv[1]
    text = open(fname).read().split("\n")
    textb = [bytes.fromhex(s) for s in text]
    scores = [(i,score(textb[i])) for i in range(0,len(textb))]
    sortscores = sorted(scores, key=lambda a : a[1])
    print("It's the "+str(sortscores[0][0])+"th one.\n")
    print(sortscores[0][1])
    sortext = [(j[0], j[1], text[j[0]]) for j in sortscores]
    print("\n")
    print("Other lines and their scores")
    print(*sortext[0:20], sep="\n")
