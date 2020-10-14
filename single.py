import json
import requests

def process_id(id):
    url = 'http://localhost:8000/words/%i'
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

def process_word(word):
    url_template = "http://localhost:8000/words/%s"
    r = requests.get(url_template % word)
    data = r.json()
    return data

if __name__ == '__main__':
    id_range = range(100)
    process_range_id(id_range)
