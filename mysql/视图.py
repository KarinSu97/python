import pymysql
import pandas as pd

#连接数据库
conn = pymysql.connect(host='localhost', user='root', password='123456', db='test', port=3306,charset='utf8mb4')

#创建视图
sql='''
CREATE VIEW `NewView`AS 
SELECT * from score WHERE score.score>=80 ;
'''