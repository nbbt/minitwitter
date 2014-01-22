'''
Created on Jan 20, 2014

@author: anya
'''

import tornado.ioloop
import tornado.web
import MySQLdb
from minitwitter.server.handlers import StatusesHandler, UsersHandler, FollowsHandler,\
    UserStatusesHandler
from minitwitter.model.twitter_model import TwitterModel
from minitwitter.model.twitter_mysql_client import TwitterMysqlClient

#COnnection Details

TEST_DB_DETAILS = ("localhost", "testuser", "", "testdb")
PROD_DB_DETAILS = ("localhost", "produser", "", "prod")
PORT = 1200

            
def create_application(twitter_model):
    """
    Create a tornado application with the given Twitter model.
    @param model: The Twitter model.
    @type model: TwitterModel or other class that implements the relevant methods.
    """
    return tornado.web.Application([
    (r"/statuses", StatusesHandler, dict(twitter_model=twitter_model)),
    (r"/users", UsersHandler, dict(twitter_model=twitter_model)),
    (r"/users/([\d]+)/followers", FollowsHandler, dict(twitter_model=twitter_model)),
    (r"/statuses/([\d]+)", UserStatusesHandler, dict(twitter_model=twitter_model))
])


def start_server(port, db_details):
    con = MySQLdb.connect(*db_details);
    twitter_model = TwitterModel(TwitterMysqlClient(con))
    application = create_application(twitter_model)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
    
