# -*- coding: utf-8 -*-
"""
Created on Mon May 09 20:16:49 2016

@author: star
"""

#webcrawler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import json
import time

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

Tags=['小说','随笔','散文','日本文学','通话','诗歌','名著','港台'
    ,'漫画','绘本','推理','青春','言情','科幻','武侠','奇幻'
    ,'历史','哲学','传记','设计','建筑','电影','回忆录','音乐'
    ,'旅行','励志','职场','美食','教育','灵修','健康','家居'
    ,'经济学','管理','金融','商业','营销','理财','股票','企业史'
    ,'科普','互联网','编程','交互设计','算法','通信','web','程序']

#html = getHtml("https://api.douban.com/v2/book/search?tag=小说&count=1")
file='data.json'
fp = open(file,'a+')

for tag in Tags:
    html=getHtml("https://api.douban.com/v2/book/search?tag="+tag+"&count=100")
    obj_html=json.dumps(html)
    fp.write(json.loads(obj_html))
    time.sleep(100)
    html=getHtml("https://api.douban.com/v2/book/search?tag="+tag+"&start=100&count=100")
    obj_html=json.dumps(html)
    fp.write(json.loads(obj_html))
    time.sleep(100)

fp.close()
#GET  https://api.douban.com/v2/book/search
#?apikey=0952ab9c793f37fc1bf802d56bbda7f4
#print getImg(html)
#print html