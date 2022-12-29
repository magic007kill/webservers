from pymysql import Connect
from pymysql.cursors import DictCursor

# ！  C:\Users\熊健熹\AppData\Local\Programs\Python\Python310
# _*_ coding: UTF-8 _*_
'''
@Project :webservers
@File    :test_db_conn.py.py
@Author  :magic007
@Date    : 11:20
'''

db = Connect(host='centos',
             port=3306,
             user='root',
             password='123456',
             db='magic007',
             charset='utf8'
             )


def save(table, **item):
    pass


def update(table, pk='id', **item):
    sql = 'update %s set %s where %s'
    # 从item中获取主键的字段值
    # item => {'name':'disen','sex':男}
    # update_fields => name=%(name)s,sex=%(sex)s
    update_fields = ','.join('%s=%%(%s)s' % (k, k) for k in item if k != pk)

    where = f'{pk}=%({pk})s'
    with db.cursor() as c:
        c.execute(sql % (table, update_fields, where), args=item)
        db.commit()  # 提交事务
        return c.rowcount > 0


def query(table, *field, where=None, args=None, one=False):
    # ','.join是用join的方法使用自定义的连接符号（如前句是‘,’）生成新字符串：如‘-’.join('a','b','c') -> 'a-b-c'
    sql = 'select %s from %s' % (','.join(field), table)
    if where:
        sql += ' where ' + where
    # 利用with来做到自动关闭DB的作用，DictCursor参数的作用是指定返回的数据格式为字典
    # c = conn.cursor(DictCursor)
    with db.cursor(DictCursor) as c:
        # execute()方法中的args参数使用来匹配sql语句中的%s%d等输入信息
        c.execute(sql, args=args)
        # 下面语句是个推导式:
        ret = c.fetchone() if one else c.fetchall()

    return ret
