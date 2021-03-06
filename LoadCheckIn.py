"""
LoadCheckIn.py: This file is for parsing the CheckIn JSON file and loading the database
Assumes that the database has been built
"""
import json
import MySQLdb
from database import login_info
import time


class YelpCheckin:
    """Organize data from Checkin JSON file"""

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
    """
    Clears all of the tables that will be populated.
    :param cursor: Open MySQLdb cursor
    """
    cursor.execute("delete from Checkins")


def drop_indexes(cursor):
    """
    Drops indexes from all of the tables that will be populated
    :param cursor: Open MySQLdb cursor
    """
    try:
        cursor.execute("DROP INDEX Checkins_checkin_info_index ON checkins")
        cursor.execute("ALTER TABLE Checkins DROP PRIMARY KEY")
    except:
        pass


def create_indexes(cursor):
    """
    Creates indexes on all of the tables that will be (have been) populated
    :param cursor: Open MySQLdb cursor
    """
    try:
        cursor.execute("CREATE INDEX Checkins_checkin_info_index ON checkins (checkin_info)")
        cursor.execute("ALTER TABLE Checkins ADD PRIMARY KEY (business_id, checkin_info)")
    except:
        pass


def parse_file(file_path, batch_size=100, how_many=-1):
    """
    Read in the json data set file and load into database
    :param file_path: Location of the file
    :param batch_size: Indicates how many records to parse before persisting
        to database.  I used this to tweak performance.
    :param how_many: Indicates how many records to parse for ending the function.
        This allows for partially loading a file (testing and debugging)
    """
    db = MySQLdb.connect(**login_info)
    # From http://stackoverflow.com/questions/3942888/unicodeencodeerror-latin-1-codec-cant-encode-character
    db.set_character_set('utf8')

    cursor = db.cursor()

    # From http://stackoverflow.com/questions/3942888/unicodeencodeerror-latin-1-codec-cant-encode-character
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    print "Dropping indexes and clearing tables"
    drop_indexes(cursor)
    clear_tables(cursor)
    row_count = 0
    list_of_ycos = []

    print "Processing Check-in File "

    start_time = time.time()
    update_time = start_time
    with open(file_path) as the_file:
        for a_line in the_file:
            json_object = json.loads(a_line)
            list_of_ycos.append(YelpCheckin(json_object))
            row_count += 1
            if row_count % batch_size == 0:
                persist_list_o_checkin_objects(list_of_ycos, cursor)
                list_of_ycos = []

            if row_count % 1000 == 0:
                total_time = (time.time() - start_time)
                time_since_last_post = time.time() - update_time
                update_time = time.time()
                print "Up to row {:} in Check-in file.  Total Time: {:.4g}; TimeSinceLastPost:{:.4g}"\
                    .format(row_count, total_time, time_since_last_post)
            if how_many > 0 and row_count % how_many == 0:
                break
        # catch the stragglers
        persist_list_o_checkin_objects(list_of_ycos, cursor)

    print "Creating indexes"
    create_indexes(cursor)

    db.commit()
    db.close()

    print "Check-In File Complete.  {0} rows processed ".format(row_count)


def persist_list_o_checkin_objects(list_o_ycos, cursor):
    """
    This function persists a list of YelpCheckin objects.  Original implementations
    persisted each one individually, which performed slowly.
    This one accepts a collection and takes advantage of parameterized queries to
    persist in batches
    :param list_o_ycos: List of YelpCategory objects
    :param cursor: Open MySQLdb cursor
    """
    checkin_data = []
    checkin_set_count = 0
    for yco in list_o_ycos:
        for checkin_info, checkin_count in yco.checkin.iteritems():
            checkin_data += [yco.business_id, checkin_info, checkin_count]
            checkin_set_count += 1
    try:
        if checkin_set_count > 0:
            sql_base = "INSERT INTO Checkins " \
                  " (business_id, checkin_info, checkin_count) " \
                  " values {}"
            parameter_base = "(%s, %s, %s)"
            sql = sql_base.format(", ".join([parameter_base] * checkin_set_count))
            cursor.execute(sql, checkin_data)

        cursor.connection.commit()

    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err


def persist_checkin_object(yco, cursor):
    """
    Saves a single YelpCheckin object to database.
    This is the original implementation but it turns out that this was
    poorly performing, so I scrapped it in favor of
    persist_list_o_business_objects
    :param yco: A single YelpCheckin object
    :param cursor: Open MySQLdb cursor
    """
    try:
        # CheckIn

        for checkin_info, checkin_count in yco.checkin.iteritems():
            sql = " INSERT INTO Checkins " \
                  " (business_id, checkin_info, checkin_count) " \
                  " values " \
                  " (%s, %s, %s) "
            cursor.execute(sql, [yco.business_id, checkin_info, checkin_count])

        cursor.connection.commit()
    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err
        print "Error with business_id {0}".format(yco.business_id)


if __name__ == '__main__':
    the_file = 'C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_checkin.json'
    parse_file(the_file, 101, 5000)
    # 45166 records
