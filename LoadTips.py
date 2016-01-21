"""
LoadTips.py:  This file is for parsing the tips JSON file and loading the database
Assumes that the database has been built
"""
import json
import MySQLdb
from database import login_info
import time

def clear_tables(cursor):
    cursor.execute("delete from User_Tips")

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

def drop_indexes(cursor):
    try:
        cursor.execute("DROP INDEX User_Tips_business_id_index ON user_tips")
        cursor.execute("DROP INDEX User_Tips_tip_date_index ON user_tips")
        cursor.execute("DROP INDEX User_Tips_user_id_index ON user_tips")
    except:
        pass


def create_indexes(cursor):
    try:
        cursor.execute("CREATE INDEX User_Tips_business_id_index ON user_tips (business_id)")
        cursor.execute("CREATE INDEX User_Tips_tip_date_index ON user_tips (tip_date)")
        cursor.execute("CREATE INDEX User_Tips_user_id_index ON user_tips (user_id)")
    except:
        pass


def parse_file(file_path, batch_size=100, how_many=-1):
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
    list_of_ytos = []

    print "Processing Tip File"
    start_time = time.time()
    update_time = start_time
    with open(file_path) as the_file:
        for a_line in the_file:
            json_object = json.loads(a_line)
            list_of_ytos.append(YelpTip(json_object))
            row_count += 1
            if row_count % batch_size == 0:
                persist_list_o_tip_objects(list_of_ytos, cursor)
                list_of_ytos=[]
            if row_count % 1000 == 0:
                total_time = (time.time() - start_time)
                time_since_last_post = time.time() - update_time
                update_time = time.time()
                print "Up to row {} in Tips file.  Total Time: {}; TimeSinceLastPost:{}".format(row_count, total_time, time_since_last_post)

            if how_many > 0 and row_count % how_many == 0:
                break

        #catch the stragglers
        persist_list_o_tip_objects(list_of_ytos, cursor)

    print "Creating indexes"
    create_indexes(cursor)

    db.commit()
    db.close()

    print "Tip File complete.  {0} rows processed".format(row_count)

def persist_list_o_tip_objects(list_o_ytos, cursor):
    tip_data = []
    tip_set_count = 0
    for yto in list_o_ytos:
        tip_data+=[yto.business_id, yto.user_id, yto.likes, yto.tip_text, yto.tip_date]
        tip_set_count+=1

    try:
        if tip_data > 0:
            sql_base = "  INSERT INTO User_Tips " \
              " (business_id, user_id, likes, tip_text, tip_date) " \
              " values {}"
            parameter_base = "(%s, %s, %s, %s, %s)"
            sql = sql_base.format(", ".join([parameter_base]* tip_set_count))
            cursor.execute(sql, tip_data)
    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err

def persist_tip_object(yto, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type yto: YelpTip
    :type cursor: MySQLdb.cursor
    """
    try:
        # User_Tips
        sql = " INSERT INTO User_Tips " \
              " (business_id, user_id, likes, tip_text, tip_date) " \
              " values " \
              " (%s, %s, %s, %s, %s) "
        cursor.execute(sql, [yto.business_id, yto.user_id, yto.likes, yto.tip_text, yto.tip_date])
        cursor.connection.commit()
    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err
        print "Error with business_id {0}, user_id {1}".format(yto.business_id, yto.user_id)


if __name__ == '__main__':
    the_file = 'C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_tip.json'
    parse_file(the_file, 101, 5000)
    #495108 records