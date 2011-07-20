import urlparse
import json
import oauth2 as oauth
import setup
import lib.services as services
import collections


##
# Simplifies the use of the oauth client just a bit
# 
##
class oauthclient(object):

    client = None
    consumer = None

    def __init__(self, consumer_key, consumer_secret, base_url=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_url = base_url

    def get_consumer(self):
        if self.consumer is None:
            self.consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
        return self.consumer

    def get_client(self):
        if self.client != None:
            return self.client
        consumer = self.get_consumer()
        self.client = oauth.Client(consumer)
        return self.client

    ##
    # example url input:
    #     'http://twitter.com/oauth/request_token'
    #      defaults to base url + /request_token
    #  returns:
    #      oauth_token        = request_token['oauth_token']
    #      oauth_token_secret = request_token['oauth_token_secret']
    def requestToken(self, request_token_url=None, params=None):
        if (request_token_url is None) and (self.base_url != None):
            request_token_url = "%s/request_token" % self.base_url
        client = self.get_client()
        extra = self.toqueryparams(params)
	
	format = None
        if params != None:
            if 'format' in params:
		format = params['format']
        resp, content = client.request(uri=request_token_url, method="POST",body=extra)
        if resp['status'] != '200':
	    return (None,content)
            #raise Exception("Invalid response %s to %s" % (resp['status'],request_token_url))
	if format is 'json':
		self.request_token = {}
        	jsonobj = json.JSONDecoder().decode(content)
		for k,v in jsonobj.items():
			self.request_token[str(k)] = v
			
	else:
        	self.request_token = dict(urlparse.parse_qsl(content))
	self.request_token['actual_response'] = content
        return self.request_token

    def toqueryparams(self,params):
	extra = None
	if params != None:
            for k,v in params.items():
                if extra is None:
                    extra = "%s=%s" %(k, v)
                else:
                    extra = extra + "&%s=%s" %(k, v)
	return extra
    ##
    # example url input - 'http://twitter.com/oauth/authorize'
    # request token from previous step
    # defaults 
    ##
    def authorizeRedirect(self, authorize_url=None, request_token=None, params=None):
        if request_token is None and hasattr(self,'request_token'):
            request_token = self.request_token
        if(authorize_url is None) and (self.base_url != None):
            authorize_url = "%s/authorize" % self.base_url
	start = True
	if request_token != None:
		start = False
        	url = "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
	else:
		url = authorize_url
        if params != None:
            for k,v in params.items():
		if start:
                	extra = "?%s=%s" %(k, v)
			start = False
		else:
                	extra = "&%s=%s" %(k, v)
                url = url + extra    
        return url;


    ##
    # example input:
    #   access_token_url = 'http://twitter.com/oauth/access_token'
    # returns a dictionary with:
    #   oauth_token        = access_token['oauth_token']
    #   oauth_token_secret = access_token['oauth_token_secret']

    def accessToken(self,access_token_url=None, oauth_verifier=None, request_token=None):
        if request_token is None:
            request_token  = self.request_token
        token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        if oauth_verifier != None:
            token.set_verifier(oauth_verifier)
        if(access_token_url is None) and (self.base_url != None):
            access_token_url = "%s/access_token" % self.base_url
        client = oauth.Client(self.get_consumer(), token)
        resp, content = client.request(access_token_url, "POST")
        access_token = dict(urlparse.parse_qsl(content))
	access_token['actual_response'] = content
        return  access_token


### wraps some of the auth calls for the web UI
class OAuthService(object):
    
    def __init__(self):
	pass
    
    def request_token_call(self,secret=None,grant_type='authorization_code',assertion_type=None):
	## process flow for oauth
	params = services.request_value_dict(['client_id','redirect_uri'])
	if grant_type is 'authorization_code':
	    params['code'] = services.get_param('code')
	    params['client_secret'] = services.get_param('shared_secret')
	elif grant_type is 'refresh_token':
	    # todo implement
	    pass
	else:
	    ## assume its a bearer token flow
	    params['assertion'] = secret
	params['grant_type'] = grant_type
	params['format'] = 'json'
	base_url =  services.get_param('base_url')
	suffix_override =  services.get_param('suffix_override')
	if suffix_override != None:
	    suffix_override = base_url + '/' + suffix_override
	client = oauthclient(params['client_id'], services.get_param('shared_secret'), base_url)
	sending = client.toqueryparams(params)
	try:
	    request_token = client.requestToken(suffix_override, params)
	    request_token.update(params);
	    if ('error' in request_token):
		request_token['error_description'] = setup.get_message(request_token['error'])
	except Exception as e:
	    request_token = {}
	    request_token.update(params)
	    request_token['error'] = "Error occured in oAuth Call ({0})".format(e)
	    print (e)
	except ValueError as ve:
	    request_token = {}
	    request_token.update(params)
	    request_token['error'] = "Input Error occured in oAuth Call ({0})".format(ve)
	except:
	    request_token = {}
	    request_token.update(params)
	    request_token['error'] = 'Unknown error'
	if suffix_override != None:	
	    request_token['url_used'] = suffix_override + '?' + sending
	else:
	    request_token['url_used'] = base_url + '/oauth/request_token?' + sending
	return request_token

service = OAuthService()
