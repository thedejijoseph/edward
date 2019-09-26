
import tornado.web
import tornado.httpserver
import tornado.httpclient

import io, os, json
import secrets, random


class BaseHandler(tornado.web.RequestHandler):
    pass
    
class IndexPage(BaseHandler):
    def get(self):
       self.render('index.html')

class AboutPage(BaseHandler):
    def get(self):
        self.render('about.html')

class Connect(BaseHandler):
    def get(self):
        self.render('connect.html')
    
    def post(self):
        # process request: ajax
        name = self.get_argument('full_name', 'No Name')
        email = self.get_argument('email_address', 'noname@empty.io')
        phone = self.get_argument('phone_number', '+234 123 456 7890')

        

        success = {
            'status': 'success',
            'message': 'Connected.'
        }
        error = {
            'status': 'error',
            'message': ' Please try that again.'
        }
        self.write(json.dumps(success))


from tornado.options import define
define("port", default=3308, type=int)

handlers = [
    (r"/", IndexPage),
    (r"/about", AboutPage),
    (r"/connect", Connect)
]

# switch debug mode on or off
try:
    var = os.environ['APP_STAGE']
    prod = True if var == 'PROD' else False
except:
    prod = False


settings = dict(
    debug = False if prod else True,
    cookie_secret = secrets.token_hex(16),
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    autoescape = None,
)

app = tornado.web.Application(handlers, **settings)
def start():
    try:
        tornado.options.parse_command_line()
        port = tornado.options.options.port
        server = tornado.httpserver.HTTPServer(app)
        server.listen(port)
        
        start_msg = f"App server started. Port {port}"
        print('\n' + '=' * len(start_msg) + '\n' \
            + start_msg + '\n' + '=' * len(start_msg))
        
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        stop_msg = "Stopping app server"
        print('\n' + '=' * len(stop_msg) + '\n' \
            + stop_msg + '\n' + '=' * len(stop_msg))
        import sys
        sys.exit()

if __name__ == "__main__":
    start()
