import requests
from threading import Thread

    def process_id(id):
        url = 'http://localhost/words/%i'
        r = requests.get(url % id)
        data = r.json()
        return data

    def process_range_id(id_range, store=None):
        if store is None:
            store = {}

        for id in id_range:
            store[id] = process_id(id)
            print(store[id])

        return store

    def threaded_processing(nThreads, id_range):
        store = {}
        threads = []

        # create threads here
        for i in range(nThreads):
            ids = id_range[i::nThreads]
            t = Thread(target=process_range_id, args=(ids, store))
            threads.append(t)

        # now we start threads and wait for threads to finish
        [t.start() for t in threads]
        [t.join() for t in threads]

        return store

    if __name__ == '__main__':
        id_range = range(8000)
        threaded_processing(100, id_range)
        # nList = [1, 2, 4, 8, 16, 32, 64]
        # for nThreads in nList[1:]:
        #     ans = threaded_processing(nThreads, id_range)
