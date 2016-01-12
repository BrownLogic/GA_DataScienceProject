"""
This file is for parsing the review JSON file and loading the database
Assumes that the database has been built
"""
import json
import sqlite3


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


def parse_file(file_path):
    """Read in the json data set file and load into database
    :param (str) file_path :
    """
    db = sqlite3.connect("DsProject.db")
    cursor = db.cursor()
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
    :type cursor: sqlite3.cursor
    """
    try:
        # Review
        sql = " INSERT INTO Review " \
              " (review_id, business_id, user_id, stars, review_text, review_date) " \
              " values " \
              " (?, ?, ?, ?, ?, ?) "
        cursor.execute(sql, (yro.review_id, yro.business_id, yro.user_id, yro.stars, yro.review_text, yro.review_date))

        #Review_Votes
        for vote_type, vote_count in yro.votes.iteritems():
            sql = " INSERT INTO Review_Votes " \
                  " (review_id, business_id, user_id, vote_type, vote_count) " \
                  " values " \
                  " (?, ?, ?, ?, ?) "
            cursor.execute(sql, (yro.review_id, yro.business_id, yro.user_id, vote_type, vote_count))

#        cursor.connection.commit()
    except sqlite3.OperationalError:
        cursor.connection.rollback()
        print "Error with review_id {0}, business_id {1}, user_id {2}".format(yrw.review_id, yro.business_id, yro.user_id)
        raise


if __name__ == '__main__':
    #parse_file('C:\\Users\\matt\\Documents\\Projects\\SqliteSandbox\\review_one_record.json')
    parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_review.json')
    #1569264 records