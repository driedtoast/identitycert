import sys, os
from config import Config

## directories
basedir = sys.path[0]
staticdir = basedir + '/static'
confdir = basedir + '/conf'
datadir = basedir + '/data'
jobsdir = None

## configurations
cfg = None

## creates data dir if it doesn't exist
def setupdata():
    if(os.path.exists(datadir) == False):
        os.mkdir(datadir)
