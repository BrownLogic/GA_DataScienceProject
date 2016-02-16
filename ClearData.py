"""
ClearData.py: Clears all of the (known) tables in ProjectDB.
Redundant since each file load has their own 'clear' functions.

"""
import MySQLdb
from database import login_info

def clear_tables(tables, cursor):
    """
    Clears contents of tables in list.

    :param tables: List of tables to delete
    :param cursor: Open MySQLdb cursor
    """
    for table in tables:
        cursor.execute('delete from {0}'.format(table))


def clear_business(cursor):
    """
    Clears tables related to the Business file
    :param cursor: Open MySQLdb cursor
    """
    tables = ['Bus_Attributes', 'Bus_Categories', 'Bus_hours', 'Bus_Neighborhoods', 'Business']
    clear_tables(tables, cursor)


def clear_categories(cursor):
    """
    Clears tables related to the Categories file
    :param cursor: Open MySQLdb cursor
    """
    tables = ['categories', 'cat_parents', 'ct_country_list']
    clear_tables(tables, cursor)


def clear_review(cursor):
    """
    Clears tables related to the Review file
    :param cursor: Open MySQLdb cursor
    """
    tables = ['Review', 'Review_Votes']
    clear_tables(tables, cursor)


def clear_checkins(cursor):
    """
    Clears tables related to the CheckIn file
    :param cursor: Open MySQLdb cursor
    """
    tables = ['Checkins']
    clear_tables(tables, cursor)


def clear_tips(cursor):
    """
    Clears tables related to the Tip file
    :param cursor: Open MySQLdb cursor
    """
    tables = ['User_Tips']
    clear_tables(tables, cursor)


def clear_user(cursor):
    """
    Clears tables related to the User file
    :param cursor: Open MySQLdb cursor
    """
    tables = ['User_Votes', 'User_Friends', 'User_Elite', 'User_Compliments', 'User']
    clear_tables(tables, cursor)


def clear_database():
    """
    Opens a connection and clears all databases
    """
    db = MySQLdb.connect(**login_info)

    cursor = db.cursor()
    clear_business(cursor)
    clear_checkins(cursor)
    clear_review(cursor)
    clear_tips(cursor)
    clear_user(cursor)
    db.commit()
    db.close()


if __name__ == '__main__':
    clear_database()
