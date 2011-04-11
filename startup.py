
import sys, os, imp, glob

commonlib = './third-party/lib/common/'
sitepkgs = './third-party/lib/site-packages'


sys.path.append(os.path.abspath(commonlib))
sys.path.append(os.path.abspath(sitepkgs))

## make sure the sitepkgs are added
for currentf in glob.glob( os.path.join(sitepkgs, '*') ):
        if os.path.isdir(currentf):
                sys.path.append(os.path.abspath(currentf))



## starts up the application and configures it 

if sys.argv:
        app = sys.argv[1]
	sys.path.append(os.path.abspath('./apps/'+app))
	importname = 'application'
	# __import__(importname)
	try:
        	moduleLoaded =  sys.modules[importname]
    	except KeyError:
        	pass
	fp, pathname, description = imp.find_module(importname)

    	try:
        	moduleLoaded = imp.load_module(importname, fp, pathname, description)
    	finally:
        	# Since we may exit via an exception, close fp explicitly.
        	if fp:
           		fp.close()
	print('starting up '+app)
	config = None
	cfgfile = './conf/%s.cfg' % app
	if (os.path.exists(cfgfile)):
		from config import Config
		f = file(cfgfile)
		config = Config(f)
	moduleLoaded.start(sys.argv[2:],config)	
else:
	print('must provide an application name ')
        

