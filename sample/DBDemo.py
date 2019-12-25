# coding=utf-8
import pymysql

if __name__ == '__main__':
    conn = pymysql.connect(host="127.0.0.1", user="root", password="jiangying", database="test", charset="utf8")
    cursor = conn.cursor()
    sql = """
        CREATE TABLE quetion (
        id INT auto_increment PRIMARY KEY ,
        title VARCHAR(500) NOT NULL UNIQUE,
        answers VARCHAR(5000)
        )ENGINE=innodb DEFAULT CHARSET=utf8;
    """
    # 执行SQL语句
    cursor.execute(sql)
    # sql1 = """
    #     CREATE TABLE selection (
    #     id INT auto_increment PRIMARY KEY,
    #     quetionId INT,
    #     selection VARCHAR(500)
    #     )ENGINE=innodb DEFAULT CHARSET=utf8;
    # """
    # cursor.execute(sql1)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()