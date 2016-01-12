import sqlite3

def clear_tables(tables, cursor):
    for table in tables:
        cursor.execute("delete from {0}".format(table))


def clear_business(cursor):
    tables = ['Bus_Attributes', 'Bus_Categories', 'Bus_hours', 'Bus_Neighborhoods', 'Business']
    clear_tables(tables, cursor)


def clear_review(cursor):
    tables = ['Review','Review_Votes']
    clear_tables(tables, cursor)


def clear_checkins(cursor):
    tables = ['Checkins']
    clear_tables(tables, cursor)


def clear_tips(cursor):
    tables = ['User_Tips']
    clear_tables(tables, cursor)


def clear_user(cursor):
    tables = ['User_Votes', 'User_Friends', 'User_Elite', 'User_Compliments', 'User']
    clear_tables(tables, cursor)

def clear_database():
    db = sqlite3.connect("DsProject.db")
    cursor = db.cursor()
    clear_business(cursor)
    clear_checkins(cursor)
    clear_review(cursor)
    clear_tips(cursor)
    clear_user(cursor)
    cursor.execute(("vacuum")) #optional...reclaims space
    db.commit()
    db.close()


if __name__ == '__main__':
    clear_database()
