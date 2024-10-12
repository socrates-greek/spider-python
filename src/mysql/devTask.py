from src.mysql.mysqldb import Database
from datetime import datetime, timedelta

class Task:
    def __init__(self, subject, description, charger, status, project, work_type, follower, iteration, priority,
                 deadline, work_hours, plan_start_time, plan_end_time,
                 product, progress, functional_module, create_time):
        self.subject = subject
        self.description = description
        self.charger = charger
        self.status = status
        self.project = project
        self.work_type = work_type
        self.follower = follower
        self.iteration = iteration
        self.priority = priority
        self.deadline = deadline
        self.work_hours = work_hours
        self.plan_start_time = plan_start_time
        self.plan_end_time = plan_end_time
        self.product = product
        self.progress = progress
        self.functional_module = functional_module
        self.create_time = create_time


def insert_devTask(task):
    conn = Database.get_connection()  # 假设这是你获取数据库连接的方法
    cursor = conn.cursor()

    sql = """INSERT INTO nas.nas_task_list 
                 (subject, description, charger, status, project, work_type, 
                  follower, iteration, priority, deadline, work_hours, 
                  plan_start_time, plan_end_time, product, progress, 
                  functional_module, create_time) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                         %s, %s, %s, %s, %s, %s, %s)"""

    params = (
        task.subject, task.description, task.charger, task.status, task.project,
        task.work_type, task.follower, task.iteration, task.priority, task.deadline,
        task.work_hours, task.plan_start_time, task.plan_end_time,
        task.product, task.progress, task.functional_module,
        task.create_time
    )
    print(params)
    try:
        cursor.execute(sql, params)
        conn.commit()
        print("工作列表插入成功")
    except Exception as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # 关闭游标


def getTaskByiteration():
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("select l.iteration,count(*) as taskNum, sum(l.work_hours) as countHour from nas_task_list l  "
                       "group by l.iteration", ())
        rows = cursor.fetchall()
        # 获取列名
        column_names = [i[0] for i in cursor.description]
        # 将查询结果转换为字典列表
        results = [dict(zip(column_names, row)) for row in rows]
        print(results)
        return results
    except  Exception as e:
        print(e)
    return None


def getTaskListByiteration(iteration):
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("select * from nas_task_list l where TRIM(l.iteration)= %s", (iteration,))
        rows = cursor.fetchall()
        # 获取列名
        column_names = [i[0] for i in cursor.description]

        # 将查询结果转换为字典列表，并处理空值
        # 将查询结果转换为字典列表，并处理空值和日期格式
        results = [
            {
                col: (value.isoformat() if isinstance(value, datetime) else (value if value is not None else ''))
                for col, value in zip(column_names, row)
            }
            for row in rows
        ]
        # 将查询结果转换为字典列表
        # results = [dict(zip(column_names, row)) for row in rows]
        print(results)
        return results
    except  Exception as e:
        print(e)
    return None
