from wsgiref.simple_server import make_server


def myapp(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    if len(environ['PATH_INFO']) == 1:
        return "Hello World!"
    else:
        return "Hello {name}!".format(name=environ['PATH_INFO'][1:])


httpd = make_server('', 8000, myapp)
print ("Serving HTTP on port 8000...")

httpd.serve_forever()