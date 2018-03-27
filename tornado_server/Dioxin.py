# coding:utf-8
# @__Author__ = "WDdeBWT"
# @__Date__ : 2018/03/27

import os
import json

import tornado.ioloop
import tornado.web
import tornado.options
from tornado.escape import json_decode

import DataAnalysis

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ajaxPost.html")

class AjaxHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Double Evil English --- 我们都惠吹")

    def post(self):
        try:
            data=json_decode(self.request.body)
            print(data)
            da = DataAnalysis.Vectorization('D:\\code\\github\\JNJP_Scripts\\tornado_server\\static')
            format_matrix = da.get_format_matrix(data['key_string'])
            sim_dict = da.get_similarity_vector(format_matrix)
            case_description = da.get_case(sim_dict['max_sim'])
            img_dict = da.get_img(sim_dict['max_sim'])
            suggest_description = da.get_suggest(sim_dict['max_sim'])
            format_dict = self.formatmatrix_to_dict(format_matrix)
            json_str = json.dumps({'format_dict': format_dict, 'sim_dict': sim_dict, 'case_description': case_description,
                'img_dict': img_dict, 'suggest_description': suggest_description, 'status_code': str(200), 'status_msg': '(^_^)'})
            self.write(json_str)
        except Exception as e:
            print(e)
            rt_dict = {'status_code': 404, 'status_msg': 'AjaxHandler Post Error'}
            self.write(json.dumps(rt_dict))

    def formatmatrix_to_dict(self, format_matrix):
        format_matrix_dict = {}
        for fmt_li in format_matrix:
            temp_str = ''
            for block in fmt_li[1:]:
                temp_str = temp_str + '-' + block
            format_matrix_dict[fmt_li[0]] = temp_str
        return format_matrix_dict

settings = {
"static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/ajax_search", AjaxHandler),
    ],**settings)

if __name__ == '__main__':
    application.listen(8086)
    tornado.ioloop.IOLoop.instance().start()