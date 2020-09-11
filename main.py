# import json
# import requests

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado import web
from tornado.options import define, options, parse_command_line

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
        pass

class getRecord(web.RequestHandler):
    @web.asynchronous
    def get(self, arg):
        pass

def makeApp():
    urls = [('/healthcheck', healthCheck),
            ('/records', storeRecords),
            ('/record/word',getRecord)]
    
    return web.Application(urls)

if __name__ == '__main__':
    app = web.Application([('/healthcheck', healthCheck),
           ('/records', storeRecords),
           ('/record/word',getRecord)])
    httpServer = HTTPServer(app)
    httpServer.listen(8000)
    IOLoop.instance().start()
