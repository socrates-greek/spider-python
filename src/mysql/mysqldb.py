import json
from collections import defaultdict
from datetime import datetime, timedelta

import mysql.connector
from mysql.connector import Error


class Database:
    _connection = None

    @classmethod
    def connect(cls, host, user, password, database):
        if cls._connection is None:
            try:
                cls._connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )
                print("数据库连接成功")
            except Error as e:
                print(f"连接失败: {e}")

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            raise Exception("数据库未连接，请先调用 connect() 方法")
        return cls._connection


def create_table():
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT NOT NULL
        )
    """)
    conn.commit()
    print("表创建成功")


def insert_work(work, state):
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO nas_work_list (work, state,create_time) VALUES (%s, %s,%s)",
                   (work, state, datetime.now()))
    conn.commit()
    print("工作列表插入成功")


def update_work(id, state, work):
    conn = Database.get_connection()
    cursor = conn.cursor()
    updateTime = datetime.now()
    cursor.execute("UPDATE nas_work_list SET state=%s, work=%s ,update_time=%s  where id = %s",
                   (state, work, updateTime, id))
    conn.commit()
    print("工作列表修改成功")


def finish_work(updates):
    conn = Database.get_connection()
    cursor = conn.cursor()
    # 假设要更新的数据列表，每个元素是一个元组 (state, work, id)
    # 获取当前时间
    updateTime = datetime.now()
    # 批量更新
    sql = "UPDATE nas_work_list SET state=%s, update_time=%s WHERE id=%s"
    params = [(item['state'], updateTime, item['id']) for item in updates]  # 创建参数列表
    cursor.executemany(sql, params)  # 批量执行更新
    # 提交更改
    conn.commit()
    print("工作列表批量修改成功")


def getAll_finish_work(state):
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nas_work_list  WHERE state = %s", (state,))
        rows = cursor.fetchall()
        # 获取列名
        column_names = [i[0] for i in cursor.description]
        # 将查询结果转换为字典列表
        results = [dict(zip(column_names, row)) for row in rows]
        # 转换 datetime 对象为字符串
        for item in results:
            if item['create_time'] is not None:
                item['create_time'] = item['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            else:
                item['create_time'] = ""
            if item['update_time'] is not None:
                item['update_time'] = item['update_time'].strftime("%Y-%m-%d %H:%M:%S")
            else:
                item['update_time'] = ""

        # print(results)
        # 创建一个字典以分组数据
        grouped_data = defaultdict(list)
        # 遍历数据，根据 create_time 进行分组
        for item in results:
            create_time = datetime.strptime(item['create_time'], "%Y-%m-%d %H:%M:%S")
            year, week, _ = create_time.isocalendar()  # 获取年份和周数
            key = f"{year}-{week}"  # 使用 f-string 创建键
            grouped_data[(key)].append(item)

        # print(grouped_data)
        # 打印分组后的数据
        # for key, items in grouped_data.items():
        #     print(f"日期: {key}, 工作项: {items}")

        # 转换为 JSON 格式
        json_result = json.dumps(grouped_data, ensure_ascii=False)
        return json_result
    except  Exception as e:
        print(e)
    return None


def delete_work(id):
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM  nas_work_list where id = %s", (id,))
    conn.commit()
    print("工作列表修改成功")


def fetch_work(state):
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nas_work_list  WHERE state = %s", (state,))
        rows = cursor.fetchall()
        # 获取列名
        column_names = [i[0] for i in cursor.description]
        # 将查询结果转换为字典列表
        results = [dict(zip(column_names, row)) for row in rows]
        # 转换 datetime 对象为字符串
        for item in results:
            if item['create_time'] is not None:
                item['create_time'] = item['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            else:
                item['create_time'] = ""
            if item['update_time'] is not None:
                item['update_time'] = item['update_time'].strftime("%Y-%m-%d %H:%M:%S")
            else:
                item['update_time'] = ""
        # 转换为 JSON 格式
        json_result = json.dumps(results, ensure_ascii=False)
        return json_result
    except  Exception as e:
        print(e)
    return None


# 主程序
if __name__ == "__main__":
    Database.connect("localhost", "your_username", "your_password", "your_database")
    create_table()
    insert_user("Alice", 30)
    insert_user("Bob", 25)
    fetch_users()
