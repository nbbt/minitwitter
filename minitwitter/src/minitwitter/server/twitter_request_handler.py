'''
Created on Jan 22, 2014

@author: anya
'''
from tornado.web import RequestHandler
from httplib import BAD_REQUEST, INTERNAL_SERVER_ERROR, SERVICE_UNAVAILABLE
from minitwitter.model.exceptions import DbException, InputError


class TwitterRequestHandler(RequestHandler):
    def initialize(self, twitter_model):
        """
        @param twitter_model: The twitter object that is responsible for validation and the DB 
        operations.
        @type twitter_model: TwitterModel
        """
        self.twitter_model = twitter_model
        
    def _validate_user_id(self, str_user_id):
        """
        Make sure the given user id can be converted to int (further validation - in the model).
        If not, raise exception.
        @param str_user_id:
        @type str_user_id:
        @return: user_id conveted to int.
        @rtype: int.
        """
        try:
            return int(str_user_id)
        except ValueError:
            raise BadUserIdException;

    def _validate_user_id_from_url(self, str_user_id):
        """
        Make sure the given user id can be converted to int (further validation - in the model).
        If not, raise exception suitable for the case of bad user id from url.       
        @param str_user_id:
        @type str_user_id:
        @return: user_id conveted to int.
        @rtype: int.        
        """
        try:
            return int(str_user_id)
        except ValueError:
            raise BadUserIdFromUrlException;
                    
    def _handle_client_error(self, e):
        """
        Handle a case when bad user_id argument is passed (for example - cant be converted to int). 
        """
        self.set_status(BAD_REQUEST)
        self._write_custom_body(e.message)
        
    def _handle_bad_user_id_from_url(self):
        """
        Handle a case when user_id parsed from the url is not legal. This is not supposed to 
        happen unless there is a bug (because of the url mapping using regex).
        """
        self.set_status(INTERNAL_SERVER_ERROR)
        
    def _handle_db_exception(self):
        self.set_status(SERVICE_UNAVAILABLE)
        self._write_custom_body("Db is down.")

    def _write_custom_body(self, message):
        """
        Return simple custom html body with the given message.
        @param message:
        @type message:
        """
        body = "%d: %s" %(self.get_status(), message)
        self.finish("<html><body>%s</body></html>" %body)
                         
class BadUserIdException(Exception):
    pass

class BadUserIdFromUrlException(Exception):
    pass

def handle_exceptions_decorator(method):
    def wrapped_method(self, *args):
        try:
            method(self, *args)
        except BadUserIdFromUrlException:
            self._handle_bad_user_id_from_url()
        except DbException:
            self._handle_db_exception()
        except (InputError, BadUserIdException) as e:
            self._handle_client_error(e)
    
    return wrapped_method
        
