
import threading

_thread_locals = threading.local()

def get_old_key():

    return getattr(_thread_locals,'old_key',None)

class StoreOldKeyMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self,req):

        _thread_locals.old_key = req.session.session_key

        response = self.get_response(req)

        return response