# -*- coding: UTF-8 -*-
__author__ = 'li'
import MySQLdb
from read_config import config

user = config.get('database', 'db_user')
pwd = config.get('database', 'db_password')
host = config.get('database', 'db_ip')
db = config.get('database', 'db_name')
port = int(config.get('database', 'db_port'))
"""
get data from db
type:帖子类型 1：代表帖子 2：代表城市帖子
"""


def get_data(select_sql, type):
    cnx = MySQLdb.connect(user=user, passwd=pwd, port=port, host=host, db=db, charset="utf8")
    cursor = cnx.cursor()
    d = {}
    try:
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        for row in rows:

            if type == 1:
                key = ''.join([row[11], '_', str(row[12])])

            else:
                key = ''.join([row[11][0:5], '_', str(row[12])])
            if key not in d:
                d[key] = []
                d[key].append(row)
            else:
                d[key].append(row)
        return d
    except Exception as err:
        print("query database' failed.")
        print("Error: {}".format(err.msg))
    finally:
        cursor.close()
        cnx.close()


