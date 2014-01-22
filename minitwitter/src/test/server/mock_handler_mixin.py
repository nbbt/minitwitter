'''
Created on Jan 22, 2014

@author: anya
'''
import json

class MockHandlerMixin():
    """
    Overrides method of HttpRequestHandler to enable pure unit tesing of handler's logic.
    Mock handlers should inherit from this class in addition to the specific handler in test.
    For example:
    
    class MockCreateUserHandler(MockHandlerMixin, CreateUSerHandler):
        ...
    Note - the order of the super classes is important in order to allow the Mixin class to 
    override the necessary method (Not the best practice but better then writing this class
    logic 10 times over).
    
    """
    def __init__(self, twitter_model, args=None):
        self.args = args
        self.initialize(twitter_model)
        self.response_text = ""
        self.status = None
        
    def write(self, chunk):
        self.response_text += json.dumps(chunk)

    def finish(self, chunk):
        self.response_text += json.dumps(chunk)

    def write_error(self, status_code, **kwargs):
        self.error_code = status_code

    def get_argument(self, name):
        return self.args[name]
    
    def set_status(self, status_code):
        self.status = status_code
        
    def get_status(self):
        return self.status
    
    def no_errors(self):
        if self.status is None:
            return True
        if self.status % 100 in [4,5]:
            return False
        return True
        