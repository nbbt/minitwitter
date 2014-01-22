'''
Created on Jan 22, 2014

@author: anya
'''
from minitwitter.server.twitter_request_handler import TwitterRequestHandler,\
    handle_exceptions_decorator
from httplib import NO_CONTENT, CREATED



class StatusesHandler(TwitterRequestHandler):
    """
    Handles global feed requests.
    """
    @handle_exceptions_decorator
    def get(self):
        self.write({"posts": self.twitter_model.get_global_feed()})


class FollowsHandler(TwitterRequestHandler):
    """
    Handles follow/unfollow requests.
    """
    
    @handle_exceptions_decorator
    def put(self, follower_id):
        followee_id = self._validate_user_id(self.get_argument("followee_id"))
        follower_id = self._validate_user_id_from_url(follower_id)
        followee_id = int(followee_id)
        self.twitter_model.follow(int(follower_id), followee_id)
        self.write("Successfully added to following list.")
        
        
    @handle_exceptions_decorator    
    def delete(self, follower_id):
        followee_id = self._validate_user_id(self.get_argument("followee_id"))
        self.twitter_model.unfollow(int(follower_id), int(followee_id))
        self.set_status(NO_CONTENT)
        self.write("Successfully removed from following list.")
        
        
class UserStatusesHandler(TwitterRequestHandler):
    """
    Handles user requests for feed or post message.
    """
    
    @handle_exceptions_decorator
    def get(self, user_id):
        user_id = self._validate_user_id_from_url(user_id)
        self.write({"posts": self.twitter_model.get_feed_for_user(int(user_id))})
    
    @handle_exceptions_decorator
    def post(self, user_id):
        user_id = self._validate_user_id_from_url(user_id)
        message = self.get_argument("message")
        self.twitter_model.post_message(int(user_id), message)
        self.write("Posted!")

class UsersHandler(TwitterRequestHandler):
    """
    Handles requests to create a new user
    """
    @handle_exceptions_decorator
    def post(self):
        new_user_name = self.get_argument("user_name")
        self.twitter_model.create_new_user(new_user_name)
        self.set_status(CREATED)
        self.write("New user created successfully!")
