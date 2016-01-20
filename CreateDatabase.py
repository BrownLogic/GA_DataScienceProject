# This is largely a sandbox tool

import MySQLdb
from database import login_info

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

