'''
Created on Jan 22, 2014

@author: anya
'''
import unittest
from minitwitter.server.handlers import UsersHandler, StatusesHandler, FollowsHandler,\
    UserStatusesHandler
from httplib import BAD_REQUEST, INTERNAL_SERVER_ERROR, SERVICE_UNAVAILABLE
from minitwitter.model.exceptions import DbException
from test.model.mock_twitter_model import MockTwitterModel
from test.server.mock_handler_mixin import MockHandlerMixin


"""
Test all handlers using mock for the model (keeps all data in python objects instead of DB) and 
mock for the handler (overrides all methods except the get/post etc).
Test the handlers with good and bad input.
"""



class UsersHandlerTest(unittest.TestCase):
    def test_post(self):
        new_user_name = "user1"
        model = MockTwitterModel()
        handler = MockUsersHandler(model, {"user_name": new_user_name})
        handler.post()
        self.assert_(model.user_name_exists(new_user_name), "User name wasnt really added.")
        self.assert_(handler.no_errors(), "There are error in legal post.")
        
class StatusesHandlerTest(unittest.TestCase):
    def test_get(self):
        post1 = "Hi"
        post2 = "Bye"
        post3 = "Morning!"
        model = MockTwitterModel(posts=[[1, post1], [3, post2], [2, post3]])
        handler = MockStatusesHandler(model)
        handler.get()
        self.assertIn(post1, handler.response_text, "One or more of the posts weren't added.")
        self.assertIn(post2, handler.response_text, "One or more of the posts weren't added.")
        self.assertIn(post3, handler.response_text, "One or more of the posts weren't added.")
        
class FollowsHandlerTest(unittest.TestCase):
    def test_put(self):
        follower_id = 5
        followee_id = 2
        model = MockTwitterModel(follows=[[1,2], [1,3], [3,7]])
        handler = MockFollowsHandlerHandler(model, {"followee_id": str(followee_id)})
        handler.put(follower_id)
        self.assertIn([follower_id, followee_id], model.follows,\
                       "The followee wasn't added to the followers following list.")

    def test_put_bad_followee_id(self):
        model = MockTwitterModel()
        handler = MockFollowsHandlerHandler(model, {"followee_id": "a"})
        handler.put(5)
        assert handler.status == BAD_REQUEST
        
    def test_put_bad_follower_id(self):
        model = MockTwitterModel()
        handler = MockFollowsHandlerHandler(model, {"followee_id": 1})
        handler.put("a")
        self.assert_(handler.status == INTERNAL_SERVER_ERROR,\
                      "Should return %d for bad follower id" %INTERNAL_SERVER_ERROR)
        
    def test_delete(self):
        follower_id = 1
        followee_id = 3
        model = MockTwitterModel(follows=[[1,2], [follower_id, followee_id], [3,7]])
        handler = MockFollowsHandlerHandler(model, {"followee_id": str(followee_id)})
        handler.delete(follower_id)
        self.assertNotIn([follower_id, followee_id], model.follows,\
                         "User %d wasnt removed from following list of user %d"\
                         %(followee_id,follower_id) )


class UserStatusesHandlerTest(unittest.TestCase):
    def test_get(self):
        user_id = 2
        followed_posts = ["Morning!", "Whats up?", "How are you?"]
        not_followed_posts = ["Bla Bla", ":)", ":("]
        followed = [1, 5]
        follows = [[1, 3], [user_id, followed[0]], [4, user_id], [user_id, followed[1]]]
        posts = [[user_id, not_followed_posts[0]], 
                 [followed[0], followed_posts[0]], 
                 [7, not_followed_posts[1]],
                 [followed[1], followed_posts[1]],
                 [followed[0],followed_posts[2]],
                 [user_id, not_followed_posts[2]]]
        model = MockTwitterModel(follows=follows, posts=posts)
        handler = MockUserStatusesHandler(model)
        handler.get(user_id)
        
        for post in followed_posts:
            self.assertIn(post, handler.response_text,\
                           "Post of a followed user doen't appear in the feed.")
            
        for post in not_followed_posts:
            self.assertNotIn(post, handler.response_text,\
                              "Not followed user post appears in the feed.")
    
    def test_get_bad_user_id(self):
        model = MockTwitterModel()
        handler = MockUserStatusesHandler(model)
        handler.get("a")
        self.assert_(handler.status == INTERNAL_SERVER_ERROR,\
                      "Get with bad user name should result %d error." %INTERNAL_SERVER_ERROR)
    
    def test_post(self):
        user_id = 4
        post = "This is users post."
        model = MockTwitterModel()
        handler = MockUserStatusesHandler(model, {"message": post})
        handler.post(user_id)
        self.assertIn([user_id, post], model.posts, "The post wasnt posted.")
    
    def test_post_bad_user_id(self):
        model = MockTwitterModel()
        handler = MockUserStatusesHandler(model)
        handler.post("b")
        self.assert_(handler.status == INTERNAL_SERVER_ERROR,\
                      "Post with bad user name should result %d error." %INTERNAL_SERVER_ERROR)
        
class BadDbClient(object):
    """
    Mock Db client that raises DbException for each method called.
    """
    def __getattribute__(self, *args, **kwargs):
        raise DbException

class DbErrorTest(unittest.TestCase):
    """
    Test one arbitrary handler (probably should test all of them or make sure all relevant methods
    are decorated with the same exception handling decorator) for the case the is a problem with
    the db.
    """
    def test_db_error(self):
        model = BadDbClient()
        handler = MockStatusesHandler(model)
        handler.get()
        self.assert_(handler.status == SERVICE_UNAVAILABLE)
    

"""
Mock handlers - inherit from MockHandlerMixin which overrides tornado.web.RequestHandler
methods to test the handlers logic only.
Note - MockHandlerMixin must come first in the list of super classes.
This is not the best way to test the handler, because:
1. Depends on inheritance order.
2. The intension was to disable the actions of tornado.web.RequestHandler (which all handlers
   inherit from). Practically only some methods are overriden so strange things may happen.
"""
class MockUsersHandler(MockHandlerMixin, UsersHandler):
    pass

class MockStatusesHandler(MockHandlerMixin, StatusesHandler):
    pass

class MockFollowsHandlerHandler(MockHandlerMixin, FollowsHandler):
    pass

class MockUserStatusesHandler(MockHandlerMixin, UserStatusesHandler):
    pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()