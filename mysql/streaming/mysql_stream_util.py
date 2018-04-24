import datetime
import MySQLdb # python 3
import pandas as pd
import time
import numpy as np

host = "enter host"
user="enter user"
passwd="enter password"
db="enter db"

def start_conn():
    for i in range(0,100):
        conn = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
        cursor = conn.cursor()

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        value = np.random.randint(0,10)

        data = [(date, value)]

        # change query accordingly
        sql = "insert into stream_table(date, value) VALUES(%s, %s)"

        number_of_rows = cursor.executemany(sql, data)
        conn.commit()
        time.sleep(10)

start_conn()
