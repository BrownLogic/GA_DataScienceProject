"""
LoadCheckIn.py: This file is for parsing the CheckIn JSON file and loading the database
Assumes that the database has been built
"""
import json
import MySQLdb
from database import login_info


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


def clear_tables(cursor):
    cursor.execute("delete from Checkins")


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

    print "Processing Check-in File "

    with open(file_path) as the_file:
        for a_line in the_file:
            json_object = json.loads(a_line)
            persist_checkin_object(YelpCheckin(json_object), cursor)
            row_count += 1
            if row_count % 1000 == 0:
                print "Up to row {} in Check-in file".format(row_count)

    db.commit()
    db.close()

    print "Check-In File Complete.  {0} rows processed ".format(row_count)

def persist_checkin_object(yco, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type yco: YelpCheckin
    :type cursor: MySqlDB.cursor
    """
    try:
        # CheckIn

        for checkin_info, checkin_count in yco.checkin.iteritems():
            sql = " INSERT INTO Checkins " \
                  " (business_id, checkin_info, checkin_count) " \
                  " values " \
                  " (%s, %s, %s) "
            cursor.execute(sql, [yco.business_id, checkin_info, checkin_count])

    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err
        print "Error with business_id {0}".format(yco.business_id)
        raise


if __name__ == '__main__':
    parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_checkin.json')
    #45166 records