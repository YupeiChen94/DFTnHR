from flask import Flask
app = Flask(__name__)

# class PrefixMiddleware(object):
#     # class for URL sorting
#     def __init__(self, app, prefix=''):
#         self.app = app
#         self.prefix = prefix
#
#     def __call__(self, environ, start_response):
#         # in this line I'm doing a replace of the word dfthr which is my app name in IIS to ensure proper URL redirect
#         if environ['PATH_INFO'].lower().replace('/rd', '').startswith(self.prefix):
#             self.path = environ['PATH_INFO']
#             environ['PATH_INFO'] = environ['PATH_INFO'].lower().replace('/rd', '')[len(self.prefix):]
#             self.path2 = environ['PATH_INFO']
#             environ['SCRIPT_NAME'] = self.prefix
#             self.script = environ['SCRIPT_NAME']
#             return self.app(environ, start_response)
#         else:
#             start_response('404', [('Content-Type', 'text/plain')])
#             return ["This url does not belong to the app.".encode()]
#
#
# app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/dfthr')


@app.route('/hello')
def hello():
    return "Hello!"


@app.route('/')
def home():
    return 'You are on the homepage of DFTHR!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)