from connect_mysqldb import connect_mysql
import os
unix_socket_path = os.environ["INSTANCE_UNIX_SOCKET"]

# db = connect_mysql()

#with db.connect() as conn:
#    time = conn.execute("SELECT NOW()").fetchone()
#    curr_time = time[0]
#    print(curr_time)

import MySQLdb

db = MySQLdb.connect(unix_socket=unix_socket_path, user="jackwoth")
cursor = db.cursor()
cursor.execute("SELECT NOW()")
time = cursor.fetchone()
print(time)



