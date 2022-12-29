from pymysql import Connect

# ！  C:\Users\熊健熹\AppData\Local\Programs\Python\Python310
# _*_ coding: UTF-8 _*_
'''
@Project :webservers
@File    :test_db_conn.py.py
@Author  :magic007
@Date    : 11:20
'''

conn = Connect(host='centos',
               port=3306,
               user='root',
               password='123456',
               db='magic007',
               charset='utf8'
               )

print("--连接成功--")
