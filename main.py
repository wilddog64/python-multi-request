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

class Application(web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self._data = None
        self._conn = None
        self._cursor = None
        self._DEFAULT_PATH = os.path.join(os.path.realpath(''), 'db.sqlite')

    # connect to database
    def db_connect(self, conn=None, db_path=None):

        if db_path is None:
            db_path = self._DEFAULT_PATH

        if self._conn is None:
            self._conn = sqlite3.connect(db_path)

        self._conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])

    def create_word_table(self):

        # create table
        create_stmt = 'CREATE TABLE IF NOT EXISTS words(id integer primary key autoincrement, word text)'
        self._cursor = self._conn.cursor()
        self._cursor.execute(create_stmt)

    def insert_data(self, data):
        insert_stmt = 'INSERT INTO words (word) VALUES (?)'
        self._cursor = self._conn.cursor()

        try:
          for r in data:
              self._cursor.execute(insert_stmt, (r,))
          self._conn.commit()
        except:
            self._conn.rollback()
            raise RuntimeError('fail to insert data')

    def get_word(self, idx):
        select_stmt = 'SELECT id, word FROM words WHERE id = (?)'

        self.db_connect()
        cursor = self._conn.cursor()
        cursor.execute(select_stmt, str(idx))
        row = cursor.fetchone()

        return row

# this storeRecords class has one post method that can accept a post data from web and
# store the upload data in a localhost /tmp directory.
class storeRecords(web.RequestHandler):
    def post(self):
        # self.data = re.sub(r'\s+', '\n', self.request.body.decode('utf-8'))
        data = self.request.body.decode('utf-8').split(' ')
        self.application.db_connect()
        self.application.create_word_table()
        self.application.insert_data(data)

# the getWord class will generate an unique RESTful url and return the data. The get method
# it provided is an asynchron
class getWords(web.RequestHandler):
    @web.asynchronous
    def get(self, arg):
        # we make get as an asynchronus method, which means the method can accept multiple
        # request. But it won't flush the buffer. We have to call finsh manually. To support
        # asynchronus, we use IOLoop, set the callback to finish method

        # to make a unique REST url, we add target as a parameter for get method. This each word in our
        # file becomes http://localhost:8000/words/<a word>

        index = int(arg)
        word = self.application.get_word(index)
        self.write(json.dumps(word))

        # make this web method become async, and call finish method when timeout
        loop = IOLoop.instance()
        loop.add_timeout(loop.time() + 0.1, self.finish)

if __name__ == '__main__':
    # create our simple REST server
    app = Application([('/healthcheck', healthCheck),
           ('/records', storeRecords),
           (r'/words/(\d+)',getWords)])
    httpServer = HTTPServer(app)
    httpServer.listen(8000)
    IOLoop.instance().start()
