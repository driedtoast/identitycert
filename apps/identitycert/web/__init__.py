from bottle import route, run, abort, debug
from bottle import mako_view as view
from bottle import send_file, redirect
from bottle import PasteServer
from bottle import request, response
from beaker.middleware import SessionMiddleware
import jwt
#import ext.werkzeug
import bottle
import time
import os, sys,  traceback
import setup
import lib.oauth2 as oauth2
import lib.saml2 as saml2
import json
import setup
import lib.services as services
import saml

cfg = None


##############################################################
### static file methods
############################################################
	
@route('/static/keys/:dir/:filename')
def static_file_keys(dir,filename):
	## request.environ['HTTP_IF_MODIFIED_SINCE'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(100))
	send_file(filename, root=setup.keydir+'/'+dir, mimetype='text/plain')	

##############################################################
### UI methods
############################################################

### dashboard
@route('/')
@view('index')
def index():
    return dict(name='index')

### cert management
@route('/cert/list')
@view('cert/list')
def certlist():
    service = services.KeyService()	
    list = service.list()
    return dict(name='cert list', certs=list)
    
@route('/cert/add')
@view('cert/add')
def certadd():
    return dict(name='add cert')
    
@route('/cert/save')
@view('cert/list')
def certsave():
    service = services.KeyService()
    name = services.get_param('name')
    service.addCert(name)
    list = service.list()
    return dict(name='add cert',certs=list)
    
    

### OAUTH 2 flows

@route('/oauth2/testauthorize')
@view('oauth2/testauthorize')
def testauthorize():
    ## process flow for oauth
    tostore = services.request_value_dict(['client_id','shared_secret','redirect_uri','base_url','state','suffix_override','token_type','scope'])
    params = services.dict_subset(tostore,['client_id','redirect_uri','state','scope'])
    params['response_type'] = 'code'
     
    services.session.store(tostore, False)
    if services.session.get_attr('state') is None:
	services.session.put('state',services.session.get_session().id)
        params['state'] = services.session.get_attr('state')
    
    consumer_key = services.get_param('client_id')
    shared_secret = services.get_param('shared_secret')
    base_url =  services.get_param('base_url')
    
    oauthclient = oauth2.oauthclient(consumer_key, shared_secret, base_url)
    redirect_url = oauthclient.authorizeRedirect(params=params)
    return dict(link=redirect_url )

@route('/oauth2/callback')
@view('oauth2/callback')
def testcallback():
    values = services.request_value_dict(['client_id','shared_secret','code','state','error','scope'])
    request_token = oauth2.service.request_token_call()
    if request_token != None:
    	values.update(request_token)
    	services.session.store(request_token)
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
    service = services.KeyService()	
    list = service.list()
    return dict(name='oauth 2 bearer flow', certs=list)

@route('/oauth2/bearerflow/submit',method='POST')
@view('oauth2/callback')
def oauth2_bearerflow_submit():
    ## clean out the values, hmm beaker might need to be invalidated	
    services.session.clear_attr(['error','access_token','refresh_token','error_description','state','code'])
    values = dict(name='oauth 2 bearer submit flow')
    token_type = services.get_param('token_type')
    if token_type != None:
	client_id = services.get_param('client_id')
        username = services.get_param('username')
	audience = services.get_param('aud')
	callback = services.get_param('redirect_uri')
	keysign = services.get_param('keysign')
	keyname = services.get_param('keyname')
	privateKey = None
	publicKey = None
	if(keysign != None and keysign == 'on' and keyname != None):
		privateKeyFile = open(setup.keydir  +'/' + keyname + '/private.pem', 'r')
		privateKey = privateKeyFile
		publicKeyFile = open(setup.keydir +'/' + keyname + '/public.pem', 'r')
		publicKey = publicKeyFile
	if token_type == 'jwt':
            tojson = {}
            tojson['iss'] = client_id
            tojson['prn'] = username
	    tojson['aud'] = audience
	    tojson['iat'] = round(time.time())
            tojson['exp'] = round(time.time() + 300,0)
            secret = json.dumps(tojson)
	    key = services.get_param('shared_secret')
	    algorithm = 'HS256' # RS256
	    if(privateKey != None):
		key = setup.keydir  +'/' + keyname + '/private.pem' # setup.staticdir + '/mycert-private.pem'
		algorithm = 'RS256' 
            secret = jwt.encode(tojson,key,algorithm )
            request_token = oauth2.service.request_token_call(secret,'urn:ietf:params:oauth:grant-type:jwt-bearer',assertion_type='JWT')
            values.update(request_token)
	elif token_type == 'saml' and keysign:
	    assertion = saml2.service.buildAssertion(username, audience, client_id, callback)
	    secret = saml2.service.encodeAssertion(assertion,setup.keydir  +'/' + keyname + '/private.pem', publicKey.read())#setup.keydir  +'/' + keyname + '/public.pem')
	    request_token = oauth2.service.request_token_call(secret,'urn:ietf:params:oauth:grant-type:saml2-bearer',assertion_type='SAML')
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
	#werkzeug = ext.werkzeug.Plugin()
	#app.install(werkzeug)
	# services.requestprovider=werkzeug
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

