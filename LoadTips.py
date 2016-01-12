"""
This file is for parsing the tips JSON file and loading the database
Assumes that the database has been built
"""
import json
import sqlite3


class YelpTip:
    """organize check-in data"""

    def __init__(self, yelp_json_object):
        if 'type' in yelp_json_object:
            self.type = yelp_json_object['type']
        if 'business_id' in yelp_json_object:
            self.business_id = yelp_json_object['business_id']
        if 'user_id' in yelp_json_object:
            self.user_id = yelp_json_object['user_id']
        if 'date' in yelp_json_object:
            self.tip_date = yelp_json_object['date']
        if 'text' in yelp_json_object:
            self.tip_text = yelp_json_object['text']
        if 'likes' in yelp_json_object:
            self.likes = yelp_json_object['likes']


def parse_file(file_path):
    """Read in the json data set file and load into database
    :param (str) file_path :
    """
    db = sqlite3.connect("DsProject.db")
    cursor = db.cursor()
    row_count = 0

    print "Processing Tip File"
    with open(file_path) as the_file:
        for a_line in the_file:
            json_object = json.loads(a_line)
            persist_review_object(YelpTip(json_object), cursor)
            row_count += 1
            if row_count % 1000 == 0:
                print "Up to row {} in Tips file".format(row_count)


#    cursor.execute("COMMIT TRANSACTION")
    db.commit()
    db.close()

    print "Tip File complete.  {0} rows processed".format(row_count)


def persist_review_object(yto, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type yto: YelpTip
    :type cursor: sqlite3.cursor
    """
    try:
        # User_Tips
        sql = " INSERT INTO User_Tips " \
              " (business_id, user_id, likes, tip_text, tip_date) " \
              " values " \
              " (?, ?, ?, ?, ?) "
        cursor.execute(sql, (yto.business_id, yto.user_id, yto.likes, yto.tip_text, yto.tip_date))

    except sqlite3.OperationalError:
        cursor.connection.rollback()
        print "Error with business_id {0}, user_id {1}".format(yto.business_id, yto.user_id)
        raise


if __name__ == '__main__':
    #parse_file('C:\\Users\\matt\\Documents\\Projects\\SqliteSandbox\\tip_one_record.json')
    parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_tip.json')
    #495108 records