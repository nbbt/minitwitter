'''
Created on Jan 22, 2014

@author: anya
'''


class TwitterDbClientInterface(object):
    """
    Contains all methods that must be implemented by a data base client for Twitter.
    The database client is not responsible on validating the requests, it assumes all the given
    parameters and the requested operations are valid.
    """
    
    def create_new_user(self, name):
        """
        Create a new Twitter user with the given name.
        @param name: The name of the user.
        @type name: str.
        """
        raise NotImplementedError()
            
    def post_message(self, user_id, message):
        """
        @param user_id: The id of the user the post belongs to.
        @type user_id: int.
        @param message: The message to post.
        @type message: str (up to 1000 chars!)
        """
        raise NotImplementedError()
        
    def follow(self, follower_id, followee_id):
        """
        Add the followee to the list of followed users of the follower.
        
        @param follower_id: The id of the follower.
        @type follower_id: int.
        @param followee_id: The id of the user which is followed.
        @type followee_id: int.
        """
        raise NotImplementedError()
    
    def unfollow(self, follower_id, followee_id):
        """
        Remove the followee from the list of followed users of the follower.
        @param follower_id: The id of the following user.
        @type follower_id: int.
        @param followee_id: The id of the followed user.
        @type followee_id: int.
        """
        raise NotImplementedError()
         
    def get_global_feed(self):
        """
        Return the posts of all users.
        @rtype: list of tuples.
        """
        raise NotImplementedError()
    
    
    def get_feed_for_user(self, user_id):
        """
        Return the the posts of all users followed by the user with the given user_id.
        @param user_id: The follower for which the feed is requested.
        @type user_id: int.
        @return: All posts of the users that are followed by the user with the given id.
        @rtype: int.
        """
        raise NotImplementedError()
    
    def user_exists(self, user_id):
        """
        @param user_id: The id of the user to check if exists.
        @type user_id: int.
        @return: True if the user exists in the db. False otherwise. 
        @rtype: bool.
        """
        raise NotImplementedError()
    
    def is_following(self, user1_id, user2_id):
        """
        @param user1_id: The follower.
        @type user1_id: int.
        @param user2_id: The followee.
        @type user2_id: int.
        @return: True if user1 is following user2. False otherwise.
        @rtype: bool.
        """
        raise NotImplementedError()