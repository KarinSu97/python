#html形式邮件
import smtplib
from email.mime.text import MIMEText

sender='linchuhai123@163.com'   #发送者
receiver='1173229840@qq.com'   #接收者
subject='程序跑完提醒'   #主题
smtpserver='smtp.163.com'   #设置服务器
username='linchuhai123'   #用户名
password='2012050355lch'   #密码
msg=MIMEText('<html><h1>程序已经跑完</h1></html>','html','utf-8')   #邮件正文
msg['Subject']=subject   #主题

smtp=smtplib.SMTP()
smtp.connect(smtpserver)   #连接服务器
smtp.login(username,password)   #登陆
smtp.sendmail(sender,receiver,msg.as_string())   #发送邮件
smtp.quit()