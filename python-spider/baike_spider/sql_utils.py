class Squtils(object):

    age=0

    def   insertData(self,conn,data):

        cursor = conn.cursor()
        # SQL 查询语句
        isql = "INSERT INTO article( title, detail, nodes) VALUES ('%s', '%s', '%s' )" % ((data['title']), (data['detail_node']), (data['summary_node']))
        try:
            # 执行SQL语句
            cursor.execute(isql)
            conn.commit()
        except  Exception as e:
            print("Error: unable to fecth data")
            print(e.args)
            conn.rollback()

        # 关闭数据库连接

    def dbSelect(self,conn):

        # 使用cursor()方法获取操作游标
        cursor = conn.cursor()
        # SQL 查询语句
        # SQL 查询语句
        sql = "SELECT * FROM ARTICLE "

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                fname = row[0]
                lname = row[1]
                age = row[2]
                sex = row[3]
                # 打印结果
                print ("title=%s,id=%s,detail=%s,nodes=%s" % (fname, lname, age, sex ))
        except:
            print("Error: unable to fecth data")
            conn.rollback()

        # 关闭数据库连接
        # db.close()

    def __init__(self, age=20):
        self.age = age