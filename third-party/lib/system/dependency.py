import sys, os, subprocess
sys.path.append(os.path.abspath('../common'))
import urllib, tarfile
from config import Config

downloadpath='../../../temp'


## Resolves the dependencies
def main(argz=None):
	# the main code goes here
	filename = argz[0]
        configdir = os.path.dirname(filename)
	downloadpath = configdir + '/../temp'

	f = file(filename)
	cfg = Config(f)
	for m in cfg.dependencies:
		s = 'Resolving  %s  %s' % (m.name, m.version)
		try:
			if(os.path.exists(downloadpath) is True): 
				os.removedirs(downloadpath)
				
			if(os.path.exists(downloadpath) != True): 
				os.makedirs(downloadpath)
			fname = os.path.basename(m.location)
			ftype = 'tar'
			if(fname.find('.git') != -1):
				ftype = 'git'
                        fname = fname.replace('.tar','')
                        fname = fname.replace('.gz','')
                        fname = fname.replace('.tgz','')
                        fname = fname.replace('.git','')
			basepkgname= '%s/%s' % (downloadpath, fname)
			if(ftype is 'git'):
				subprocess.call(['git','clone',m.location,basepkgname])
			else:
				savelocation = '%s.tar.gz' % (basepkgname)
				urllib.urlretrieve(m.location, savelocation) 
     				print('saved url ' + m.location + ' to ' + savelocation) 
				tar = tarfile.open(savelocation)
				tar.extractall(downloadpath)
				tar.close()
			subprocess.call([argz[1], basepkgname, configdir]) 
		except IOError, e:
     			print(e) 

 
if __name__ == "__main__":
	main(sys.argv[1:])
