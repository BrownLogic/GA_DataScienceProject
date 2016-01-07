"""
This file is for parsing the user JSON file and loading the database
Assumes that the database has been built
"""
import json
import sqlite3
import collections

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


def parse_file(file_path):
    """Read in the json data set file and load into database
    :param (str) file_path :
    """
    db = sqlite3.connect("DsProject.db")
    cursor = db.cursor()

    row_count = 0

    with open(file_path) as the_file:
        for a_line in the_file:
            json_object = json.loads(a_line)
            persist_user_object(YelpUser(json_object), cursor)

            row_count += 1
            if row_count % 1000 == 0:
                print "Up to row {}".format(row_count)

    db.commit()
    db.close()


def persist_user_object(yuo, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type yuo: YelpUser
    :type cursor: sqlite3.cursor
    """
    try:
        # User
        sql = " INSERT INTO User " \
              " (user_id, name, review_count, average_stars, yelping_since, fans)" \
              " values " \
              " (?, ?, ?, ?, ?, ?) "
        cursor.execute(sql, (yuo.user_id, yuo.name, yuo.review_count, yuo.average_stars, yuo.yelping_since, yuo.fans))

        # User_Compliments
        for comp_type, comp_count in yuo.compliments.iteritems():
            sql = " INSERT INTO User_Compliments " \
                  " (user_id, compliment_type, compliment_count) " \
                  " values " \
                  " (?, ?, ?) "
            cursor.execute(sql, (yuo.user_id, comp_type, comp_count))

        # User_Elite
        for years in yuo.elite:
            sql = " INSERT INTO User_Elite " \
                  " (user_id, years_elite) " \
                  " values " \
                  " (?, ?) "
            cursor.execute(sql, (yuo.user_id, years))

        # User_Friends
        for friend in yuo.friends:
            sql = " INSERT INTO User_Friends " \
                  " (user_id, friends) " \
                  " values " \
                  " (?, ?) "
            cursor.execute(sql, (yuo.user_id, friend))

        # User_Votes
        for vote_type, vote_count in yuo.votes.iteritems():
            sql = " INSERT INTO User_Votes " \
                  " (user_id, vote_type, vote_count) " \
                  " values " \
                  " (?, ?, ?) "
            cursor.execute(sql, (yuo.user_id, vote_type, vote_count))

#        cursor.connection.commit()
    except sqlite3.OperationalError:
        cursor.connection.rollback()
        print "Error with business_id {0}".format(yuo.user_id)
        raise


if __name__ == '__main__':
    #parse_file('C:\\Users\\matt\\Documents\\Projects\\SqliteSandbox\\user_one_record.json')
    parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_user.json')
    #366715 records
