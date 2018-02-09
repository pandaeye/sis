# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem
import psycopg2
import logging


class SisSpiderPipeline(object):
    def __init__(self):
        self.file = open('papers.json','wb')
    def process_item(self, item, spider):
        if item['title']:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
            return item
        else:
            raise DropItem("missing title in %s" %item)
class SisSpiderPipelineSQL(object):
    def __init__(self):
        self.postgresconn = psycopg2.connect(database="postgres", user="postgres", password="6584201", host="127.0.0.1", port="5432")
        self.cursor = self.postgresconn.cursor()
        
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
        fh = logging.FileHandler('sql.log')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.setLevel(logging.ERROR)
            
    def process_item(self, item, spider):
        if item['title'] and item['addr']:
            sql="insert into scrapy_sis_error(title,addr) values(%s,%s)"
            try:
                self.logger.info(sql)
                self.cursor.execute(sql,(item['title'],item['addr']))
                self.postgresconn.commit()
            except:
                self.logger.error(sql)
                self.logger.exception('this is an exception message')
                self.postgresconn.rollback()
            return item
        else:
            raise DropItem("missing title in %s" %item)
        
