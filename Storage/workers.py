from multiprocessing import Pool
import store
import read


def f(x):
    return x*x

if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.apply_async(store.receive_imports)
    pool.apply_async(read.receive_imports)
    
    print result.get(timeout=1)
    print pool.map(f, range(10))
