import logging

LOG_FILENAME = '/var/log/pytoaster'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

def logmessage(message):
	logging.info(message)
	
def logerror(message):
	logging.error(message)	
