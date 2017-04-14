# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 12:23:39 2016

@author: 64510
"""
import mysql.connector
import pandas as pd
import numpy as np
from numpy import random
from pandas import Series
from pandas import DataFrame

conn = mysql.connector.connect(
#                host = 'localhost',
#                port = 0,
                user = 'root',
                passwd = 'root',
                db = 'ir',
                )
cur = conn.cursor()

values = []
randArray = random.uniform( 0, 5, size=600)
for x in range(18905,18935):
    for y in range(0,20):
        values.append((x,y))
random.shuffle(values)

cur.execute('delete from bookrating')
for i in range(0,300):
    cur.execute('insert into bookrating (bookid,userid,rating) values(%s,%s,%s)',[int(values[i][0]),int(values[i][1]),float(randArray[i])])

cur.close()
conn.commit()
conn.close()