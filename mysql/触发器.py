import pymysql
import pandas as pd

#连接数据库
conn = pymysql.connect(host='localhost', user='root', password='123456', db='test', port=3306,charset='utf8mb4')

#创建触发器
sql='''
delimiter //
CREATE TRIGGER upd_score BEFORE INSERT ON a FOR EACH ROW
BEGIN
IF NEW.score < 0 THEN
    SET NEW.score = 0;
ELSEIF NEW.score > 100 THEN
SET NEW.score = 100;
END IF;
END;//
delimiter ;
'''