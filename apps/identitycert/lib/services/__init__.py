from bottle import request, response
import cgi, os, time
import cgitb; cgitb.enable()
import setup
import subprocess
import M2Crypto
from OpenSSL import crypto

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
	    
	## hackeriffic, something is odd with the way m2crypto and openssl generate keys related to how this works
	# openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout private.pem -out public.pem
	# args = ['openssl','req','-x509','-nodes','-days', '365', '-newkey', 'rsa:1024', '-keyout', dirn + '/private.pem', '-out',dirn + '/public.pem','-batch']
	# subprocess.call(args)
	# openssl x509 -in public.pem -out public_der.pem -outform der
	# args = ['openssl','x509','-in',dirn + '/public.pem','-out',dirn + '/public_der.pem','-outform','der']
	# subprocess.call(args)
	pkey = crypto.PKey()
	pkey.generate_key(crypto.TYPE_RSA, 512)
        digest='md5'
       
	req = crypto.X509Req()
	subj = req.get_subject()
	subj.CN='Certificate Authority'
	 
	req.set_pubkey(pkey)
	req.sign(pkey, digest)
       
       
	cert = crypto.X509()
	cert.set_serial_number(0)
	cert.gmtime_adj_notBefore(0)
	cert.gmtime_adj_notAfter(60*60*24*365*5)
	cert.set_issuer(req.get_subject())
	cert.set_subject(req.get_subject())
	cert.set_pubkey(req.get_pubkey())
	cert.sign(pkey, digest)
	
	open(dirn + '/private.pem', 'w').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
	open(dirn + '/public.pem', 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
	pubkey = M2Crypto.X509.load_cert(dirn + '/public.pem')
	pubkey.save(dirn + '/public_der.pem',format=M2Crypto.X509.FORMAT_DER)
	# THIS SEGFAULTS
	# key = M2Crypto.RSA.gen_key (1024, 65537,empty_callback)
	# key.save_key (dirn + '/private.pem',None)
	# self.createPublicCert(key,dirn)

    def createPublicCert(self,key, dirn):
	pkey = M2Crypto.EVP.PKey ()
	pkey.assign_rsa ( key )
	## create request
	x = M2Crypto.X509.Request ()
	x.set_pubkey(pkey)
	name = x.get_subject()
	name.C="US"
	name.CN = "Identity Cert Group"
	ext1 = M2Crypto.X509.new_extension('subjectAltName', 'DNS:foobar.example.com')
	ext2 = M2Crypto.X509.new_extension('nsComment', 'Hello there')
	extstack = M2Crypto.X509.X509_Extension_Stack()
	extstack.push(ext1)
	extstack.push(ext2)
	x.add_extensions(extstack)
	x.sign(pkey,'md5')
	x.save_pem( dirn + '/public.pem')
	
	pkey = x.get_pubkey()
        sub = x.get_subject()
        cert = M2Crypto.X509.X509()
        cert.set_serial_number(1)
        cert.set_version(2)
        cert.set_subject(sub)
        t = long(time.time()) + time.timezone
        now = M2Crypto.ASN1.ASN1_UTCTIME()
        now.set_time(t)
        nowPlusYear = M2Crypto.ASN1.ASN1_UTCTIME()
        nowPlusYear.set_time(t + 60 * 60 * 24 * 365)
        cert.set_not_before(now)
        cert.set_not_after(nowPlusYear)
        issuer = M2Crypto.X509.X509_Name()
        issuer.C = "US"
        issuer.CN = "Identity Cert Group"
        cert.set_issuer(issuer)
        cert.set_pubkey(pkey) 
        ext = M2Crypto.X509.new_extension('basicConstraints', 'CA:TRUE')
        cert.add_ext(ext)
        cert.sign(pkey, 'md5')
	cert.save( dirn + '/public_der.pem',format=M2Crypto.X509.FORMAT_DER )

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
    def clear_attr(self,names):
	sess = self.get_session()
	for name in names:
	    if name in sess:
	        del sess[name]

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
    
