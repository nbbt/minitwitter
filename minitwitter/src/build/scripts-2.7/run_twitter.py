'''
Created on Jan 22, 2014

@author: anya
'''
from minitwitter.server.http_server import start_server, TEST_DB_DETAILS,\
    PROD_DB_DETAILS, PORT
from optparse import OptionParser



def get_option_parser():
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", type="int",
                      help="The post to listen to", default=PORT)
    parser.add_option("-d", "--prod",
                      action="store_true", dest="use_prod_db",
                      help="User production DB.", default=False)
    return parser

if __name__ == "__main__":
    (options, args) = get_option_parser().parse_args()
    if options.use_prod_db:
        db_details = PROD_DB_DETAILS
        db = "prod"
    else:
        db_details = TEST_DB_DETAILS
        db = "test" 
    print "Starting server, using port %d and %s db." %(options.port, db)
    start_server(options.port, db_details)
