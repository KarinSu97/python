import pymysql
import pandas as pd

#连接数据库
conn = pymysql.connect(host='localhost', user='root', password='123456', db='test', port=3306,charset='utf8mb4')

#定义json字段
sql='CREATE TABLE g (\
	uid INT PRIMARY KEY AUTO_INCREMENT,\
	data json\
)'
sql='INSERT INTO g VALUES (NULL,"{"data":1,"name":"linchuhai","age":18}")'
sql="INSERT INTO g VALUES (NULL,'{\"data\":3,\"name\":\"lucy\",\"age\":17}')"


#解析json字段的数据
sql='SELECT json_extract(data,"$.name"),json_extract(data,"$.age") FROM g'
data=pd.read_sql(sql,conn)
data

#将某个表的多个字段转化为json数据
sql='INSERT INTO g SELECT id + 3 AS uid,json_object ("sex", sex) AS DATA FROM e'

#将json数据中几个字段合并为列表
sql='''
SELECT
	uid,
	json_merge (
		json_extract (DATA, '$.province'),
		json_extract (DATA, '$.adress')
	)
FROM
	g;
'''


#将json数据中某些字段合并为列表
sql='''
UPDATE g
SET DATA = json_array_append (
    DATA,
    '$.adress',
    json_extract (DATA, '$.province')
)
WHERE
    json_extract (DATA, '$.province') IS NOT NULL
AND uid > 0
'''

#删除json数据中某个字段
sql='''
UPDATE g
SET DATA = json_remove (DATA, "$.province")
WHERE
	uid > 0
'''

#以json数据中某个字段创建索引
#创建虚拟列
sql='''
ALTER TABLE users ADD COLUMN first_name VARCHAR (128)  AS (
	json_extract (DATA, "$.first_name")
);
'''
#创建索引，idx_name为索引的名字
sql='ALTER TABLE users ADD INDEX idx_name (first_name)'

