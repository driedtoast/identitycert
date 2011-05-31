from bottle import route, run, abort, debug
from bottle import mako_view as view
from bottle import send_file, redirect
from bottle import PasteServer
from bottle import request, response
from beaker.middleware import SessionMiddleware
import jwt
import bottle
import time
import os, sys,  traceback
import setup
import lib.oauth2 as oauth2
import json
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


### OAUTH 2 flows

def get_param(name):
    if name in request.GET:
        return request.GET[name]
    if name in request.POST:
        return request.POST[name]
    sess = get_session()
    if name in sess:
	return sess[name]
    return None

def get_session():
    s = request.environ.get('beaker.session')
    return s

## get a list of return values
def request_value_dict(namelist):
    retdict = {}
    for name in namelist:
	param = get_param(name)
	if param != None:
		retdict[name] = param
    return retdict    
    
## get a subset of a dict based on name list
def dict_subset(map,namelist):
    retdict = {}
    for name in namelist: 
        if name in map:
            retdict[name] = map[name]
    return retdict

def store_session(map, save=True):
    session = get_session()
    for k,v in map.items():
        session[k] = v
    if(save):
        session.save()

@route('/oauth2/testauthorize')
@view('oauth2/testauthorize')
def testauthorize():
    ## process flow for oauth
    tostore = request_value_dict(['client_id','shared_secret','redirect_uri','base_url','state','suffix_override','token_type'])
    params = dict_subset(tostore,['client_id','redirect_uri','state'])
    params['response_type'] = 'code'
     
    store_session(tostore, False)
    s = get_session()
    if s['state'] is None:
	s['state'] = s.id
        params['state'] = s['state']
    s.save()
    
    consumer_key = get_param('client_id')
    shared_secret = get_param('shared_secret')
    base_url =  get_param('base_url')
    
    oauthclient = oauth2.oauthclient(consumer_key, shared_secret, base_url)
    redirect_url = oauthclient.authorizeRedirect(params=params)
    return dict(link=redirect_url )

## gets the request token from the service
## based on the suffix 
def testrequesttoken():
    return request_token_call()

def request_token_call(secret=None,grant_type='authorization_code',assertion_type=None):
    ## process flow for oauth
    params = request_value_dict(['client_id','redirect_uri'])
    print grant_type
    if grant_type is 'authorization_code':
        params['code'] = get_param('code')
        params['client_secret'] = get_param('shared_secret')
    elif grant_type is 'refresh_token':
	# todo implement
	pass
    else:
	## assume its a bearer token flow
        params['assertion'] = secret
    params['grant_type'] = grant_type
    params['format'] = 'json'
    base_url =  get_param('base_url')
    suffix_override =  get_param('suffix_override')
    if suffix_override != None:
        suffix_override = base_url + '/' + suffix_override
    oauthclient = oauth2.oauthclient(params['client_id'], get_param('shared_secret'), base_url)
    sending = oauthclient.toqueryparams(params)
    try: 
	request_token = oauthclient.requestToken(suffix_override, params)
	request_token.update(params);
	if (has_key(request_token,'error')):
	    request_token['error_description'] = setup.get_message(request_token['error'])
    except Exception as e:
	request_token = {}
	request_token.update(params)
	request_token['error'] = "Error occured in oAuth Call ({0})".format(e)
    except ValueError as ve:
	request_token = {}
	request_token.update(params)
	request_token['error'] = "Input Error occured in oAuth Call ({0})".format(ve)
    except:
	request_token = {}
	request_token.update(params)
	request_token['error'] = 'Unknown error'
    if suffix_override != None:	
	request_token['url_used'] = suffix_override + '?' + sendingi
	
	
    else:
	request_token['url_used'] = base_url + '/oauth/request_token?' + sending
    return request_token


@route('/oauth2/callback')
@view('oauth2/callback')
def testcallback():
    values = request_value_dict(['client_id','shared_secret','code','state','error'])
    request_token = testrequesttoken()
    if request_token != None:
    	values.update(request_token)
    	store_session(request_token)
	print request_token
    values['name'] = 'oauth 2 callback'
    return values

@route('/oauth2/useragentflow')
@view('oauth2/useragentflow')
def oauth2_useragentflow():
    return dict(name='oauth 2 useragentflow')

@route('/oauth2/webserverflow')
@view('oauth2/webserverflow')
def oauth2_webserverflow():
    return dict(name='oauth 2 webserverflow')

@route('/oauth2/bearerflow')
@view('oauth2/bearerflow')
def oauth2_bearerflow():
    return dict(name='oauth 2 bearer flow')

@route('/oauth2/bearerflow/submit')
@view('oauth2/callback')
def oauth2_bearerflow_submit():
    values = dict(name='oauth 2 bearer submit flow')
    token_type = get_param('token_type')
    print token_type
    if token_type != None:
        if token_type == 'jwt':
            tojson = {}
            tojson['iss'] = get_param('client_id')
            tojson['prn'] = get_param('username')
	    tojson['aud'] = get_param('aud')
            tojson['exp'] = round(time.time() + 3400,0)
            secret = json.dumps(tojson)
            secret = jwt.encode(tojson, get_param('shared_secret'))
            token_type='JWT'
            grant_type = 'http://oauth.net/grant_type/jwt/1.0/bearer'
            request_token = request_token_call(secret,grant_type,assertion_type=token_type)
            values.update(request_token)
	else:
	    values = {"error":"No token type provided on form"}
    return values



@route('/oauth2/deviceflow')
@view('oauth2/deviceflow')
def oauth2_deviceflow():
    return dict(name='oauth 2 deviceflow')

@route('/oauth2/usernamepasswordflow')
@view('oauth2/usernamepasswordflow')
def oauth2_usernamepasswordflow():
    return dict(name='oauth 2 usernamepasswordflow')

@route('/oauth2/clientcredentialsflow')
@view('oauth2/clientcredentialsflow')
def oauth2_clientcredentialsflow():
    return dict(name='oauth 2 clientcredentialsflow')

@route('/oauth2/assertionflow')
@view('oauth2/assertionflow')
def oauth2_assertionflow():
    return dict(name='oauth 2 assertionflow')
    





########################
## Starts up the web 
## application
#######################
def startweb(host,port,runmode=True):
	bottle.TEMPLATE_PATH.insert(0,os.path.dirname( os.path.realpath( __file__ ))+'/views/')
	app = bottle.default_app()
	session_opts = {
    		'session.type': 'file',
    		'session.cookie_expires': 300,
    		'session.data_dir': './data',
    		'session.auto': True
	}
	app = SessionMiddleware(app,session_opts)
	if runmode:
		run(server=PasteServer,host=host, port=port,app=app)
	return app

