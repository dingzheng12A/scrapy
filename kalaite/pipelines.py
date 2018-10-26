# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='devops', password='devops', charset='utf8', db='Devops')
cursor=conn.cursor()
f=open("b.txt","a")
class KalaitePipeline(object):
    def process_item(self, item, spider):
        #print("item Url:%s" % item['img_url'])
        print("all content:%s" % item['allcontent'])
        if len(item['title']) != 0 and item['type'] == "news":
                sql="INSERT INTO Devops.spider_news(title,content,allcontent,img_url,createtime)VALUES(%s,%s,%s,%s,%s)"
                cursor.execute(sql,("".join(item['title']),"".join(item['content']),"".join(item['allcontent']),"|".join(item['img_url']),"".join(item['date'])))
                conn.commit()
        elif len(item['title']) != 0 and item['type'] == "product":
                sql="INSERT INTO Devops.spider_product(title,content,allcontent,img_url,createtime)VALUES(%s,%s,%        s,%s,%s)"
                cursor.execute(sql,("".join(item['title']),"".join(item['content']),"".join(item['allcontent']        ),"|".join(item['img_url']),"".join(item['date'])))
                conn.commit()

        #f.write(item)
        return item
