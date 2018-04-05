import pymysql

#连接数据库
conn = pymysql.connect(host='localhost', user='root', password='123456', db='mysql', port=3306,charset='utf8mb4')

#创建新用户
sql="CREATE USER 'linchuhai'@'localhost' IDENTIFIED BY '123456';"
conn.query(sql)
conn.commit()

#授予用户root所有权限，并且用于授予其他用户权限功能
sql="GRANT ALL ON *.* TO 'root'@'localhost' IDENTIFIED BY '123456' WITH GRANT OPTION;"
conn.query(sql)
conn.commit()

#设置用户每小时最多的请求次数和连接数
sql="GRANT ALL ON *.* TO 'root'@'localhost' IDENTIFIED BY '123456' WITH MAX_QUERIES_PER_HOUR 3 MAX_USER_CONNECTIONS 1;"
conn.query(sql)
conn.commit()

#查看用户拥有的权限
sql="SHOW GRANTS FOR 'linchuhai'@'localhost';"
conn.query(sql)
conn.commit()

#删除用户权限,这里删除插入权限
sql="REVOKE INSERT ON *.* FROM 'linchuhai'@'localhost'"
conn.query(sql)
conn.commit()

#删除用户
sql="DROP USER 'linchuhai'@'localhost';"
conn.query(sql)
conn.commit()

#关闭连接
conn.close()

