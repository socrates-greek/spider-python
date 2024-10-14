import json

from src.mysql.mysqldb import Database
from datetime import datetime, timedelta

class Reminder:
    def __init__(self, reminder,details,startTime,endTime , create_time):
        self.reminder = reminder
        self.details = details
        self.startTime = startTime
        self.endTime = endTime
        self.create_time = create_time


def insert_reminder(rem):
    conn = Database.get_connection()  # 假设这是你获取数据库连接的方法
    cursor = conn.cursor()
    sql = """INSERT INTO nas.nas_reminder_list 
                 (title, details, start_time ,end_time, create_time) 
                 VALUES (%s, %s, %s, %s, %s)"""

    params = (
        rem.reminder,
        rem.details,
        rem.startTime,
        rem.endTime,
        rem.create_time
    )
    # print(params)
    try:
        cursor.execute(sql, params)
        conn.commit()
        print("备忘列表插入成功")
    except Exception as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # 关闭游标


def getReminderUnExpired():
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("select l.id,l.title,l.details,l.start_time,l.end_time,l.create_time from nas_reminder_list l where l.start_time>=now()", ())
        rows = cursor.fetchall()
        # 获取列名
        column_names = [i[0] for i in cursor.description]
        # 将查询结果转换为字典列表
        results = [dict(zip(column_names, row)) for row in rows]
        print(results)
        json_str = json.dumps(results, default=default_serializer)
        return json_str
    except  Exception as e:
        print(e)
    return None

def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # 转换为字符串
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def delete_reminder(id):
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM  nas_reminder_list where id = %s", (id,))
        conn.commit()
        print("备忘删除成功")
    except Exception as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # 关闭游标




# def getTaskListByiteration(iteration):
#     try:
#         conn = Database.get_connection()
#         cursor = conn.cursor()
#         cursor.execute("select * from nas_task_list l where TRIM(l.iteration)= %s", (iteration,))
#         rows = cursor.fetchall()
#         # 获取列名
#         column_names = [i[0] for i in cursor.description]
#
#         # 将查询结果转换为字典列表，并处理空值
#         # 将查询结果转换为字典列表，并处理空值和日期格式
#         results = [
#             {
#                 col: (value.isoformat() if isinstance(value, datetime) else (value if value is not None else ''))
#                 for col, value in zip(column_names, row)
#             }
#             for row in rows
#         ]
#         # 将查询结果转换为字典列表
#         # results = [dict(zip(column_names, row)) for row in rows]
#         print(results)
#         return results
#     except  Exception as e:
#         print(e)
#     return None
