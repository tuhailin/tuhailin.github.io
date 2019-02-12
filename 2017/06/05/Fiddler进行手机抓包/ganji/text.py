import pymysql
from MysqlHelper import MysqlHelper



#在数据库中插入数据
def insertData(db, cursor, data):
    # print(data)
    for d in data:
        # print(d)
        values = list(d)
        sa = values[4].replace('笔', '').replace('万', '')
        if '.' in sa:
            sa = int(sa.replace('.', '')) * 1000
        comm = values[5].replace('万', '')
        if '.' in comm:
            comm = int(comm.replace('.', '')) * 1000
        if int(sa) > 2000:
            sa = int(sa) + 250  #   +400  +250
        else:
            sa = int(sa) + 100  # 100  +50
        if int(comm) > 2000:
            comm = int(comm) + 250
        else:
            comm = int(comm) + 100
        # 插入数据
        sql = "insert into kjds_kd(title,price,brand,sales,comment,region,source,month,goods_type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        try:
            # 执行sql语句
            cursor.execute(sql, (values[1], values[2], values[3], sa, comm, values[6], values[7], '12', values[9]))
            # 提交到数据库执行
            db.commit()

            print("successfully insert data")
        except Exception as e:
            print(e)
            # 发生错误时回滚
            db.rollback()

#显示
def readTable(cursor):
    #选择全部
    cursor.execute("select * from kjds_goods")
    #获得返回值，返回多条记录，若没有结果则返回()
    results = cursor.fetchall()

    #遍历打印
    # for row in results:
    #     if row[8] == '11':
    #         print(row)

    return results

if __name__ == '__main__':

    # 链接mysql数据库
    # db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="goods", charset="utf8")
    db = pymysql.connect(host="111.10.48.226", port=7000, user="root", password="gmall168", database="business", charset="utf8")
    # 创建指针
    cursor = db.cursor()



    #显示表格
    data = readTable(cursor)
    if data:
        # 插入数据
        insertData(db, cursor, data)

    # 关闭游标链接
    cursor.close()
    # 关闭数据库服务器连接，释放内存
    db.close()