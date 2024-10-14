import base64
import json
from datetime import datetime

import tornado.web
import tornado.websocket
from src.mysql.mysqldb import  update_work, finish_work, getAll_finish_work
from src.mysql.reminderDb import insert_reminder, getReminderUnExpired, Reminder, delete_reminder


class ReminderListHandler(tornado.web.RequestHandler):
    # 处理请求前进行 Basic 认证
    def prepare(self):
        auth_header = self.request.headers.get("Authorization")
        # print(auth_headerer)
        if auth_header is None or not self.check_auth(auth_header):
            self.set_status(401)
            self.set_header("WWW-Authenticate", 'Basic realm="Protected"')
            self.finish()

    # 校验 Basic 认证信息
    def check_auth(self, auth_header):
        auth_type, credentials = auth_header.split(" ")
        if auth_type.lower() == "basic":
            decoded_credentials = base64.b64decode(credentials).decode("utf-8")
            username, password = decoded_credentials.split(":")
            return username == 'eason' and password == 'Wj*lyp82nlf*'
        return False

    # 处理 POST 请求
    def post(self, path):
        # 设置响应头
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
        data = json.loads(self.request.body)  # 解析 JSON 数据
        if path == "create":
            self.create_reminder(data)
        elif path == "queryUnexpired":
            self.get_reminderUnExpired(data)
        elif path == "delete":
            self.delete_reminder(data)
        elif path == "update":
            self.update_work(data)
        elif path == "batchFinish":
            self.finish_work(data)
        elif path == "getALLFinish":
            self.getall_finish_work(data)
        else:
            self.set_status(404)
            self.write({"error": "未知路径"})

    def get_reminderUnExpired(self, data):
        # 处理用户创建
        # 读取 JSON 数据
        try:
            result = getReminderUnExpired()
            self.write({"code": 200, "message": "success", "data": result})  # 返回成功响应
            self.flush()
        except json.JSONDecodeError as e:
            self.set_status(400)  # 设置状态码为 400 表示错误请求
            self.write({"code": 400, "message": e})
            self.flush()

    def create_reminder(self, data):
        # 处理用户创建
        # 读取 JSON 数据
        try:
            title = data.get("title")  # 获取 "message" 字段
            details = data.get("details")  # 获取 "message" 字段
            startTime = data.get("startTime")  # 获取 "sender" 字段
            endTime = data.get("endTime")  # 获取 "sender" 字段
            remind = Reminder(title,details,startTime,endTime,datetime.now())
            insert_reminder(remind)
            self.write({"code": 200, "message": "success"})  # 返回成功响应
            self.flush()
        except json.JSONDecodeError:
            self.set_status(400)  # 设置状态码为 400 表示错误请求
            self.write({"code": 400, "message": "Invalid JSON"})
            self.flush()

    def update_work(self, data):
        # 处理用户更新
        # 读取 JSON 数据
        try:
            id = data.get("id")  # 获取 "message" 字段
            state = data.get("state")  # 获取 "sender" 字段
            work = data.get("work")  # 获取 "sender" 字段
            print(id, state)
            update_work(id, state, work)
            self.write({"code": 200, "message": "success"})  # 返回成功响应
            self.flush()
        except json.JSONDecodeError:
            self.set_status(400)  # 设置状态码为 400 表示错误请求
            self.write({"code": 400, "message": "Invalid JSON"})
            self.flush()

    def finish_work(self, data):
        # 处理用户更新
        # 读取 JSON 数据
        try:
            ids = data.get("ids")  # 获取 "message" 字段
            new_array = [{"id": id, "state": "1"} for id in ids]
            print(new_array)
            finish_work(new_array)
            self.write({"code": 200, "message": "success"})  # 返回成功响应
            self.flush()
        except json.JSONDecodeError:
            self.set_status(400)  # 设置状态码为 400 表示错误请求
            self.write({"code": 400, "message": "Invalid JSON"})
            self.flush()

    def getall_finish_work(self, data):
        # 处理用户更新
        # 读取 JSON 数据
        try:
            # ids = data.get("ids")  # 获取 "message" 字段
            # new_array = [{"id": id, "state": "1"} for id in ids]
            # print(new_array)
            result = getAll_finish_work("1")
            self.write({"code": 200, "message": "success", "data": result})  # 返回成功响应
            self.flush()
        except json.JSONDecodeError:
            self.set_status(400)  # 设置状态码为 400 表示错误请求
            self.write({"code": 400, "message": "Invalid JSON"})
            self.flush()

    def delete_reminder(self, data):
        # 处理用户更新
        # 读取 JSON 数据
        try:
            id = data.get("id")  # 获取 "message" 字段
            print(id)
            delete_reminder(id)
            self.write({"code": 200, "message": "success"})  # 返回成功响应
            self.flush()
        except json.JSONDecodeError:
            self.set_status(400)  # 设置状态码为 400 表示错误请求
            self.write({"code": 400, "message": "Invalid JSON"})
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
