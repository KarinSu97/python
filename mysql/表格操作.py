import pymysql
import pandas as pd

#连接数据库
conn = pymysql.connect(host='localhost', user='root', password='123456', db='test', port=3306,charset='utf8mb4')

#创建表格，INT表示数据类型为整数型，UNSIGNED表示数据都是无符号，即正数
sql="CREATE TABLE a (a INT UNSIGNED,b INT);"
conn.query(sql)
conn.commit()

#删除表格
sql='DROP TABLE a;'
conn.query(sql)
conn.commit()

#插入数据
sql="INSERT INTO a SELECT 1,2;"
conn.query(sql)
conn.commit()

#查询数据
sql='SELECT b-a FROM a;'
data=pd.read_sql(sql,conn)

#定义自增字段，必须是索引的一部分
sql='CREATE TABLE b (a INT AUTO_INCREMENT PRIMARY KEY);'
conn.query(sql)
conn.commit()
sql="INSERT INTO b SELECT NULL;"
sql="INSERT INTO b SELECT -1;"
sql='INSERT INTO b VALUES (NULL),(100),(NULL);'

#修改表中某条记录
sql='UPDATE b set a=0 WHERE a=-1;'
conn.query(sql)
conn.commit()

#查看所有编码格式
sql='SHOW CHARACTER SET;'
conn.query(sql)
conn.commit()

#ENUM，用于创建一个集合，一般是可列举的字段
sql="CREATE TABLE e (id INT PRIMARY KEY AUTO_INCREMENT,sex ENUM('male','female'))"
conn.query(sql)
conn.commit()

#将某个字段转化为指定的类型
sql='SELECT * FROM e ORDER BY CAST(sex AS CHAR) ASC;'

#日期函数
sql="SELECT NOW(6),SYSDATE(6);"   #NOW()表示执行sql语句的时间，SYSDATE()表示执行函数时的时间
sql="SELECT DATE_ADD(NOW(),INTERVAL 5 DAY);"   #日期加
sql="SELECT DATE_SUB(NOW(),INTERVAL 7 DAY);"    #日期减

#设置根据修改自动更新时间
sql='CREATE TABLE f (\
	id INT PRIMARY KEY AUTO_INCREMENT,\
	b INT NOT NULL,\
	c TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP\
);'

#从第5条记录开始，取出5条记录
sql='SELECT * from employees LIMIT 5,5;'

#排序，desc表示降序，asc表示升序
sql='''
SELECT
    *
FROM
    employees
ORDER BY
    emp_no DESC
LIMIT 5;
'''

#表格连接
sql='''
SELECT
    *
FROM
    employees,
    titles
WHERE
    employees.emp_no = titles.emp_no
'''

#表格左连接
sql='''
SELECT
    *
FROM
    employees
LEFT JOIN dept_manager ON employees.emp_no = dept_manager.emp_no
WHERE
    dept_manager.dept_no IS NULL
'''

#字符串连接
sql='''
SELECT
    employees.emp_no,CONCAT(first_name," ",last_name),gender
FROM
    employees,
    titles
WHERE
    employees.emp_no = titles.emp_no
'''

#计算每周的订单量
sql='''
SELECT
    ADDDATE(
        '1970-01-05',
        INTERVAL floor(
            DATEDIFF(payment_date, '1970-01-05') / 7
        ) * 7 DAY
    ) AS START,
    ADDDATE(
        '1970-01-05',
        INTERVAL floor(
            DATEDIFF(payment_date, '1970-01-05') / 7
        ) * 7 + 6 DAY
    ) AS END,
count(payment_id)
FROM
    payment
GROUP BY
    START,END
'''

#排名问题
sql='''
SET @pre_value = NULL;
SET @rank_count = 0;
SELECT
	id,
	score,
	CASE
WHEN @pre_value = score THEN
	@rank_count
WHEN @pre_value := score THEN
	@rank_count :=@rank_count + 1
END AS rank
FROM
	score
ORDER BY
	score.score DESC;
'''