from lib import bottle
from lib.bottle import route, template, request, error, debug, static_file
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

@route('/')
def index():
    content=""
    table=[0, 0, 0, 1, 2, 0, 0, 0, 0]
    output = template('templates/game', table=table, content=content)
    return output

@route('/help')
def help():
    static_file('help.html', root='.')

@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='static')

def main():
    debug(True)
    run_wsgi_app(bottle.default_app())
 
@error(403)
def Error403(code):
    return 'Get your codes right dude, you caused some error!'
 
@error(404)
def Error404(code):
    return 'Stop cowboy, what are you trying to find?'
 
if __name__=="__main__":
    main()