# coding:utf-8
# @__Author__ = "WDdeBWT"
# @__Date__ : 2018/03/27

import os
import json
import time

import tornado.ioloop
import tornado.web
import tornado.options
from tornado.escape import json_decode

import DataAnalysis

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("search.html")
class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("search.html")
class PostHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ajaxPost.html")
class ProcessHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("process.html")
class IntroduceHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("introduce2.html")

class AjaxHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Double Evil English --- 我们都惠吹")

    def post(self):
        try:
            data=json_decode(self.request.body)
            # print(data)
            da = DataAnalysis.Vectorization('D:\\VSCodeTest\\Show\\static')
            # da = DataAnalysis.Vectorization('C:\\Users\\Administrator\\Desktop\\Dioxin_tornado_80\\static')
            format_matrix = da.get_format_matrix(data['key_string'])
            sim_dict = da.get_similarity_vector(format_matrix)
            case_description = da.get_case(sim_dict['max_sim'])
            img_dict = da.get_img(sim_dict['max_sim'])
            suggest_dict = da.get_suggest(sim_dict['max_sim'])
            order_str = da.get_order()
            format_dict = self.formatmatrix_to_dict(format_matrix)
            json_str = json.dumps({'format_dict': format_dict, 'sim_dict': sim_dict, 'case_description': case_description,
                'img_dict': img_dict, 'suggest_dict': suggest_dict, 'order_str': order_str, 'status_code': str(200), 'status_msg': '(^_^)'})
            time.sleep(1)
            assert len(data['key_string']) >= 50
            self.write(json_str)
        except Exception as e:
            print(e)
            rt_dict = {'status_code': str(404), 'status_msg': 'AjaxHandler Post Error'}
            self.write(json.dumps(rt_dict))

    def formatmatrix_to_dict(self, format_matrix):
        format_matrix_dict = {}
        for fmt_li in format_matrix:
            temp_str = ''
            for block in fmt_li[1:]:
                temp_str = temp_str + '-' + block[0:6]
            format_matrix_dict[fmt_li[0]] = temp_str
        return format_matrix_dict



settings = {
"static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/search", SearchHandler),
    (r"/ajaxPost", PostHandler),
    (r"/process", ProcessHandler),
    (r"/introduce2", IntroduceHandler),
    (r"/ajax_search", AjaxHandler),
    ],**settings)

if __name__ == '__main__':
    application.listen(8086)
    tornado.ioloop.IOLoop.instance().start()