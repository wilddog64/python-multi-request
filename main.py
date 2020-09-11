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

class healthCheck(web.RequestHandler):
    def get(self):
        self.write({'message': 'yay, you reach me!!'})

class storeRecords(web.RequestHandler):
    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        data = re.sub(r'\s+', '\n', self.request.body.decode('utf-8'))
        # self.write(data.split("\n"))
        with open('/tmp/words.txt', 'w') as f:
            f.writelines(data)

class getWords(web.RequestHandler):
    @web.asynchronous
    def get(self):
        self.write({'message': 'passed'})
        loop = IOLoop.instance()
        loop.add_timeout(loop.time() + 0.1, self.finish)

if __name__ == '__main__':
    app = web.Application([('/healthcheck', healthCheck),
           ('/records', storeRecords),
           ('/words/',getRecord)])
    httpServer = HTTPServer(app)
    httpServer.listen(8000)
    IOLoop.instance().start()
