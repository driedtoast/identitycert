import logging, os, errno

LOG_FILENAME = '/var/log/pytoaster'

def logmessage(message):
	logging.info(message)
	
def logerror(message):
	logging.error(message)	

dirname = os.path.dirname(LOG_FILENAME)
try:
	os.makedirs(dirname)
except OSError as exc:
	if exc.errno == errno.EEXIST:
		pass
	else: raise
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
