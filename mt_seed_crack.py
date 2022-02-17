import time
import random
import mt19937 as mt


def waiting_seed_rng(lbd = 40, ubd = 1000, wait=True):
    wint = random.randint(lbd, ubd)
    if wait == True: #actually wait
        time.sleep(wint)
        mt.seed_mt(int(time.time()))
        wint = random.randint(lbd, ubd)
        time.sleep(wint)
    else: #simulate waiting
        mt.seed_mt(int(time.time() + wint))
    return mt.extract_number()


def crack_seed(rando, vals=10000):
    t0 = int(time.time())
    for i in range(0, vals):
        mt.seed_mt(t0 + i)
        if rando == mt.extract_number():
            return t0 + i
        mt.seed_mt(t0 - i - 1)
        if rando == mt.extract_number():
            return t0 - i -1
    return None

def check_seed_consistency(seed):
    mt.seed_mt(seed)
    return mt.extract_number()
