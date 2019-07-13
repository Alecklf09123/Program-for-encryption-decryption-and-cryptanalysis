from multiprocessing import Pool
from random import getrandbits

key = getrandbits(56)

def f(x):
    for i in range(x[0], x[1]):
        print(i)
        if key == i:
            print("yahoo! = ", i)
            f = open('text.txt', 'w')
            f.write(i)
            break

if __name__ == '__main__':
# print(list(range(2**56)))
    with Pool(5) as p:
        print(p.map(f, [(0, 2**10), (2**10, 2**20), (2**20, 2**30), (2**30, 2**40), (2**40, 2**56)]))
