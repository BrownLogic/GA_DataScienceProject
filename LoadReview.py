"""
LoadReview.py: This file is for parsing the review JSON file and loading the database
Assumes that the database has been built
"""
import json
import MySQLdb
from database import login_info

class YelpReview:
    """organize check-in data"""

    def __init__(self, yelp_json_object):
        if 'type' in yelp_json_object:
            self.type = yelp_json_object['type']
        if 'review_id' in yelp_json_object:
            self.review_id = yelp_json_object['review_id']
        if 'business_id' in yelp_json_object:
            self.business_id = yelp_json_object['business_id']
        if 'user_id' in yelp_json_object:
            self.user_id = yelp_json_object['user_id']
        if 'stars' in yelp_json_object:
            self.stars = yelp_json_object['stars']
        if 'date' in yelp_json_object:
            self.review_date = yelp_json_object['date']
        if 'text' in yelp_json_object:
            self.review_text = yelp_json_object['text']
        if 'votes' in yelp_json_object:
            self.votes = yelp_json_object['votes']
        else:
            self.votes = {}

def clear_tables(cursor):
    cursor.execute("delete from Review_Votes")
    cursor.execute("delete from Review")

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

    clear_tables(cursor)
    row_count = 0

    print "Processing Review File"
    with open(file_path) as the_file:
        for a_line in the_file:
            json_object = json.loads(a_line)
            persist_review_object(YelpReview(json_object), cursor)
            row_count += 1
            if row_count % 1000 == 0:
                print "Up to row {} in Review file".format(row_count)


#    cursor.execute("COMMIT TRANSACTION")
    db.commit()
    db.close()
    print "Review File Complete.  {0} rows processed".format(row_count)


def persist_review_object(yro, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type yro: YelpReview
    :type cursor: MySQLdb.cursor
    """
    try:
        # Review
        sql = " INSERT INTO Review " \
              " (review_id, business_id, user_id, stars, review_text, review_date) " \
              " values " \
              " (%s, %s, %s, %s, %s, %s) "
        cursor.execute(sql, [yro.review_id, yro.business_id, yro.user_id, yro.stars, yro.review_text, yro.review_date])

        #Review_Votes
        for vote_type, vote_count in yro.votes.iteritems():
            sql = " INSERT INTO Review_Votes " \
                  " (review_id, business_id, user_id, vote_type, vote_count) " \
                  " values " \
                  " (%s, %s, %s, %s, %s) "
            cursor.execute(sql, [yro.review_id, yro.business_id, yro.user_id, vote_type, vote_count])

        cursor.connection.commit()
    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err
        print "Error with review_id {0}, business_id {1}, user_id {2}".format(yro.review_id, yro.business_id, yro.user_id)
        raise


if __name__ == '__main__':
    parse_file('/home/ubuntu/projects/ga_yelp/yelp_data_raw/yelp_academic_dataset_review.json')
    #1569264 records