from bottle import request, response
import cgi, os
import cgitb; cgitb.enable()
import setup
import M2Crypto

def empty_callback ():
    return

## Gets a list of keys
## Generates keys and stores them
class KeyService(object):
    def __init__(self):
	pass
    
    def list(self):
	l = []
	for root, dirs, files in os.walk(setup.keydir):
	    for name in dirs:       
		l.append(name)
        return l
    
    def addCert(self, name):
	dirn = setup.keydir+'/'+name
	if os.path.exists(dirn) == False:
	    os.mkdir(dirn)
	key = M2Crypto.RSA.gen_key (256, 65537,empty_callback)
	key.save_key (dirn + '/private.pem',None)
	key.save_pub_key (dirn + '/public.pem')
	## create keys
	pass 

## simple wrapper for session stuff
class SessionService(object):
    
    def __init__(self):
        pass
    
    def get_session(self):
        s = request.environ.get('beaker.session')
        return s
    
    def store(self, map, save=True):
        sess = self.get_session()
        for k,v in map.items():
            sess[k] = v
        if(save):
            sess.save()
    def get_attr(self,name):
        sess = self.get_session()
        if name in sess:
            return sess[name]
        return None
    def put_attr(self, name, value):
        sess = self.get_session()
        sess[name] = value
        sess.save()


def get_file(name):
    #try:
	#print request()[name]
	#for k, v in request().files.iteritems():
	#    print k + " - " + v
        
	#filereq = request().files.get(name)
	#return filereq.file.read()
    #except Exception as e:
	#print e
    return None

session = SessionService()


## Gets param from session or session    
def get_param(name):
    if request.GET and name in request.GET:
        return request.GET[name]
    if request.POST and name in request.POST:
        return request.POST[name]
    return session.get_attr(name)
    
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
    
