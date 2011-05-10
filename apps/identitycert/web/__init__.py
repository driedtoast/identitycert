from bottle import route, run, abort, debug
from bottle import mako_view as view
from bottle import send_file, redirect
from bottle import PasteServer
from bottle import request, response
import bottle
import os, sys,  traceback
import setup
import lib.oauth2 as oauth2

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


### OAUTH 2 flows

def get_param(name):
    if name in request.GET:
        return request.GET[name]
    if name in request.POST:
        return request.POST[name]
    return None


@route('/oauth2/testauthorize')
def testauthorize():
    ## process flow for oauth
    consumer_key = get_param('client_id')
    type = get_param('type')
    state = get_param('state')
    scope = get_param('scope')
    immediate = get_param('immediate')
    redirect_uri = get_param('redirect_uri')
    secret_type = get_param('secret_type')
    shared_secret = get_param('shared_secret')
    base_url =  get_param('base_url')
    
    params = []
    params['redirect_uri'] = redirect_uri
    
    oauthclient = oauth2.oauthclient(consumer_key, shared_secret, base_url)
    oauthclient.requestToken()
    
    redirect(oauthclient.authorizeRedirect(params=params))

@route('/oauth2/callback')
@view('oauth2/callback')
def testcallback():
    ## callback support
    return dict(name='oauth 2 callback');


## if 'simple_name' in request.POST:
##			simple_name = request.POST['simple_name']

@route('/oauth/useragentflow')
@view('oauth2/useragentflow')
def oauth2_useragentflow():
    return dict(name='oauth 2 useragentflow')

@route('/oauth/webserverflow')
@view('oauth2/webserverflow')
def oauth2_webserverflow():
    return dict(name='oauth 2 webserverflow')

@route('/oauth/deviceflow')
@view('oauth2/deviceflow')
def oauth2_deviceflow():
    return dict(name='oauth 2 deviceflow')

@route('/oauth/usernamepasswordflow')
@view('oauth2/usernamepasswordflow')
def oauth2_usernamepasswordflow():
    return dict(name='oauth 2 usernamepasswordflow')

@route('/oauth/clientcredentialsflow')
@view('oauth2/clientcredentialsflow')
def oauth2_clientcredentialsflow():
    return dict(name='oauth 2 clientcredentialsflow')

@route('/oauth/assertionflow')
@view('oauth2/assertionflow')
def oauth2_assertionflow():
    return dict(name='oauth 2 assertionflow')
    





########################
## Starts up the web 
## application
#######################
def startweb(host,port):
	bottle.TEMPLATE_PATH.insert(0,os.path.dirname( os.path.realpath( __file__ ))+'/views/')
	run(server=PasteServer,host=host, port=port)
