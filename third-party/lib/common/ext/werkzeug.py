
import werkzeug

from werkzeug import *
import bottle


class WerkzeugDebugger(DebuggedApplication):
    """ A subclass of :class:`werkzeug.debug.DebuggedApplication` that obeys the
        :data:`bottle.DEBUG` setting. """

    def __call__(self, environ, start_response):
        if bottle.DEBUG:
            return DebuggedApplication.__call__(self, environ, start_response)
        return self.app(environ, start_response)

            
class WerkzeugPlugin(object):
    """ This plugin adds support for :class:`werkzeug.Response`, all kinds of
        :module:`werkzeug.exceptions` and provides a thread-local instance of
        :class:`werkzeug.Request`. It basically turns Bottle into Flask. """

    name = 'werkzeug'

    def __init__(self, evalex=False, request_class=werkzeug.Request,
                       debugger_class=WerkzeugDebugger):
        self.request_class = request_class
        self.debugger_class = debugger_class
        self.evalex=evalex
        self.app = None

    def setup(self, app):
        self.app = app
        if self.debugger_class:
            app.wsgi = self.debugger_class(app.wsgi, evalex=self.evalex)
            app.catchall = False

    def apply(self, callback, context):
        def wrapper(*a, **ka):
            environ = bottle.request.environ
            bottle.local.werkzueg_request = self.request_class(environ)
            try:
                rv = callback(*a, **ka)
            except werkzeug.exceptions.HTTPException, e:
                rv = e.get_response(environ)
            if isinstance(rv, werkzeug.BaseResponse):
                rv = bottle.HTTPResponse(rv.iter_encoded(), rv.status_code, rv.header_list)
            return rv
        return wrapper

    @property
    def request(self):
        ''' Return a local proxy to the current :class:`werkzeug.Request`
            instance.'''
        return werkzeug.LocalProxy(lambda: bottle.local.werkzueg_request)
    
    def __getattr__(self, name):
        ''' Convenient access to werkzeug module contents. '''
        return getattr(werkzeug, name)


Plugin = WerkzeugPlugin