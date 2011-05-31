# import db as db
import web as web
import setup
from bottle import route, run, abort, debug



debug(True)

#############
### start method
#############
def start(argv=None,config=None, runmode=True):
	setup.cfg = config
	# db.cfg = config.db
	# print db.check()
	## TODO put startup logic here
	web.cfg = config
	return web.startweb(host=config.server.hostname, port=config.server.port, runmode=runmode)
