# coding=utf-8
import pymysql

if __name__ == '__main__':
    conn = pymysql.connect(host="xxxxxx", user="xxxxx", password="xxxxxx", database="questionnaire", charset="utf8")
    cursor = conn.cursor()
    sql = """
        CREATE TABLE health (
        id INT auto_increment PRIMARY KEY ,
        title VARCHAR(200) NOT NULL UNIQUE,
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