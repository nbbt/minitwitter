'''
Created on Jan 22, 2014

@author: anya
'''
from minitwitter.model.exceptions import UserNotExistsException, AlreadyFollowingException,\
    NotFollowingException


class TwitterModel(object):
    """
    A Twitter model. Holds the state of the Twitter application.
    Responsible on validation and processing requests using given db client.
    Exposes an API for actions on the Twitter application.
    Adds validation layer to the simple TwitterDbClient.
    """
    
    def __init__(self, db_client):
        """
        C'tor.
        @param db_client: Client for db access.
        @type db_client: TwitterDbClientInterface.
        """
        self.db_client = db_client
        
    def create_new_user(self, name):
        """
        Create a new Twitter user with the given name.
        @param name: The name of the user.
        @type name: str.
        """
        self.db_client.create_new_user(name)
            
    def post_message(self, user_id, message):
        """
        @param user_id: The id of the user the post belongs to.
        @type user_id: int.
        @param message: The message to post.
        @type message: str (up to 1000 chars!)
        """
        self._validate_user_exists(user_id)
        self.db_client.post_message(user_id, message)
        
    def follow(self, follower_id, followee_id):
        """
        Add the followee to the list of followed users of the follower.
        
        @param follower_id: The id of the follower.
        @type follower_id: int.
        @param followee_id: The id of the user which is followed.
        @type followee_id: int.
        """
        
        self._validate_user_exists(follower_id)
        self._validate_user_exists(followee_id)
        
        if self.db_client.is_following(follower_id, followee_id):
            raise AlreadyFollowingException(follower_id, followee_id)
        
        self.db_client.follow(follower_id, followee_id)            
    
    def unfollow(self, follower_id, followee_id):
        """
        Remove the followee from the list of followed users of the follower.
        @param follower_id: The id of the following user.
        @type follower_id: int.
        @param followee_id: The id of the followed user.
        @type followee_id: int.
        """
        self._validate_user_exists(follower_id)
        self._validate_user_exists(followee_id)
        
        if not self.db_client.is_following(follower_id, followee_id):
            raise NotFollowingException(follower_id, followee_id)
        
        self.db_client.unfollow(follower_id, followee_id)            
    
         
    def get_global_feed(self):
        """
        Return the posts of all users.
        @rtype: list of tuples.
        """
        return self.db_client.get_global_feed()
    
    
    def get_feed_for_user(self, user_id):
        """
        Return the the posts of all users followed by the user with the given user_id.
        @param user_id: The follower for which the feed is requested.
        @type user_id: int.
        @return: All posts of the users that are followed by the user with the given id.
        @rtype: int.
        """
        self._validate_user_exists(user_id)
        return self.db_client.get_feed_for_user(user_id)
    
    def _validate_user_exists(self, user_id):
        """
        Check if the user exists in the db. If not, raise exception.
        @param user_id: The user id to check.
        @type user_id: int
        """
        if not self.db_client.user_exists(user_id):
            raise UserNotExistsException(user_id)