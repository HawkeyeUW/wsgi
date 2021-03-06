"""
This pseudo calculator should support the following operations:

  * Positive
  * Negative

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/positive/5' then the response
body in my browser should be `true`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/positive/5  => 'true'
  http://localhost:8080/positive/0  => 'false'
  http://localhost:8080/positive/-5 => 'false'
  http://localhost:8080/negative/0  => 'false'
  http://localhost:8080/negative/-2 => 'true'
```

"""
def home():
    body = ['<h1>Pseudo Calculator</h1>', '<ul>']
    body.append('<h3>This is a calculator that will determine if number is positive or negative</h3>')
    body.append('<ul>')
    body.append('<html>Instructions......</html>')
    body.append('<li>First parameter of path will be the word positive or negative</li>')
    body.append('<li>Second parameter of path will be the number</li>')
    body.append('<li>Example: /positive/5 will yield TRUE</li>')
    return '\n'.join(body)

def positive(*args):
    value = args[0]
    value = int(value)
    if value > 0:
        sign = True
    else:
        sign = False

    page = ['<h1>Pseduo Calculator for Positive Values</h1>']
    page.append(f'<html>The value is {value} and it is positive {sign}</html>')
    return '\n'.join(page)

def negative(*args):
    value = args[0]
    value = int(value)
    if value < 0:
        sign = True
    else:
        sign = False

    page = ['<h1>Pseduo Calculator for Negative Values</h1>']
    page.append(f'<html>The value is {value} and it is negative {sign}</html>')
    return '\n'.join(page)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments, based on the path.
    """

    funcs = {
        '': home,
        'positive': positive,
        'negative': negative
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func= funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    #func = some_func
    #args = ['25', '32']

    #return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
