"""
LoadUser.py:This file is for parsing the user JSON file and loading the database
Assumes that the database has been built
"""
import json
import MySQLdb
from database import login_info
import time

class YelpUser:
    """organize user data"""

    def __init__(self, yelp_json_object):
        if 'user_id' in yelp_json_object:
            self.user_id = yelp_json_object['user_id']
        if 'name' in yelp_json_object:
            self.name = yelp_json_object['name']
        if 'review_count' in yelp_json_object:
            self.review_count = yelp_json_object['review_count']
        if 'average_stars' in yelp_json_object:
            self.average_stars = yelp_json_object['average_stars']
        if 'yelping_since' in yelp_json_object:
            self.yelping_since = yelp_json_object['yelping_since']
        if 'fans' in yelp_json_object:
            self.fans = yelp_json_object['fans']
        if 'votes' in yelp_json_object:
            self.votes = yelp_json_object['votes']
        if 'friends' in yelp_json_object:
            self.friends = yelp_json_object['friends']
        if 'elite' in yelp_json_object:
            self.elite = yelp_json_object['elite']
        if 'compliments' in yelp_json_object:
            self.compliments = yelp_json_object['compliments']

def clear_tables(cursor):
    try:
        cursor.execute("delete from User_Votes")
        cursor.execute("delete from User_Friends")
        cursor.execute("delete from User_Elite")
        cursor.execute("delete from User_Compliments")
        cursor.execute("delete from User")
    except:
        pass

def drop_indexes(cursor):
    try:
        cursor.execute("DROP INDEX User_Compliments_compliment_type_index ON user_compliments")
        cursor.execute("DROP INDEX User_Compliments_user_id_index ON user_compliments")
        cursor.execute("DROP INDEX User_Elite_user_id_index ON user_elite")
        cursor.execute("DROP INDEX User_Friends_friends_index ON user_friends")
        cursor.execute("DROP INDEX User_Friends_user_id_index ON user_friends")
        cursor.execute("DROP INDEX User_Votes_user_id_index ON user_votes")
        cursor.execute("DROP INDEX User_Votes_vote_type_index ON user_votes")
        cursor.execute("ALTER TABLE User_Votes DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE User_Friends DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE User_Elite DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE User_Compliments DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE User DROP PRIMARY KEY")

    except:
        pass


def create_indexes(cursor):
    try:
        cursor.execute("CREATE INDEX User_Compliments_compliment_type_index ON user_compliments (compliment_type)")
        cursor.execute("CREATE INDEX User_Compliments_user_id_index ON user_compliments (user_id)")
        cursor.execute("CREATE INDEX User_Elite_user_id_index ON user_elite (user_id)")
        cursor.execute("CREATE INDEX User_Friends_friends_index ON user_friends (friends)")
        cursor.execute("CREATE INDEX User_Friends_user_id_index ON user_friends (user_id)")
        cursor.execute("CREATE INDEX User_Votes_user_id_index ON user_votes (user_id)")
        cursor.execute("CREATE INDEX User_Votes_vote_type_index ON user_votes (vote_type)")
        cursor.execute("ALTER TABLE User_Votes ADD PRIMARY KEY (user_id, vote_type)")
        cursor.execute("ALTER TABLE User_Friends ADD PRIMARY KEY (user_id, friends)")
        cursor.execute("ALTER TABLE User_Elite ADD PRIMARY KEY (user_id, years_elite)")
        cursor.execute("ALTER TABLE User_Compliments ADD PRIMARY KEY (user_id, compliment_type)")
        cursor.execute("ALTER TABLE User ADD PRIMARY KEY (user_id)")
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
    list_of_yuos = []
    print "Processing User File"

    start_time = time.time()
    update_time = start_time
    with open(file_path) as the_file:
        for a_line in the_file:
            json_object = json.loads(a_line)
            list_of_yuos.append(YelpUser(json_object))
            row_count += 1
            if row_count % batch_size == 0:
                persist_list_o_user_objects(list_of_yuos, cursor)
                list_of_yuos=[]

            if row_count % 1000 == 0:
                total_time = (time.time() - start_time)
                time_since_last_post = time.time() - update_time
                update_time = time.time()
                print "Up to row {:} in User file.  Total Time: {:.4g}; TimeSinceLastPost:{:.4g}".format(row_count, total_time, time_since_last_post)

            if how_many > 0 and row_count % how_many == 0:
                break

        #catch the stragglers
        persist_list_o_user_objects(list_of_yuos,cursor)

    print "Creating indexes"
    create_indexes(cursor)

    db.commit()
    db.close()

    print "User File complete.  {0} rows processed".format(row_count)


def persist_list_o_user_objects(list_o_yuos, cursor):
    user_data = []
    user_set_count = 0
    user_compliments_data = []
    user_compliments_set_count = 0
    user_elite_data = []
    user_elite_set_count = 0
    user_friends_data = []
    user_friends_set_count = 0
    user_votes_data = []
    user_votes_set_count = 0
    for yuo in list_o_yuos:
        user_data+=[yuo.user_id, yuo.name, yuo.review_count, yuo.average_stars, yuo.yelping_since, yuo.fans]
        user_set_count+=1
        for comp_type, comp_count in yuo.compliments.iteritems():
            user_compliments_data+=[yuo.user_id, comp_type, comp_count]
            user_compliments_set_count+=1
        for years in yuo.elite:
            user_elite_data+=[yuo.user_id, years]
            user_elite_set_count+=1
        for friend in yuo.friends:
            user_friends_data+=[yuo.user_id, friend]
            user_friends_set_count+=1
        for vote_type, vote_count in yuo.votes.iteritems():
            user_votes_data+=[yuo.user_id, vote_type, vote_count]
            user_votes_set_count+=1
    try:
        if user_set_count > 0:
            sql_base = " INSERT INTO User " \
              " (user_id, name, review_count, average_stars, yelping_since, fans)" \
              " values {}"
            parameter_base = "(%s, %s, %s, %s, %s, %s)"
            sql = sql_base.format(", ".join([parameter_base]* user_set_count))
            cursor.execute(sql, user_data)
        if user_compliments_set_count > 0:
            sql_base = "INSERT INTO User_Compliments " \
                  " (user_id, compliment_type, compliment_count) " \
                  " values {}"
            parameter_base = "(%s, %s, %s)"
            sql = sql_base.format(", ".join([parameter_base]* user_compliments_set_count))
            cursor.execute(sql, user_compliments_data)
        if user_elite_set_count > 0:
            sql_base = "INSERT INTO User_Elite " \
                  " (user_id, years_elite) " \
                  " values {}"
            parameter_base = "(%s, %s)"
            sql = sql_base.format(", ".join([parameter_base]* user_elite_set_count))
            cursor.execute(sql, user_elite_data)
        if user_friends_set_count > 0:
            sql_base = "INSERT INTO User_Friends " \
                  " (user_id, friends) " \
                  " values {}"
            parameter_base = "(%s, %s)"
            sql = sql_base.format(", ".join([parameter_base]* user_friends_set_count))
            cursor.execute(sql, user_friends_data)
        if user_votes_set_count > 0:
            sql_base = "INSERT INTO User_Votes " \
                  " (user_id, vote_type, vote_count) " \
                  " values {}"
            parameter_base = "(%s, %s, %s)"
            sql = sql_base.format(", ".join([parameter_base]* user_votes_set_count))
            cursor.execute(sql, user_votes_data)

        cursor.connection.commit()

    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err

if __name__ == '__main__':
    the_file = 'C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_user.json'
    parse_file(the_file, 101, 5000)
    #366715 records
