"""
LoadUser.py:This file is for parsing the user JSON file and loading the database
Assumes that the database has been built
"""
import json
import MySQLdb
from database import login_info

class YelpUser:
    """organize user data"""

    def __init__(self, yelp_json_object):
        if 'user_id' in yelp_json_object:
            self.user_id = yelp_json_object['user_id']
        if 'name' in yelp_json_object:
            self.name = yelp_json_object['name']
        if 'review_count' in yelp_json_object:
            self.review_count = yelp_json_object['review_count']
        if 'average_stars' in yelp_json_object:
            self.average_stars = yelp_json_object['average_stars']
        if 'yelping_since' in yelp_json_object:
            self.yelping_since = yelp_json_object['yelping_since']
        if 'fans' in yelp_json_object:
            self.fans = yelp_json_object['fans']
        if 'votes' in yelp_json_object:
            self.votes = yelp_json_object['votes']
        if 'friends' in yelp_json_object:
            self.friends = yelp_json_object['friends']
        if 'elite' in yelp_json_object:
            self.elite = yelp_json_object['elite']
        if 'compliments' in yelp_json_object:
            self.compliments = yelp_json_object['compliments']

def clear_tables(cursor):
    cursor.execute("delete from User_Votes")
    cursor.execute("delete from User_Friends")
    cursor.execute("delete from User_Elite")
    cursor.execute("delete from User_Compliments")
    cursor.execute("delete from User")

def drop_indexes(cursor):
    cursor.execute("DROP INDEX User_Compliments_compliment_type_index ON user_compliments")
    cursor.execute("DROP INDEX User_Compliments_user_id_index ON user_compliments")
    cursor.execute("DROP INDEX User_Elite_user_id_index ON user_elite")
    cursor.execute("DROP INDEX User_Friends_friends_index ON user_friends")
    cursor.execute("DROP INDEX User_Friends_user_id_index ON user_friends")
    cursor.execute("DROP INDEX User_Votes_user_id_index ON user_votes")
    cursor.execute("DROP INDEX User_Votes_vote_type_index ON user_votes")


def create_indexes(cursor):
    cursor.execute("CREATE INDEX User_Compliments_compliment_type_index ON user_compliments (compliment_type)")
    cursor.execute("CREATE INDEX User_Compliments_user_id_index ON user_compliments (user_id)")
    cursor.execute("CREATE INDEX User_Elite_user_id_index ON user_elite (user_id)")
    cursor.execute("CREATE INDEX User_Friends_friends_index ON user_friends (friends)")
    cursor.execute("CREATE INDEX User_Friends_user_id_index ON user_friends (user_id)")
    cursor.execute("CREATE INDEX User_Votes_user_id_index ON user_votes (user_id)")
    cursor.execute("CREATE INDEX User_Votes_vote_type_index ON user_votes (vote_type)")


def parse_file(file_path):
    """Read in the json data set file and load into database
    :param (str) file_path :
    """
    db = MySQLdb.connect(**login_info)
    db.set_character_set('utf8') #From http://stackoverflow.com/questions/3942888/unicodeencodeerror-latin-1-codec-cant-encode-character

    cursor = db.cursor()

    #From http://stackoverflow.com/questions/3942888/unicodeencodeerror-latin-1-codec-cant-encode-character
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    print "Dropping indexes and clearing tables"
    drop_indexes(cursor)
    clear_tables(cursor)

    row_count = 0
    print "Processing User File"
    with open(file_path) as the_file:
        for a_line in the_file:
            json_object = json.loads(a_line)
            persist_user_object(YelpUser(json_object), cursor)

            row_count += 1
            if row_count % 1000 == 0:
                print "Up to row {} in User file".format(row_count)

    print "Creating indexes"
    create_indexes(cursor)

    db.commit()
    db.close()

    print "User File complete.  {0} rows processed".format(row_count)


def persist_user_object(yuo, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type yuo: YelpUser
    :type cursor: MySQLdb.cursor
    """
    try:
        # User
        sql = " INSERT INTO User " \
              " (user_id, name, review_count, average_stars, yelping_since, fans)" \
              " values " \
              " (%s, %s, %s, %s, %s, %s) "
        cursor.execute(sql, [yuo.user_id, yuo.name, yuo.review_count, yuo.average_stars, yuo.yelping_since, yuo.fans])

        # User_Compliments
        for comp_type, comp_count in yuo.compliments.iteritems():
            sql = " INSERT INTO User_Compliments " \
                  " (user_id, compliment_type, compliment_count) " \
                  " values " \
                  " (%s, %s, %s) "
            cursor.execute(sql, [yuo.user_id, comp_type, comp_count])

        # User_Elite
        for years in yuo.elite:
            sql = " INSERT INTO User_Elite " \
                  " (user_id, years_elite) " \
                  " values " \
                  " (%s, %s) "
            cursor.execute(sql, [yuo.user_id, years])

        # User_Friends
        for friend in yuo.friends:
            sql = " INSERT INTO User_Friends " \
                  " (user_id, friends) " \
                  " values " \
                  " (%s, %s) "
            cursor.execute(sql, [yuo.user_id, friend])

        # User_Votes
        for vote_type, vote_count in yuo.votes.iteritems():
            sql = " INSERT INTO User_Votes " \
                  " (user_id, vote_type, vote_count) " \
                  " values " \
                  " (%s, %s, %s) "
            cursor.execute(sql, [yuo.user_id, vote_type, vote_count])

        cursor.connection.commit()
    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err
        print "Error with business_id {0}".format(yuo.user_id)
        raise


if __name__ == '__main__':
    parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_user.json')
    #366715 records
