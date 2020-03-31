# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class PttscrapyprojectPipeline(object):
#
#     def process_item(self, item, spider):
#         return item
import pymysql

import logging

from twisted.enterprise import adbapi

class PttscrapyprojectPipeline(object):
    '''保存到数据库中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        #读取settings中配置的数据库参数
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    # SQL语句在这里
    def _conditional_insert(self, tx, item):

        sql = "insert into test_db."+str(item['category_db'])+"(author_id,author_name,title_name,published_time,content_text,canonical_url,created_time,update_time,comment_id,comment_text,comment_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #sql = "insert into test_db." + str(item['category_db']) + "(author_id,author_name,title_name,published_time,content_text,canonical_url,created_time,update_time,comment_id,comment_text) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #params = (item['author_id'], item['author_name'], item['title_name'], item['published_time'], item['content_text'],item['canonical_url'], item['created_time'], item['update_time'],item['comment_id'],item['comment_text'])
        params = (item['author_id'], item['author_name'], item['title_name'], item['published_time'],item['content_text'],item['canonical_url'],item['created_time'],item['update_time'],item['comment_id'],item['comment_text'],item['comment_time'])
        tx.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        # logging.error(failue)
        print(failue)