
import sys, os, imp, glob
import unittest

commonlib = './third-party/lib/common/'
sitepkgs = './third-party/lib/site-packages'


sys.path.append(os.path.abspath(commonlib))
sys.path.append(os.path.abspath(sitepkgs))

for currentf in glob.glob( os.path.join(sitepkgs, '*') ):
       	if os.path.isdir(currentf):
		print( ' adding ' + currentf)
		sys.path.append(os.path.abspath(currentf))


## starts up the application and configures it 
import toasterutils

if sys.argv and len(sys.argv) > 1:
        app = sys.argv[1]
	sys.path.append(os.path.abspath('./apps/'+app))
	sys.path.append(os.path.abspath('./tests/'+app))

	testname = None	
	testclassname = None
	if (len(sys.argv) >= 3):
		testname = sys.argv[2]
		if (len(sys.argv) > 3):
			testclassname = sys.argv[3]

	
	importname = 'testsuite'
	if (testname != None):
		importname = testname

	moduleLoaded = toasterutils.loadImportName(importname)
	testsuite = toasterutils.loadImportName('testsuite')
	
	print('running tests from '+app+' - ' + importname)
	config = None
	cfgfile = './conf/%s.cfg' % app
	if (os.path.exists(cfgfile)):
		from config import Config
		f = file(cfgfile)
		config = Config(f)

	testsuite.cfg = config
	suite = None
	if (testname == None or testclassname == None):
		suite = unittest.TestLoader().loadTestsFromModule(moduleLoaded)
                if(testname == None):
                        ts = unittest.TestSuite()
                        ts.addTests(suite)
                        ts.addTests(moduleLoaded.AllTests())
                        suite = ts
	else:
		suite = unittest.TestLoader().loadTestsFromTestCase(moduleLoaded[testclassname])
	unittest.TextTestRunner(verbosity=2).run(suite)	
else:
	print('must provide an application name ')
        
