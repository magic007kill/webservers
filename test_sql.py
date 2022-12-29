# ！  C:\Users\熊健熹\AppData\Local\Programs\Python\Python310
# _*_ coding: UTF-8 _*_
'''
@Project :webservers
@File    :test_sql.py
@Author  :magic007
@Date    : 13:16
'''
from pymysql import Connect



conn = Connect(host='centos',
               port=3306,
               user='root',
               password='123456',
               db='magic007',
               charset='utf8'
               )

print("--连接成功--")

cursor = conn.cursor()

sql = 'select * from tb_user'

try:
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    for row in result:
        # id = row[0]
        # name = row[1]
        # phone = row[2]
        # email = row[3]
        # profession = row[4]
        # age = row[5]
        # gender = row[6]
        # status = row[7]
        # createtime = row[8]
        print(row)
except:
    print('Error: unable to fetch data')

conn.close()

