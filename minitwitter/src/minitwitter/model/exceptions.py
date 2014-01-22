'''
Created on Jan 22, 2014

@author: anya
'''

class TwitterException(Exception):
    """
    Super class for all exceptions raised in twitter app.
    """
    pass

class InputError(TwitterException):
    """
    Super class for all exceptions caused by wrong input (asking feed for non existing users etc.)
    """

class UserNotExistsException(InputError):
    """
    Raised in case of a attempt to perform user action for non existing user.
    """
    def __init__(self, user_id):
        self.message = "User %d does not exist!" %user_id
    
class AlreadyFollowingException(InputError):
    """
    Raised in case of a follow request for follower which is already following the followee.
    """
    def __init__(self, follwer_id, followee_id):
        InputError.__init__(self)
        self.message = "User #%d is already following user #%d" %(follwer_id, followee_id)
        
class NotFollowingException(InputError):
    """
    Raised in case of a un follow request user that is not following the followee.
    """
    def __init__(self, follwer_id, followee_id):
        Exception.__init__(self)
        self.message = "User #%d is not following user #%d" %(follwer_id, followee_id)
        
            
class DbException(Exception):
    """
    Raised in case there is a problem with the db.
    """
    pass
            