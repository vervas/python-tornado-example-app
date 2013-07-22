from tornado.options import define, options, parse_command_line
import tornado.ioloop
import tornado.web
import tornado.httpserver
import os

define("port", default=8888, help="Port to listen on", type=int)


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('hello.html', app_type='Tornado')

if __name__ == "__main__":
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
    )

    server = tornado.httpserver.HTTPServer(app)
    server.bind(options.port)
    # autodetect cpu cores and fork one process per core
    try:
        server.start(0)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
