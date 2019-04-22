import mp_pool as mp
import time
import random as rd
import threading


def test(a, b):
    return sum(range(min(a,b)), max(a,b))


def pp(name):
    for i in range (1000):
        a, b = rd.randint(1,10000), rd.randint(1,10000)
        res1, res2 = test(a, b), p.map_one(test, (a,b))
        
        assert res1 == res2, "thread {} |worker {} call no {} | {} != {}".format(name,1, i, res1, res2)
    print('thread {} finished without errors'.format(name))
p = mp.Pool(5)
nb_thread = 6

threads = []
for i in range(nb_thread):
    t = threading.Thread(target=pp, args=(str(i), ))
    threads.append(t)
    t.start()

for t in threads : t.join()
p.stop()