# This is largely a sandbox tool

import MySQLdb
from database import login_info
"""
if __name__ == '__main__':
    db = MySQLdb.connect(**login_info)
    cursor = db.cursor()

    sql = " INSERT INTO sandbox " \
          " (int_col, string_col, decimal_col)" \
          " values " \
          " (%s, %s, %s) "
    cursor.execute(sql, [1,"two's", "4.4"])
    cursor.connection.commit()
    db.close()

"""
out_of_main = []

def some_function():
    for i in xrange(0,10):
        in_main.append(i)
        if i % 2 == 0:
            out_of_main.append(i)

def some_other_function():
    print len(in_main)
    print len(out_of_main)

if __name__ == '__main__':
    in_main = []
    some_function()
    some_other_function()