import mp_pool as mp
import time


def test(a, b):
    # time.sleep(1)
    return a+b


p = mp.Pool(2)

result = p.map_one(test, (1 ,2))
print('result is', result)
result = p.map_one(test, (1 ,2))
print(result)
result = p.map_one(test, (1 ,2))
print(result)
result = p.map_one(test, (1 ,2))
print(result)
result = p.map_one(test, (1 ,2))
print(result)
result = p.map_one(test, (1 ,2))
print(result)
p.stop()
print('bde')