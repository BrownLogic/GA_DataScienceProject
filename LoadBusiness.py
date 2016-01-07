"""
This file is for parsing the business JSON file and loading the database
Assumes that the database has been built
"""
import json
import sqlite3
import collections

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
            persist_business_object(YelpBusiness(json_object), cursor)

            row_count += 1
            if row_count % 1000 == 0:
                print "Up to row {}".format(row_count)

    db.commit()
    db.close()



def flatten_attributes(attributes):
    # Attributes will be a dictionary
    # some of the elements will *also* be dictionaries
    # this function flattens the result into a flattened reference
    ret = {}
    new_key = ''
    new_value = ''

    for k, v in attributes.iteritems():
        if isinstance(v, collections.MutableMapping):
            for k1, v1 in v.iteritems():
                ret["{0}.{1}".format(k,k1)] = v1
        else:
            ret[k] = v

    return ret

def persist_business_object(ybo, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type ybo: YelpBusiness
    :type cursor: sqlite3.cursor
    """
    try:
        # Business
        sql = " INSERT INTO Business " \
              " (business_id, type, name, city, state, full_address, " \
              " latitude, longitude, stars, review_count, open) " \
              " values " \
              " (?, ?, ?, ?, ?, ?, " \
              " ?, ?, ?, ?, ?) "
        cursor.execute(sql, (ybo.business_id, ybo.type, ybo.name, ybo.city, ybo.state,
                                    ybo.full_address,
                                    ybo.latitude, ybo.longitude, ybo.stars, ybo.review_count, ybo.open))
        # Bus_Attributes
        for attribute, attribute_value in ybo.attributes.iteritems():
            sql = " INSERT INTO Bus_Attributes " \
                  " (business_id, attribute, attribute_value) " \
                  " values " \
                  " (?, ?, ?) "
            cursor.execute(sql, (ybo.business_id, attribute, attribute_value))

        # Bus_Categories
        for cat in ybo.categories:
            sql = " INSERT INTO Bus_Categories " \
                  " (business_id, category) " \
                  " values " \
                  " (?, ?) "
            cursor.execute(sql, (ybo.business_id, cat))
        # Bus_Neighborhoods
        for hood in ybo.neighborhoods:
            sql = " INSERT INTO Bus_Neighborhoods " \
                  " (business_id, neighborhood) " \
                  " values " \
                  " (?, ?) "
            cursor.execute(sql, (ybo.business_id, hood))
        # Bus_Hours
        # This one is a bit more squirrely. The 'hours' is a dictionary itself
        for day, times in ybo.hours.iteritems():
            sql = " INSERT INTO Bus_hours " \
                  " (business_id, day_of_week, open_time, close_time) " \
                  " VALUES " \
                  " (?, ?, ?, ?) "
            cursor.execute(sql,(ybo.business_id, day, times['open'], times['close']))

#        cursor.connection.commit()
    except sqlite3.OperationalError:
        cursor.connection.rollback()
        print "Error with business_id {0}".format(ybo.business_id)
        raise


if __name__ == '__main__':
    #parse_file('C:\\Users\\matt\\Documents\\Projects\\SqliteSandbox\\business_one_record.json')
    parse_file('C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_business.json')
    #61184 records
