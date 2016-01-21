"""
LoadReview.py: This file is for parsing the review JSON file and loading the database
Assumes that the database has been built
"""
import json
import MySQLdb
from database import login_info
import time

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

def clear_tables(cursor):
    cursor.execute("delete from Review_Votes")
    cursor.execute("delete from Review")



def drop_indexes(cursor):
    try:
        cursor.execute("DROP INDEX Review_Business_id_index ON review")
        cursor.execute("DROP INDEX Review_date_index ON review")
        cursor.execute("DROP INDEX Review_stars_index ON review")
        cursor.execute("DROP INDEX Review_user_id_index ON review")
        cursor.execute("DROP INDEX Review_Votes_Business_id_index ON review_votes")
        cursor.execute("DROP INDEX Review_Votes_User_id_index ON review_votes")
        cursor.execute("DROP INDEX Review_Votes_vote_type_index ON review_votes")
        cursor.execute("ALTER TABLE Review_Votes DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE Review DROP PRIMARY KEY")
    except:
        pass


def create_indexes(cursor):
    try:
        cursor.execute("CREATE INDEX Review_Business_id_index ON review (business_id)")
        cursor.execute("CREATE INDEX Review_date_index ON review (review_date)")
        cursor.execute("CREATE INDEX Review_stars_index ON review (stars)")
        cursor.execute("CREATE INDEX Review_user_id_index ON review (user_id)")
        cursor.execute("CREATE INDEX Review_Votes_Business_id_index ON review_votes (business_id)")
        cursor.execute("CREATE INDEX Review_Votes_User_id_index ON review_votes (user_id)")
        cursor.execute("CREATE INDEX Review_Votes_vote_type_index ON review_votes (vote_type)")
        cursor.execute("ALTER TABLE Review_Votes ADD PRIMARY KEY (review_id, business_id, user_id, vote_type)")
        cursor.execute("ALTER TABLE Review ADD PRIMARY KEY (review_id)")
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

    list_of_yros = []
    print "Processing Review File"

    start_time = time.time()
    update_time = start_time
    with open(file_path) as the_file:
        for a_line in the_file:
            json_object = json.loads(a_line)
            list_of_yros.append(YelpReview(json_object))
            row_count += 1
            if row_count % batch_size == 0:
                persist_list_o_review_objects(list_of_yros, cursor)
                list_of_yros=[]

            if row_count % 1000 == 0:
                total_time = (time.time() - start_time)
                time_since_last_post = time.time() - update_time
                update_time = time.time()
                print "Up to row {} in Review file.  Total Time: {}; TimeSinceLastPost:{}".format(row_count, total_time, time_since_last_post)

            if how_many > 0 and row_count % how_many == 0:
                break

        #catch the stragglers
        persist_list_o_review_objects(list_of_yros,cursor)

    print "Creating indexes"
    create_indexes(cursor)

    db.commit()
    db.close()
    print "Review File Complete.  {0} rows processed".format(row_count)

def persist_list_o_review_objects(list_o_yros, cursor):
    review_data = []
    review_set_count = 0
    review_votes_data = []
    review_votes_set_count = 0
    for yro in list_o_yros:
        review_data+=[yro.review_id, yro.business_id, yro.user_id, yro.stars, yro.review_text, yro.review_date]
        review_set_count+=1
        for vote_type, vote_count in yro.votes.iteritems():
            review_votes_data+=[yro.review_id, yro.business_id, yro.user_id, vote_type, vote_count]
            review_votes_set_count+=1
    try:
        if review_set_count > 0:
            sql_base = " INSERT INTO Review " \
              " (review_id, business_id, user_id, stars, review_text, review_date) " \
              " values {}"
            parameter_base = "(%s, %s, %s, %s, %s, %s)"
            sql = sql_base.format(", ".join([parameter_base]* review_set_count))
            cursor.execute(sql, review_data)
        if review_votes_set_count > 0:
            sql_base = " INSERT INTO Review_Votes " \
                  " (review_id, business_id, user_id, vote_type, vote_count) " \
                  " values {}"
            parameter_base = "(%s, %s, %s, %s, %s)"
            sql = sql_base.format(", ".join([parameter_base]* review_votes_set_count))
            cursor.execute(sql, review_votes_data)

        cursor.connection.commit()

    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err


def persist_review_object(yro, cursor):
    # We know all of the attributes we can have
    # and what their types are
    # this first pass, I'm not going to try and be clever..just work my way down
    """
    :type yro: YelpReview
    :type cursor: MySQLdb.cursor
    """
    try:
        # Review
        sql = " INSERT INTO Review " \
              " (review_id, business_id, user_id, stars, review_text, review_date) " \
              " values " \
              " (%s, %s, %s, %s, %s, %s) "
        cursor.execute(sql, [yro.review_id, yro.business_id, yro.user_id, yro.stars, yro.review_text, yro.review_date])

        #Review_Votes
        for vote_type, vote_count in yro.votes.iteritems():
            sql = " INSERT INTO Review_Votes " \
                  " (review_id, business_id, user_id, vote_type, vote_count) " \
                  " values " \
                  " (%s, %s, %s, %s, %s) "
            cursor.execute(sql, [yro.review_id, yro.business_id, yro.user_id, vote_type, vote_count])

        cursor.connection.commit()
    except MySQLdb.Error as err:
        cursor.connection.rollback()
        print err
        print "Error with review_id {0}, business_id {1}, user_id {2}".format(yro.review_id, yro.business_id, yro.user_id)



if __name__ == '__main__':
    the_file = 'C:\\Users\\matt\\GA_DataScience\\DataScienceProject\\Yelp\\yelp_academic_dataset_review.json'
    #the_file = '/home/ubuntu/projects/ga_yelp/yelp_data_raw/yelp_academic_dataset_review.json'
    parse_file(the_file, 101, 5000)
    #1569264 records