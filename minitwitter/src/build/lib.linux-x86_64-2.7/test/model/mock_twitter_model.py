'''
Created on Jan 21, 2014

@author: anya
'''
from minitwitter.model.twitter_db_client_interface import TwitterDbClientInterface

class MockTwitterDbClient(TwitterDbClientInterface):
    '''
    Mock object that simulates the DB operations and stores everything in python obejcts.
    '''

    def __init__(self, users=None, follows=None, posts=None):
        '''
        Constructor
        '''
        self.users = self._value_or_default(users, [])
        self.follows = self._value_or_default(follows, [])
        self.posts = self._value_or_default(posts, [])
        
    def _value_or_default(self, value, default):
        """
        Return the value if it is not None, default otherwise. This replace the non indicative
        line - self.param = given_param or default.
        @param value: The given value value.
        @type value: object.
        @param default: The default value for the same 
        @type default:
        """
        if value is not None:
            return value
        else:
            return default
    
    def create_new_user(self, user_name):
        user_id = len(self.users) + 1 
        self.users.append([user_id, user_name])
        
    def post_message(self, user_id, message):
        self.posts.append([user_id, message])
        
    def get_global_feed(self):
        return self.posts
    
    def get_feed_for_user(self, user_id):
        posts = []
        followees = self._get_followees(user_id)
        for poster_id, post in self.posts:
            if poster_id in followees:
                posts.append(post)
                
        return posts
    
    def _get_followees(self, user_id):
        followees = []
        for follower, followee in self.follows:
            if follower == user_id:
                followees.append(followee)
        return followees
        
        
    def follow(self, follower_id, followee_id):
        self.follows.append([follower_id, followee_id])
        
    def unfollow(self, follower_id, followee_id):
        self.follows.remove([follower_id, followee_id])
        
    def user_name_exists(self, name):
        for (user_id, user_name) in self.users:
            if name == user_name:
                return True
            
        return False
    
    def user_exists(self, user_id):
        for (userid, user_name) in self.users:
            if userid == user_id:
                return True
        return False
    
    def is_following(self, follower_id, followee_id):
        if [follower_id, followee_id] in self.follows:
            return True
        return False
     
class MockTwitterModel(MockTwitterDbClient):
    """
    Twitter model for handler tests. Doesn't add any validation layer (not required because we 
    only want to test the handlers).
    In a perfect world the model usually contains a DB client and not inherits from it, but for
    the sake of simplicity here inheritance is used.
    """
    pass   
                            
        