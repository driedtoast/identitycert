from bottle import route, run, abort, debug
from logger import logmessage, logerror


debug(True)


@route('/helloworld')
def syncrepodata():
        logmessage('getting called ')
        return 'Hello World'




#############
### start method
#############
def start(argv=None):
   	print argv
	run(host='127.0.0.1', port=8099)

