import json
import re
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

# this storeRecords class has one post method that can accept a post data from web and
# store the upload data in a localhost /tmp directory.
class storeRecords(web.RequestHandler):
    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        data = re.sub(r'\s+', '\n', self.request.body.decode('utf-8'))
        # self.write(data.split("\n"))
        with open('/tmp/words.txt', 'w') as f:
            f.writelines(data)

words = []
with open('/tmp/words.txt', 'r') as f:
    for line in f:
        words.append(line.strip())

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
