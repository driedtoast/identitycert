
from bottle import request, response

session = SessionService()

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

## Gets param from session or session    
def get_param(name):
    if name in request.GET:
        return request.GET[name]
    if name in request.POST:
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
    