import sys, os
from config import Config
import gettext

## directories
basedir = sys.path[0]
staticdir = basedir + '/static'
confdir = basedir + '/conf'
datadir = basedir + '/data'
jobsdir = None


msgConfFile = file( staticdir + '/messages.cfg')
msgConf = Config(msgConfFile)


## configurations
cfg = None

## creates data dir if it doesn't exist
def setupdata():
    if(os.path.exists(datadir) == False):
        os.mkdir(datadir)


def get_message(key):
    return msgConf[key]
    
