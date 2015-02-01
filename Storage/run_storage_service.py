from multiprocessing import Pool
import store
import read
import query_service
from data_store import DataStore

if __name__ == '__main__':
    data_store = DataStore()
    pool = Pool(processes=2)
    pool.apply_async(store.listen_for_imports, [data_store])
    pool.apply_async(query_service.listen_for_queries, [data_store])
    
    pool.close()
    pool.join()
