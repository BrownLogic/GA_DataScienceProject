"""
This file is for parsing the business JSON file and loading the database
Assumes that the database has been built
"""
import json
import sqlite3


class YelpCheckin:
    """organize check-in data"""

    def __init__(self, yelp_json_object):
        if 'type' in yelp_json_object:
            self.type = yelp_json_object['type']
        if 'business_id' in yelp_json_object:
            self.business_id = yelp_json_object['business_id']
        if 'checkin_info' in yelp_json_object:
            self.checkin = yelp_json_object['checkin_info']
        else:
            self.checkin = {}


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
            persist_checkin_object(YelpCheckin(json_object), cursor)
            row_count += 1
            if row_count % 1000 == 0:
                print "Up to row {}".format(row_count)


#    cursor.execute("COMMIT TRANSACTION")
    db.commit()
    db.close()


def persist_checkin_object(yco, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type yco: YelpCheckin
    :type cursor: sqlite3.cursor
    """
    try:
        # CheckIn

        for checkin_info, checkin_count in yco.checkin.iteritems():
            sql = " INSERT INTO Checkins " \
                  " (business_id, checkin_info, checkin_count) " \
                  " values " \
                  " (?, ?, ?) "
            cursor.execute(sql, (yco.business_id, checkin_info, checkin_count))

#        cursor.connection.commit()
    except sqlite3.OperationalError:
        cursor.connection.rollback()
        print "Error with business_id {0}".format(yco.business_id)
        raise


if __name__ == '__main__':
    #parse_file('C:\\Users\\matt\\Documents\\Projects\\SqliteSandbox\\checkin_one_record.json')
    parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_checkin.json')
    #45166 records