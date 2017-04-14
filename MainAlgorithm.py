# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 12:18:29 2016

@author: 64510
"""

import mysql.connector
import pandas as pd
import numpy as np
from pandas import Series
from pandas import DataFrame
import time

def GetData():
    conn = mysql.connector.connect(
#                host = 'localhost',
#                port = 0,
                user = 'root',
                passwd = 'root',
                db = 'ir',
                )
    cur = conn.cursor()
   
    cur.execute("select bookid,userid,rating from bookrating")
    info = cur.fetchall()
#    info = {'user_id':[1,1,1,2,2,2,3,3,3,3,4,4] ,
#            'book_id':[1,2,3,2,3,4,1,2,3,4,2,3] ,
#            'rating' :[3,2.7,2.9,1,3,5,2.5,2,4.2,5.5,3,3.1]}
    
    ratings = pd.DataFrame(info,columns = [ 'book_id', 'user_id', 'rating'])
    
    cur.close()
    conn.commit()
    conn.close()
    
    data = ratings.pivot(index = 'user_id', columns = 'book_id', values = 'rating')
    return data

def PutData(values):
    conn = mysql.connector.connect(
#                host = 'localhost',
#                port = 0,
                user = 'root',
                passwd = 'root',
                db = 'ir',
                )
    cur = conn.cursor()
    
    cur.execute('delete from bookrecommend')
    cur.executemany('insert into bookrecommend (userid,book1,book2,book3,book4,book5) values(%s,%s,%s,%s,%s,%s)',values)
    cur.close()
    conn.commit()
    conn.close()

def UserBasedCF(data, UserID):
    corr = data.T.corr(method = 'pearson', min_periods = 1)
    corr_clean = corr.dropna(how = 'all')
    corr_clean = corr_clean.dropna(axis = 1, how = 'all')
    gift = data.ix[UserID]
    gift = gift[gift.isnull()]
    
    corr_UserID = corr_clean[UserID].drop(UserID)
    corr_UserID = corr_UserID[corr_UserID > 0.1].dropna()
    for book in gift.index:
        prediction = []
        for other in corr_UserID.index:
            if not np.isnan(data.ix[other, book]):
                prediction.append((data.ix[other, book], corr_clean[UserID][other]))
        if prediction:
            gift[book] = sum([value*weight for value,weight in prediction])/sum([pair[1] for pair in prediction])
    gift = gift.dropna().order(ascending = False)
    return gift

def ItemBasedCF(data):
    rating = data.mean()
    rating = rating.order(ascending = False)  
    return rating
    
if __name__ == '__main__':
    while(True):
        data = GetData()
        values = []
        rating = ItemBasedCF(data)
        for UserID in data.index:
            value = UserBasedCF(data, UserID)
            value = value + 0.1*rating
            value = value.dropna().order(ascending = False)
            newvalue = list(value.index)
            newvalue[0:0] = [UserID]
#            newvalue = []
#            newvalue = newvalue.append(UserID)
#            newvalue = newvalue.extend(newvalue1)
#            newvalue1= np.array([0,0,0,0,0])
#            newvalue1 = newvalue1 + newvalue;
            i = len(newvalue)
            if i>5:
                newvalue = newvalue[0:6]
            else:
                while (i<6):
                    newvalue.append(0)
                    i += 1
            for num in range(0,6):
                newvalue[num] = int(newvalue[num])
            values.append((newvalue))
        PutData(values)
        time.sleep(5)