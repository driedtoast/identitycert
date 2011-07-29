from bottle import request, response
import cgi, os
import cgitb; cgitb.enable()
import setup
import M2Crypto

MBSTRING_FLAG = 0x1000
MBSTRING_ASC  = MBSTRING_FLAG | 1
MBSTRING_BMP  = MBSTRING_FLAG | 2

def empty_callback ( *args):
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
	pkey = M2Crypto.EVP.PKey ( md='sha1')
	pkey.assign_rsa ( key )
	self.createPublicCert(pkey,dirn)
	
	pass
    def createPublicCert(self,pkey, dirn):
	## create request
	x509Request = M2Crypto.X509.Request ()
	X509ReqName = M2Crypto.X509.X509_Name ()
	X509ReqName.add_entry_by_txt ( field='C',            type=MBSTRING_ASC, entry='austria',               len=-1, loc=-1, set=0 )    # country name
	X509ReqName.add_entry_by_txt ( field='SP',           type=MBSTRING_ASC, entry='kernten',               len=-1, loc=-1, set=0 )    # state of province name
	X509ReqName.add_entry_by_txt ( field='L',            type=MBSTRING_ASC, entry='stgallen',              len=-1, loc=-1, set=0 )    # locality name
	X509ReqName.add_entry_by_txt ( field='O',            type=MBSTRING_ASC, entry='labor',                 len=-1, loc=-1, set=0 )    # organization name
	X509ReqName.add_entry_by_txt ( field='OU',           type=MBSTRING_ASC, entry='it-department',         len=-1, loc=-1, set=0 )    # organizational unit name
	X509ReqName.add_entry_by_txt ( field='CN',           type=MBSTRING_ASC, entry='Certificate client',    len=-1, loc=-1, set=0 )    # common name
	X509ReqName.add_entry_by_txt ( field='Email',        type=MBSTRING_ASC, entry='user@localhost',        len=-1, loc=-1, set=0 )    # pkcs9 email address
	X509ReqName.add_entry_by_txt ( field='emailAddress', type=MBSTRING_ASC, entry='user@localhost',        len=-1, loc=-1, set=0 )    # pkcs9 email address     
	x509Request.set_subject_name( X509ReqName )
	x509Request.set_pubkey ( pkey=pkey )
	x509Request.sign ( pkey=pkey, md='sha1' )

	## create x509
	x509Certificate =  M2Crypto.X509.X509 ()
	x509Certificate.set_version ( 0 )
	ASN1 = M2Crypto.ASN1.ASN1_UTCTIME ()
	ASN1.set_time ( 500 )
	x509Certificate.set_not_before( ASN1 )
	x509Certificate.set_not_after( ASN1 )
	x509Certificate.set_pubkey ( pkey=pkey )
	x509Name = x509Request.get_subject ()
	x509Certificate.set_subject_name( x509Name )
	x509Name = M2Crypto.X509.X509_Name ( M2Crypto.m2.x509_name_new () )
	x509Name.add_entry_by_txt ( field='C',            type=MBSTRING_ASC, entry='germany',               len=-1, loc=-1, set=0 )    # country name
	x509Name.add_entry_by_txt ( field='SP',           type=MBSTRING_ASC, entry='bavaria',               len=-1, loc=-1, set=0 )    # state of province name
	x509Name.add_entry_by_txt ( field='L',            type=MBSTRING_ASC, entry='munich',                len=-1, loc=-1, set=0 )    # locality name
	x509Name.add_entry_by_txt ( field='O',            type=MBSTRING_ASC, entry='sbs',                   len=-1, loc=-1, set=0 )    # organization name
	x509Name.add_entry_by_txt ( field='OU',           type=MBSTRING_ASC, entry='it-department',         len=-1, loc=-1, set=0 )    # organizational unit name
	x509Name.add_entry_by_txt ( field='CN',           type=MBSTRING_ASC, entry='Certificate Authority', len=-1, loc=-1, set=0 )    # common name
	x509Name.add_entry_by_txt ( field='Email',        type=MBSTRING_ASC, entry='admin@localhost',       len=-1, loc=-1, set=0 )    # pkcs9 email address
	x509Name.add_entry_by_txt ( field='emailAddress', type=MBSTRING_ASC, entry='admin@localhost',       len=-1, loc=-1, set=0 )    # pkcs9 email address
	x509Certificate.set_issuer_name( x509Name )
	x509Certificate.sign( pkey=pkey, md='sha1' )
	x509Certificate.save(dirn + '/public.pem')
	

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
    
