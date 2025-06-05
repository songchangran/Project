# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# pipelines.py
import pymysql

class MySQLPipeline:
    def open_spider(self, spider):
        spider.logger.info("MySQLPipeline 开始连接数据库")
        try:
            self.conn = pymysql.connect(
                host='43.143.173.241',
                user='root',
                password='123456',
                database='cj_data',
                charset='utf8mb4',
                port=3306
            )
            self.cursor = self.conn.cursor()
            spider.logger.info("MySQL 连接成功")
        except Exception as e:
            spider.logger.error(f"MySQL 连接失败: {e}")

    def process_item(self, item, spider):
        try:
            sql = "INSERT INTO jinshishuju (time, data, importance, previous, consensus, actual) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (item['time'], item['data'], item['importance'], item['previous'], item['consensus'], item['actual'])
            self.cursor.execute(sql, params)
            self.conn.commit()
            spider.logger.info(f"写入数据库成功: {params}")
        except Exception as e:
            spider.logger.error(f"MySQL 写入失败: {e}")
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        spider.logger.info("MySQL连接关闭")
