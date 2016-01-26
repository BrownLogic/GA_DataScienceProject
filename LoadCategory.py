"""
LoadCategory.py:  This file is for parsing the categories JSON file and loading the database
Assumes that the database has been built
NOTE: The categories file is different from the other Yelp data.
Instead of being a list of JSON objects, it is a single JSON object
"""
import json
import collections
import MySQLdb
from database import login_info
import time


class YelpCategory:
    """organize business data"""

    def __init__(self, yelp_json_object):
        if 'alias' in yelp_json_object:
            self.alias = yelp_json_object['alias']
        if 'title' in yelp_json_object:
            self.title = yelp_json_object['title']
        if 'parents' in yelp_json_object:
            self.parents = yelp_json_object['parents']
        if 'country_blacklist' in yelp_json_object:
            self.country_blacklist = yelp_json_object['country_blacklist']
        else:
            self.country_blacklist = []
        if 'country_whitelist' in yelp_json_object:
            self.country_whitelist = yelp_json_object['country_whitelist']
        else:
            self.country_whitelist = []

def clear_tables(cursor):
    cursor.execute("delete from cat_country_list")
    cursor.execute("delete from cat_parents")
    cursor.execute("delete from categories")


def drop_indexes(cursor):
    try:
        cursor.execute("ALTER TABLE cat_country_list DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE cat_parents DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE categories DROP PRIMARY KEY")
    except:
        pass


def create_indexes(cursor):
    try:
        cursor.execute("ALTER TABLE cat_country_list ADD PRIMARY KEY (alias, list_type, country)")
        cursor.execute("ALTER TABLE cat_parents ADD PRIMARY KEY (alias, parent_alias)")
        cursor.execute("ALTER TABLE categories ADD PRIMARY KEY (alias)")
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
    print "Processing Categories File the batched way, batch size = {}".format(batch_size)

    start_time = time.time()
    update_time = start_time
    list_of_ycos = []
    with open(file_path) as the_file:
        one_big_json_object = json.load(the_file)
        for small_json_object in one_big_json_object:
            list_of_ycos.append(YelpCategory(small_json_object))
            row_count += 1
            if row_count % batch_size == 0:
                persist_list_o_category_objects(list_of_ycos,cursor)
                list_of_ycos=[]

            if row_count % 1000 == 0:
                total_time = (time.time() - start_time)
                time_since_last_post = time.time() - update_time
                update_time = time.time()
                print "Up to row {:} in Category file.  Total Time: {:.4g}; TimeSinceLastPost:{:.4g}".format(row_count, total_time, time_since_last_post)

            if how_many > 0 and row_count % how_many == 0:
                break

    #catch the stragglers
    persist_list_o_category_objects(list_of_ycos,cursor)

    print("--- %s seconds ---" % (time.time() - start_time))

    print "Creating indexes"
    create_indexes(cursor)

    db.commit()
    db.close()

    print "Categories File Complete.  {0} rows processed".format(row_count)

def persist_list_o_category_objects(list_o_ycos, cursor):
    #Similar to the others except that it builds up the sets
    category_data = []
    category_set_count = 0
    cat_country_blacklist_data = []
    cat_country_blacklist_set_count = 0
    cat_country_whitelist_data = []
    cat_country_whitelist_set_count = 0
    cat_parents_data = []
    cat_parents_set_count = 0
    for yco in list_o_ycos:
        category_data+=[yco.alias, yco.title]
        category_set_count +=1
        for country in yco.country_blacklist:
            cat_country_blacklist_data+=[yco.alias, country]
            cat_country_blacklist_set_count+=1
        for country in yco.country_whitelist:
            cat_country_whitelist_data+=[yco.alias, country]
            cat_country_whitelist_set_count+=1
        for parent in yco.parents:
            cat_parents_data+=[yco.alias, parent]
            cat_parents_set_count+=1

    try:
        if category_set_count > 0:
            sql_base = " INSERT INTO categories " \
                  " (alias, category) " \
                  " values {}"
            parameter_base ="(%s, %s)"
            sql = sql_base.format(", ".join([parameter_base]*category_set_count))
            cursor.execute(sql, category_data)

        if cat_country_blacklist_set_count > 0:
            sql_base = " INSERT INTO cat_country_list " \
                      " (alias, list_type, country) " \
                      " values {}"
            parameter_base = "(%s, 'blacklist', %s)"
            sql = sql_base.format(", ".join([parameter_base]*cat_country_blacklist_set_count))
            cursor.execute(sql, cat_country_blacklist_data)

        if cat_country_whitelist_set_count > 0:
            sql_base = " INSERT INTO cat_country_list " \
                      " (alias, list_type, country) " \
                      " values {}"
            parameter_base = "(%s, 'whitelist', %s)"
            sql = sql_base.format(", ".join([parameter_base]*cat_country_whitelist_set_count))
            cursor.execute(sql, cat_country_whitelist_data)

        if cat_parents_set_count > 0:
            sql_base = " INSERT INTO cat_parents " \
                  " (alias, parent_alias) " \
                  " values {}"
            parameter_base = "(%s, %s)"
            sql = sql_base.format(", ".join([parameter_base]*cat_parents_set_count))
            cursor.execute(sql, cat_parents_data)

        cursor.connection.commit()
    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err

def persist_category_object(yco, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type ybo: YelpCategory
    :type cursor: MySQLdb.cursor
    """
    try:
        # categories
        sql = " INSERT INTO categories " \
                  " (alias, category) " \
                  " values (%s, %s)"
        cursor.execute(sql, [yco.alias, yco.title])

        # cat_country_list (blacklist)
        for country in yco.country_blacklist:
            sql = " INSERT INTO cat_country_list " \
                      " (alias, list_type, country) " \
                      " values (%s, 'blacklist', %s)"
            cursor.execute(sql, [yco.alias, country])

        # cat_country_list (whitelist)
        for country in yco.country_whitelist:
            sql = " INSERT INTO cat_country_list " \
                      " (alias, list_type, country) " \
                      " values (%s, 'whitelist', %s)"
            cursor.execute(sql, [yco.alias, country])


        # cat_parents
        for parent in yco.parents:
            sql = " INSERT INTO cat_parents " \
                  " (alias, parent_alias) " \
                  " values (%s, %s)"
            cursor.execute(sql, [yco.alias, parent])

#        cursor.connection.commit()
    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err
        print "Error with alias {0}".format(yco.alias)
        raise

if __name__ == '__main__':
    the_file = 'C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\categories.json'
    parse_file(the_file, 101, 5000)
    #1247 records
