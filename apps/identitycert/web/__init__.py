from bottle import route, run, abort, debug
from bottle import mako_view as view
from bottle import send_file, redirect
from bottle import PasteServer
from bottle import request, response
import bottle
import os, sys,  traceback
import setup

cfg = None


##############################################################
### static file methods
############################################################

@route('/static/js/:filename')
def static_file_js(filename):
    	send_file(filename, root=setup.staticdir+'/js')

@route('/static/js/plugins/:filename')
def static_file_js_plugins(filename):
    	send_file(filename, root=setup.staticdir+'/js/plugins')

@route('/static/templates/:filename')
def static_file_template(filename):
    	send_file(filename, root=setup.staticdir+'/templates')

@route('/static/css/:dir/images/:filename')
def static_file_css_images(dir,filename):
    	send_file(filename, root=setup.staticdir+'/css/'+dir+'/images')

@route('/static/css/:dir/:filename')
def static_file_cc(dir,filename):
	send_file(filename, root=setup.staticdir+'/css/'+dir)

##############################################################
### UI methods
############################################################

### dashboard
@route('/')
@view('index')
def index():
    return dict(name='index')

### account instances
@route('/oauth/:name')
@view('request')
def loginrequest(name):
	return dict(name='oauth requests', oauthrequest=name)

## if 'simple_name' in request.POST:
##			simple_name = request.POST['simple_name']

########################
## Starts up the web 
## application
#######################
def startweb(host,port):
	bottle.TEMPLATE_PATH.insert(0,os.path.dirname( os.path.realpath( __file__ ))+'/views/')
	run(server=PasteServer,host=host, port=port)

