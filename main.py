import json
import re
import os
import sys
import sqlite3
# import requests

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado import web
from tornado.options import define, options, parse_command_line
from tornado.httputil import parse_body_arguments

url_template = "http://localhost:8000/records/%i"

# process_id is a function to process a single id at a time
# def process_id(id):
#     r = requests.get(url_template % id)
#     data = r.json()
#     requests.put(url_template % id, data=data)
#     return data

# define('port', default=8000, help='enable http service run on a particular port, default is 8000', type=int)
# define('delay', default=0.1, help='a delay for GET requests', type=float)

# the healCheck class provide a simple message telling people we are live
class healthCheck(web.RequestHandler):
    def get(self):
        self.write({'message': 'yay, you reach me!!'})

class requestHandlerBase(web.RequestHandler):
    self._DEFAULT_PATH = os.path.join(os.path.realpath(''), 'db.sqlite')
    self._data = None
    self._conn = None
    self._cursor = None

    # connect to database
    def db_connect(self, conn, db_path=self._DEFAULT_PATH):
        self.conn = sqlite3.connect(db_path)

    def create_word_table(self):

        # create table
        create_stmt = ```
        CREATE TABLE IF NOT EXISTS words(id int, word text)
        ```
        self.cursor = self._conn.cursor()
        self.cursor.execute(create_stmt)

    def insert_data(self):
        insert_stmt = 'INSERT INTO words (word) VALUES (?)'
        self.cursor = self._conn.cursor()

        try:
          for r in data:
              self._cursor.execute(insert_stmt, r)
          self._conn.commit()
        except:
            self._conn.rollback()
            raise RuntimeError('fail to insert data')

    def get_word(self, id):
        select_stmt = 'SELECT id, word FROM words WHERE id = (?)'

        cursor = self.cursor
        cursor.execute(select_stmt, id)
        result = cursor.fetchone()

        return result

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, value):
        self._conn = value

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = value

# this storeRecords class has one post method that can accept a post data from web and
# store the upload data in a localhost /tmp directory.
class storeRecords(web.RequestHandlerBase):
    def post(self):
        # data = re.sub(r'\s+', '\n', self.request.body.decode('utf-8'))
        self.data = self.request.body.decode('utf-8').split(' ')
        self.db_connect()
        self.create_word_table()
        self.insert_data


words = []

# the getWord class will generate an unique RESTful url and return the data. The get method
# it provided is an asynchron
class getWords(web.RequestHandlerBase):
    @web.asynchronous
    def get(self, arg):
        # we make get as an asynchronus method, which means the method can accept multiple
        # request. But it won't flush the buffer. We have to call finsh manually. To support
        # asynchronus, we use IOLoop, set the callback to finish method

        # to make a unique REST url, we add target as a parameter for get method. This each word in our
        # file becomes http://localhost:8000/words/<a word>

        # words an array, and we want to access it outside of current scope
        # this allow us to cache the content without re-read it every time
        global words
        if len(words) == 0:
            with open('/tmp/words.txt', 'r') as f:
                for line in f:
                    words.append(line.strip())

        index = int(arg)
        self.write(json.dumps(dict(index=index, word=words[index])))

        # make this web method become async, and call finish method when timeout
        loop = IOLoop.instance()
        loop.add_timeout(loop.time() + 0.1, self.finish)

if __name__ == '__main__':
    # create our simple REST server
    app = web.Application([('/healthcheck', healthCheck),
           ('/records', storeRecords),
           (r'/words/(\d+)',getWords)])
    httpServer = HTTPServer(app)
    httpServer.listen(8000)
    IOLoop.instance().start()
