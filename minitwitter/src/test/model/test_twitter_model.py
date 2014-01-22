'''
Created on Jan 22, 2014

@author: anya
'''
import unittest
from minitwitter.model.twitter_model import TwitterModel
from minitwitter.model.exceptions import UserNotExistsException, AlreadyFollowingException,\
    NotFollowingException
from test.model.mock_twitter_model import MockTwitterDbClient


class TwitterModelTest(unittest.TestCase):
    """Test the model layer. The tests cover the validation layer and check that the right methods
    in the db_client are called. The MySqlClient is not testes (a mick DB client is used).
    """
    
    def test_post_message(self):
        user1, user2 = 1, 2
        users = [[user1, "name1"], [user2, "name2"]]
        message = "Hi! What's up guys?"
        model = TwitterModel(MockTwitterDbClient(users=users))
        model.post_message(user2, message)
        self.assertIn([user2, message], model.db_client.posts)
        
    
    def test_create_new_user(self):
        new_user_name = "name1"
        model = TwitterModel(MockTwitterDbClient())
        model.create_new_user(new_user_name)
        self.assert_(model.db_client.user_name_exists(new_user_name), "New user not created.")
        
    def test_get_global_feed(self):
        posts = [[1, "Hi"], [2, "Having Fun!"], [1, "Bla"], [8, "Lalala"]]
        model = TwitterModel(MockTwitterDbClient(posts=posts))
        self.assertItemsEqual(posts, model.get_global_feed(), "Global feed is not as expected.")

    def test_get_user_feed(self):
        users = [[1, "Tom"], [2, "Matt"], [3, "Jack"], [4, "Mila"], [5, "Mike"]]
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
        
        model = TwitterModel(MockTwitterDbClient(users=users, follows=follows, posts=posts))
        self.assertItemsEqual(followed_posts, model.get_feed_for_user(user_id),\
                              "User feed is not as expected.")
    
    def test_follow(self):
        user1, user2, user3, user4 = 1, 2, 3, 4
        users = [[user1, "name1"], [user2, "name2"], [user3, "name3"], [user4, "name4"]]
        model = TwitterModel(MockTwitterDbClient(users=users))
        model.follow(user2, user4)
        self.assertIn([user2, user4], model.db_client.follows, "Follow action had no affect.")

    def test_unfollow(self):
        user1, user2, user3, user4 = 1, 2, 3, 4
        users = [[user1, "name1"], [user2, "name2"], [user3, "name3"], [user4, "name4"]]
        follows = [[user1, user3], [user4, user1]]
        model = TwitterModel(MockTwitterDbClient(users=users, follows=follows))
        model.unfollow(user4, user1)
        self.assertNotIn([user4, user1], model.db_client.follows, "Follow action had no affect.")

    
    def test_none_existing_user_actions(self):
        """
        Check that actions on user_id that does not exists lead to the suitable exception.
        """
        users = [[1, "Tom"], [2, "Max"], [3, "Dan"]]
        model = TwitterModel(MockTwitterDbClient(users=users))
        self.assertRaises(UserNotExistsException, model.get_feed_for_user, 8)
        self.assertRaises(UserNotExistsException, model.follow, *(7, 3))
        self.assertRaises(UserNotExistsException, model.unfollow, *(1, 8))
        self.assertRaises(UserNotExistsException, model.follow, *(8, 2))
        
    def test_already_following(self):
        """
        Check that the suitable exception is raised when trying to make user1 follow user2 when
        he is already following user2.
        """
        user1, user2, user3, user4 = 1, 2, 3, 4
        users = [[user1, "name1"], [user2, "name2"], [user3, "name3"], [user4, "name4"]]
        follows = [[user1, user2], [user2, user3], [user1, user4]]
        model = TwitterModel(MockTwitterDbClient(users=users, follows=follows))
        self.assertRaises(AlreadyFollowingException, model.follow, *(user1, user2))
        self.assertRaises(AlreadyFollowingException, model.follow, *(user2, user3))
        self.assertRaises(AlreadyFollowingException, model.follow, *(user1, user4))
        
    def test_cant_unfollow(self):
        """
        Check that suitable exception is raised when trying to unfollow user2 from by user1 and
        user1 is not following user2.
        """
        user1, user2, user3, user4 = 1, 2, 3, 4
        users = [[user1, "name1"], [user2, "name2"], [user3, "name3"], [user4, "name4"]]
        follows = [[user1, user2], [user2, user3], [user1, user4]]
        model = TwitterModel(MockTwitterDbClient(users=users, follows=follows))
        self.assertRaises(NotFollowingException, model.unfollow, *(user1, user1))
        self.assertRaises(NotFollowingException, model.unfollow, *(user2, user4))
        self.assertRaises(NotFollowingException, model.unfollow, *(user4, user1))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()