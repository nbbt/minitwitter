'''
Created on Jan 21, 2014

@author: anya
'''
import MySQLdb
from _mysql_exceptions import MySQLError
from minitwitter.model.twitter_db_client_interface import TwitterDbClientInterface
from minitwitter.model.exceptions import DbException

class TwitterMysqlClient(TwitterDbClientInterface):
    """
    Basic Twitter Model class which is responsible on validation and db operation.
    Currently uses one connection, can be modified to use connection pool if needed.
    """
    def __init__(self, con):
        """
        @param con: connection to the DB. 
        @type con: MySQLdb.connections.Connection
        """
        self.con = con
    
    def create_new_user(self, name):
        """
        Create a new Twitter user with the given name.
        @param name: The name of the user.
        @type name: str.
        """
        self._execute_transaction("INSERT INTO users (name) VALUES ('%s')" %name)
        
    def post_message(self, user_id, message):
        """
        @param user_id: The id of the user the post belongs to.
        @type user_id: int.
        @param message: The message to post.
        @type message: str (up to 1000 chars!)
        """
        self._execute_transaction("INSERT INTO posts (user_id, post) VALUES (%d, '%s')"\
                                  %(user_id, message))
        
    def follow(self, follower_id, followee_id):
        """
        Add the followee to the list of followed users of the follower.
        
        @param follower_id: The id of the follower.
        @type follower_id: int.
        @param followee_id: The id of the user which is followed.
        @type followee_id: int.
        """
        self._execute_transaction("INSERT INTO follows (follower, followee) VALUES (%d, %d)"\
                                 %(follower_id, followee_id))
        
    def unfollow(self, follower_id, followee_id):
        """
        Remove the followee from the list of followed users of the follower.
        @param follower_id: The id of the following user.
        @type follower_id: int.
        @param followee_id: The id of the followed user.
        @type followee_id: int.
        """
        self._execute_transaction("DELETE FROM follows WHERE follower=%d and followee=%d"\
                                 %(follower_id, followee_id))
        
    def get_global_feed(self):
        """
        Return the posts of all users.
        @rtype: list of tuples.
        """
        cur = self._execute_transaction("SELECT user_id, post FROM posts")
        return cur.fetchall()
    
    def get_feed_for_user(self, user_id):
        cur = self._execute_transaction("""SELECT user_id, post FROM posts WHERE user_id IN 
                  (SELECT followee FROM follows WHERE follower=%d)""" %user_id)
        return cur.fetchall()
        
    def user_exists(self, user_id):
        cur = self._execute_transaction("SELECT name FROM users WHERE id=%d" %user_id) 
        if cur.rowcount >= 1:
            return True
        else:
            return False
        
    def is_following(self, user1_id, user2_id):
        cur = self._execute_transaction("""SELECT follower, followee FROM follows 
        WHERE follower=%d and followee=%d""" %(user1_id, user2_id)) 
        if cur.rowcount >= 1:
            return True
        else:
            return False
        
        
    def _execute_transaction(self, sql_command):
        """
        Execute a db transaction (and commit).
        @param sql_command: The SQL command to execute.
        @type sql_command: str.
        @return: the cursor (for fetching results)
        @rtype: MySQLdb.cursors.Cursor.
        """
        try:
            cur = self.con.cursor();
            cur.execute(sql_command)
            self.con.commit()
            return cur
        except MySQLdb.Error, e:
            if self.con:
                self.con.rollback()
            raise e;


def catch_db_error_decorator(method):
    def wrap_method(self, *args):
        try:
            method(self, *args)
        except MySQLError as e:
            raise DbException(e)
            
