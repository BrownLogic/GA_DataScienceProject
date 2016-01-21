"""
LoadBusinessBatch.py:  This file is for parsing the business JSON file and loading the database
Assumes that the database has been built
"""
import json
import collections
import MySQLdb
from database import login_info
import time


class YelpBusiness:
    """organize business data"""

    def __init__(self, yelp_json_object):
        if 'type' in yelp_json_object:
            self.type = yelp_json_object['type']
        if 'business_id' in yelp_json_object:
            self.business_id = yelp_json_object['business_id']
        if 'name' in yelp_json_object:
            self.name = yelp_json_object['name']
        if 'full_address' in yelp_json_object:
            self.full_address = yelp_json_object['full_address']
        if 'city' in yelp_json_object:
            self.city = yelp_json_object['city']
        if 'state' in yelp_json_object:
            self.state = yelp_json_object['state']
        if 'latitude' in yelp_json_object:
            self.latitude = yelp_json_object['latitude']
        if 'longitude' in yelp_json_object:
            self.longitude = yelp_json_object['longitude']
        if 'stars' in yelp_json_object:
            self.stars = yelp_json_object['stars']
        if 'review_count' in yelp_json_object:
            self.review_count = yelp_json_object['review_count']
        if 'categories' in yelp_json_object:
            self.categories = yelp_json_object['categories']
        if 'attributes' in yelp_json_object:
            self.attributes = flatten_attributes(yelp_json_object['attributes'])
        else:
            self.attributes = {}
        if 'neighborhoods' in yelp_json_object:
            self.neighborhoods = yelp_json_object['neighborhoods']
        if 'open' in yelp_json_object:
            self.open = yelp_json_object['open']
        if 'hours' in yelp_json_object:
            self.hours = yelp_json_object['hours']
        else:
            self.hours = {}


def clear_tables(cursor):
    cursor.execute("delete from Bus_Hours")
    cursor.execute("delete from Bus_Neighborhoods")
    cursor.execute("delete from Bus_Attributes")
    cursor.execute("delete from Bus_Categories")
    cursor.execute("delete from Business")


def drop_indexes(cursor):
    try:
        cursor.execute("DROP INDEX Bus_Hours_day_of_week_index ON Bus_Hours")
        cursor.execute("DROP INDEX Bus_Attributes_attribute_index ON Bus_Attributes")
        cursor.execute("DROP INDEX Business_city_index ON Business")
        cursor.execute("DROP INDEX Business_stars_index ON Business")
        cursor.execute("DROP INDEX Business_state_index ON Business")
        cursor.execute("ALTER TABLE Bus_Hours DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE Bus_Neighborhoods DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE Bus_Attributes DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE Bus_Categories DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE Business DROP PRIMARY KEY")
    except:
        pass


def create_indexes(cursor):
    try:
        cursor.execute("CREATE INDEX Bus_Hours_day_of_week_index ON Bus_Hours (day_of_week)")
        cursor.execute("CREATE INDEX Bus_Attributes_attribute_index ON Bus_Attributes (attribute)")
        cursor.execute("CREATE INDEX Business_city_index ON Business (city)")
        cursor.execute("CREATE INDEX Business_stars_index ON Business (stars)")
        cursor.execute("CREATE INDEX Business_state_index ON Business (state)")
        cursor.execute("ALTER TABLE Bus_Hours ADD PRIMARY KEY (business_id, day_of_week)")
        cursor.execute("ALTER TABLE Bus_Neighborhoods ADD PRIMARY KEY (business_id, neighborhood)")
        cursor.execute("ALTER TABLE Bus_Attributes ADD PRIMARY KEY (business_id, attribute)")
        cursor.execute("ALTER TABLE Bus_Categories ADD PRIMARY KEY (business_id, category)")
        cursor.execute("ALTER TABLE Business ADD PRIMARY KEY (business_id)")
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
    print "Processing Business File the batched way, batch size = {}".format(batch_size)

    start_time = time.time()
    update_time = start_time
    list_of_ybos = []
    with open(file_path) as the_file:
        for a_line in the_file:
            json_object = json.loads(a_line)
            list_of_ybos.append(YelpBusiness(json_object))
            row_count += 1
            if row_count % batch_size == 0:
                persist_list_o_business_objects(list_of_ybos,cursor)
                list_of_ybos=[]

            if row_count % 1000 == 0:
                total_time = (time.time() - start_time)
                time_since_last_post = time.time() - update_time
                update_time = time.time()
                print "Up to row {:} in Business file.  Total Time: {:.4g}; TimeSinceLastPost:{:.4g}".format(row_count, total_time, time_since_last_post)

            if how_many > 0 and row_count % how_many == 0:
                break

        #catch the stragglers
        persist_list_o_business_objects(list_of_ybos,cursor)

    print("--- %s seconds ---" % (time.time() - start_time))

    print "Creating indexes"
    create_indexes(cursor)

    db.commit()
    db.close()

    print "Business File Complete.  {0} rows processed".format(row_count)


def flatten_attributes(attributes):
    # Attributes will be a dictionary
    # some of the elements will *also* be dictionaries
    # this function flattens the result into a flattened reference
    ret = {}
    good_for_kids_count = 0
    for k, v in attributes.iteritems():
        if isinstance(v, collections.MutableMapping):
            for k1, v1 in v.iteritems():
                ret["{0}.{1}".format(k,k1)] = v1
        else:
            if k != 'Good for Kids': #eliminate this case.  there is another just like it.
                ret[k] = v

    return ret

def persist_list_o_business_objects(list_o_ybos, cursor):
    #Similar to the others except that it builds up the sets
    business_data = []
    business_set_count = 0
    bus_attributes_data = []
    bus_attributes_set_count = 0
    bus_categories_data = []
    bus_categories_set_count = 0
    bus_neighborhoods_data = []
    bus_neighborhoods_set_count = 0
    bus_hours_data = []
    bus_hours_set_count = 0
    for ybo in list_o_ybos:
        business_data+=[ybo.business_id, ybo.type, ybo.name, ybo.city, ybo.state,
                                ybo.full_address,
                                ybo.latitude, ybo.longitude, ybo.stars, ybo.review_count, ybo.open]
        business_set_count +=1
        for attribute, attribute_value in ybo.attributes.iteritems():
            bus_attributes_data+=[ybo.business_id, attribute, attribute_value]
            bus_attributes_set_count +=1
        for cat in ybo.categories:
            bus_categories_data+=[ybo.business_id, cat]
            bus_categories_set_count += 1
        for hood in ybo.neighborhoods:
            bus_neighborhoods_data+=[ybo.business_id, hood]
            bus_neighborhoods_set_count += 1
        for day, times in ybo.hours.iteritems():
            bus_hours_data+=[ybo.business_id, day, times['open'], times['close']]
            bus_hours_set_count += 1

    try:
        if business_set_count > 0:
            sql_base = " INSERT INTO Business " \
                  " (business_id, type, name, city, state, full_address, " \
                  " latitude, longitude, stars, review_count, open) " \
                  " values {}"
            parameter_base ="(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql = sql_base.format(", ".join([parameter_base]*business_set_count))
            cursor.execute(sql, business_data)

        if bus_attributes_set_count > 0:
            sql_base = " INSERT INTO Bus_Attributes " \
                      " (business_id, attribute, attribute_value) " \
                      " values {}"
            parameter_base = "(%s, %s, %s)"
            sql = sql_base.format(", ".join([parameter_base]*bus_attributes_set_count))
            cursor.execute(sql, bus_attributes_data)

        if bus_categories_set_count > 0:
            sql_base = " INSERT INTO Bus_Categories " \
                  " (business_id, category) " \
                  " values {}"
            parameter_base = "(%s, %s)"
            sql = sql_base.format(", ".join([parameter_base]*bus_categories_set_count))
            cursor.execute(sql, bus_categories_data)


        if bus_neighborhoods_set_count > 0:
            sql_base = " INSERT INTO Bus_Neighborhoods " \
                  " (business_id, neighborhood) " \
                  " values {}"
            parameter_base = "(%s, %s)"
            sql = sql_base.format(", ".join([parameter_base]*bus_neighborhoods_set_count))
            cursor.execute(sql, bus_neighborhoods_data)

        if bus_hours_set_count > 0:
            sql_base = " INSERT INTO Bus_Hours " \
                  " (business_id, day_of_week, open_time, close_time) " \
                  " VALUES {}"
            parameter_base = "(%s, %s, %s, %s)"
            sql = sql_base.format(", ".join([parameter_base]*bus_hours_set_count ))
            cursor.execute(sql, bus_hours_data)

        cursor.connection.commit()
    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err

def persist_business_object(ybo, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type ybo: YelpBusiness
    :type cursor: MySQLdb.cursor
    """
    try:
        # Business
        sql = " INSERT INTO Business " \
              " (business_id, type, name, city, state, full_address, " \
              " latitude, longitude, stars, review_count, open) " \
              " values " \
              " (%s, %s, %s, %s, %s, %s, " \
              " %s, %s, %s, %s, %s) "
        cursor.execute(sql, [ybo.business_id, ybo.type, ybo.name, ybo.city, ybo.state,
                                ybo.full_address,
                                ybo.latitude, ybo.longitude, ybo.stars, ybo.review_count, ybo.open])
        # Bus_Attributes
        for attribute, attribute_value in ybo.attributes.iteritems():
            sql = " INSERT INTO Bus_Attributes " \
                  " (business_id, attribute, attribute_value) " \
                  " values " \
                  " (%s, %s, %s) "
            cursor.execute(sql, [ybo.business_id, attribute, attribute_value])

        # Bus_Categories
        for cat in ybo.categories:
            sql = " INSERT INTO Bus_Categories " \
                  " (business_id, category) " \
                  " values " \
                  " (%s, %s) "
            cursor.execute(sql, [ybo.business_id, cat])
        # Bus_Neighborhoods
        for hood in ybo.neighborhoods:
            sql = " INSERT INTO Bus_Neighborhoods " \
                  " (business_id, neighborhood) " \
                  " values " \
                  " (%s, %s) "
            cursor.execute(sql, (ybo.business_id, hood))
        # Bus_Hours
        # This one is a bit more squirrely. The 'hours' is a dictionary itself
        for day, times in ybo.hours.iteritems():
            sql = " INSERT INTO Bus_Hours " \
                  " (business_id, day_of_week, open_time, close_time) " \
                  " VALUES " \
                  " (%s, %s, %s, %s) "
            cursor.execute(sql,[ybo.business_id, day, times['open'], times['close']])

#        cursor.connection.commit()
    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err
        print "Error with business_id {0}".format(ybo.business_id)
        raise

if __name__ == '__main__':
    the_file = 'C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_business.json'
    parse_file(the_file, 101, 5000)
    #61184 records
