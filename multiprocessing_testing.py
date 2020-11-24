import multiprocessing as mp
import os
import random
import time

def work(i):
    r = random.randint(1, 999)
    if r == 123:
        return (i, r)
    return ()
    
def q_work(i):
    r = random.randint(1,9999)
    if r == 2:
        q_work.q.put((i, r))
        return (i, r)
    return ()
    
def mult_work(iv = 20):
    p = mp.Pool(mp.cpu_count())
    res = [p.apply_async(work, (i, )) for i in range(iv)]
    print([r.get(timeout=3) for r in res])
    
def q_w_init(q):
    q_work.q = q
    
def mult_q_work(iv = 10000):
    i = 0
    jobs = range(iv)
    q = mp.Queue()
    p = mp.Pool(None, q_w_init, [q])
    res = p.map_async(q_work, jobs)
    while q.empty():
        time.sleep(0.1)
        if i >= 99:
            break
        i += 1
    print(q.get_nowait())
    p.terminate()
    return