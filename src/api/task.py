import tornado.web
import json
import pandas as pd
import os
# 上传文件
from src.fileio.FileIo import allowed_file, UPLOAD_FOLDER
from datetime import datetime

from src.mysql.devTask import Task, insert_devTask, getTaskByiteration, getTaskListByiteration


class WorkUploadHandler(tornado.web.RequestHandler):
    # 处理 POST 请求
    def post(self, path):
        # 设置响应头
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
        # data = json.loads(self.request.body)  # 解析 JSON 数据
        if path == "create":
            self.create_work()
        else:
            self.set_status(404)
            self.write({"error": "未知路径"})

    def get(self, path):
        # 设置响应头
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
        if path == "queryTaskCountByIteration":
            self.get_work_by_iteration()
        elif path == "queryTaskListByIteration":
            iteration = self.get_argument("iteration")  # 从 URL 中获取参数
            self.get_taskList_by_iteration(iteration)
        else:
            self.set_status(404)
            self.write({"error": "未知路径"})

    def create_work(self):
        # 读取 JSON 数据
        try:
            if 'file' not in self.request.files or not self.request.files['file']:
                self.write({"code": 400, "message": "No file provided"})
                self.flush()
                return

            file = self.request.files['file'][0]  # 获取上传的文件

            if file.filename == '':
                self.write({"code": 400, "message": "No file selected"})
                self.flush()
                return

            if allowed_file(file.filename):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                with open(file_path, 'wb') as f:
                    f.write(file.body)
                # 读取 Excel 文件
                df = pd.read_excel(file_path)
                # 这里可以根据需要处理数据，例如将其转换为 JSON
                data = df.to_dict(orient='records')
                print(data)
                # 循环遍历每个 JSON 对象
                for record in data:
                    # 处理每个记录
                    subject = record.get("标题")  # 假设你有一个名为 'subject' 的列
                    description = record.get("描述")  # 假设你有一个名为 'description' 的列
                    if pd.isna(description):
                        description = ""  # 或者其他默认值
                    charger = record.get("负责人")
                    if pd.isna(charger):
                        charger = ""  # 或者其他默认值
                    status = record.get("状态")
                    if pd.isna(status):
                        status = ""  # 或者其他默认值
                    project = record.get("所属项目")
                    if pd.isna(project):
                        project = ""  # 或者其他默认值
                    work_type = record.get("工作项类型")
                    if pd.isna(work_type):
                        work_type = ""  # 或者其他默认值
                    follower = record.get("关注者")
                    if pd.isna(follower):
                        follower = ""  # 或者其他默认值
                    iteration = record.get("所属迭代")
                    if pd.isna(iteration):
                        iteration = ""  # 或者其他默认值
                    priority = record.get("优先级")
                    if pd.isna(priority):
                        priority = ""  # 或者其他默认值
                    deadline = record.get("截止日期")
                    if pd.isna(deadline):
                        deadline = ""  # 或者其他默认值
                    work_hours = record.get("预估工时（小时）")
                    plan_start_time = record.get("计划开始日期")
                    if pd.isna(plan_start_time):
                        plan_start_time = ""  # 或者其他默认值
                    plan_end_time = record.get("计划完成日期")
                    if pd.isna(plan_end_time):
                        plan_end_time = ""  # 或者其他默认值
                    product = record.get("所属产品")
                    if pd.isna(product):
                        product = ""  # 或者其他默认值
                    progress = record.get("进度")
                    if pd.isna(progress):
                        progress = ""  # 或者其他默认值
                    functional_module = record.get("所属功能模块")
                    if pd.isna(functional_module):
                        functional_module = ""  # 或者其他默认值
                    create_time = datetime.now()

                    task = Task(subject, description, charger, status, project, work_type, follower, iteration,
                                priority, deadline, work_hours, plan_start_time, plan_end_time, product, progress,
                                functional_module, create_time)
                    insert_devTask(task)

                self.write({"code": 200, "message": "File uploaded successfully"})
            else:
                self.write({"code": 400, "message": "File type not allowed"})
            self.flush()
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"code": 400, "message": "Invalid JSON"})
            self.flush()

    def get_work_by_iteration(self):
        try:
            result = getTaskByiteration()
            self.write({"code": 200, "message": "File uploaded successfully", "data": result})
            self.flush()
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"code": 400, "message": "Invalid JSON"})
            self.flush()

    def get_taskList_by_iteration(self, iteration):
        try:
            result = getTaskListByiteration(iteration)
            self.write({"code": 200, "message": "File uploaded successfully", "data": result})
            self.flush()
        except Exception as e:
            self.set_status(400)
            self.write({"code": 400, "message": {e}})
            self.flush()

    # 处理 OPTIONS 请求（CORS 预检请求）
    def options(self):
        # 设置 CORS 头
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        # 返回状态码 204 表示成功但无内容
        self.set_status(204)
        self.finish()
