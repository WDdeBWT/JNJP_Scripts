import tornado.ioloop
import tornado.web
import tornado.options
from tornado.escape import json_decode
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ajaxPost.html")

class AjaxHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("hello world")
        self.write("我们都惠吹")
    
    def post(self):
        # self.write(bytes(str(self.request), encoding = "utf-8"))
        try:
            data=json_decode(self.request.body)
            print(data)
        except :
            pass
        self.write(data['slogan'])
        # self.write("我们不惠吹")

settings = {
"static_path": os.path.join(os.path.dirname(__file__), "static") 
}

application = tornado.web.Application([
    (r"/demo", MainHandler),
    (r"/test", AjaxHandler),
    ],**settings)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()