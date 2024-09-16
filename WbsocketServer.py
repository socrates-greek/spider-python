import base64
import json
import threading
from datetime import datetime

import tornado.ioloop
import tornado.web
import tornado.websocket
from flask import Flask
from flask_cors import CORS

import SparkApi
from fileIo import read_tou_tiao_hot

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

ganswer = []
messages = []
answerLen = 0
# 以下密钥信息从控制台获取   https://console.xfyun.cn/services/bm35
appid = "5ad1cf2f"  # 填写控制台中获取的 APPID 信息
api_secret = "5fa688019c7eef19f159b90f68195a15"  # 填写控制台中获取的 APISecret 信息
api_key = "b329304e215f13d57369a0a7f2ffa1a8"  # 填写控制台中获取的 APIKey 信息
domain = "general"  # v3.0版本
Spark_url = 'wss://spark-api.xf-yun.com/v1.1/chat'  # v3.5环服务地址


# HTTP 处理器
class DaliyHotHandler(tornado.web.RequestHandler):
    # 处理 GET 请求
    def get(self):
        result = daily_insight()
        self.write(result)


# HTTP 处理器
class RobotHandler(tornado.web.RequestHandler):
    # 处理 POST 请求
    def post(self):
        # 设置响应头
        self.set_header("Content-Type", "text/event-stream")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")

        # 读取 JSON 数据
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据
            question = data.get("message")  # 获取 "message" 字段

            # 生成器
            print(question)
            question = SparkApi.checklen(SparkApi.getText("user", question))
            SparkApi.answer = ""
            print("星火:", end="")
            thread = threading.Thread(target=SparkApi.main,
                                      args=(appid, api_key, api_secret, Spark_url, domain, question))
            thread.start()

            # SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
            def generate():
                global ganswer
                ganswer = []
                cut = False
                try:
                    while True:
                        if cut:
                            break
                        for item in SparkApi.string_set:
                            if item in ganswer:
                                continue
                            else:
                                if item != 'quit' and len(item) > 0:
                                    ganswer.append(item)
                                    yield f"{item}"
                            if item == 'quit':
                                cut = True
                                break
                    # print('\n'+SparkApi.answer)
                    SparkApi.getText("assistant", SparkApi.answer)
                except GeneratorExit:
                    print("Client closed connection")
                except Exception as e:
                    print(f"An error occurred: {e}")

            # 逐条写入数据
            for item in generate():
                self.write(item)  # 确保遵循 SSE 格式
                self.flush()  # 确保数据被发送

        except json.JSONDecodeError:
            self.set_status(400)  # 设置状态码为 400 表示错误请求
            self.write("data: Invalid JSON\n\n")
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


# 飞书消息
class FeiShuHandler(tornado.web.RequestHandler):
    # 处理请求前进行 Basic 认证
    def prepare(self):
        auth_header = self.request.headers.get("Authorization")
        print(auth_header)
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
    def post(self):
        # 设置响应头
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")

        # 读取 JSON 数据
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据
            msg = data.get("message")  # 获取 "message" 字段
            sender = data.get("sender")  # 获取 "sender" 字段
            sendTime = data.get("sendTime")
            messages.append(data)
            # print(msg, sender, sendTime)
            MyWebSocketHandler.send_message_to_clients()  # 推送消息到 WebSocket 客户端
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

# 云效代码消息
class YunXiaoHandler(tornado.web.RequestHandler):
    # 处理请求前进行 Basic 认证
    def prepare(self):
        auth_header = self.request.headers.get("X-Codeup-Token")
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
    def post(self):
        # 设置响应头
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")

        # 读取 JSON 数据
        try:
            data = json.loads(self.request.body)  # 解析 JSON 数据
            print(data)
            commits = data.get("commits")  # 获取 "sender" 字段
            print(commits)
            for commit in commits:
                author = commit.get("author")  # 获取 "sender" 字段
                sender = author.get("name")  # 获取 "sender" 字段
                msg = commit.get("message")  # 获取 "message" 字段
                sendTime = commit.get("timestamp")
                messages.append({"sender":sender,"message":msg,"sendTime":sendTime})
            MyWebSocketHandler.send_message_to_clients()  # 推送消息到 WebSocket 客户端
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



# 主动买
# @app.route('/chat', methods=['POST'])
# def ask():
#     print(request)
#     data = request.json
#     question = data.get('message')
#     print(question)
#     question = SparkApi.checklen(SparkApi.getText("user", question))
#     SparkApi.answer = ""
#     print("星火:", end="")
#     thread = threading.Thread(target=SparkApi.main, args=(appid, api_key, api_secret, Spark_url, domain, question))
#     thread.start()
#     # SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
#     def generate():
#         global ganswer
#         ganswer = []
#         cut = False
#         try:
#             while True:
#                 if cut:
#                     break
#                 for item in SparkApi.string_set:
#                     if item in ganswer:
#                         continue
#                     else:
#                         if item != 'quit' and len(item) > 0:
#                             ganswer.append(item)
#                             yield f"{item}"
#                     if item == 'quit':
#                         cut = True
#                         break
#             # print('\n'+SparkApi.answer)
#             SparkApi.getText("assistant", SparkApi.answer)
#         except GeneratorExit:
#             print("Client closed connection")
#         except Exception as e:
#             print(f"An error occurred: {e}")
#     return Response(generate(), mimetype='text/event-stream')

# @app.route('/v1/dailyInsight', methods=['GET'])
def daily_insight():
    my_map = read_tou_tiao_hot()
    key, data = find_max_date_element(my_map)
    # 检查请求是否成功
    if len(data) > 0:
        # 解析响应内容
        return {
            "message": "Successfully bought stock",
            "response": data
        }
    else:
        return {
            "message": "Failed",
            "response": "",
        }


# 将日期字符串转换为 datetime 对象，并找到最大日期
def find_max_date_element(data_dict):
    # 解析日期字符串为 datetime 对象
    date_format = '%Y-%m-%d'
    dates = {datetime.strptime(key, date_format): key for key, date_str in data_dict.items()}
    # 找到最大日期
    max_date = max(dates.keys())
    # 获取最大日期对应的字典键
    max_date_key = dates[max_date]
    # 返回最大日期和对应的值
    return max_date_key, data_dict[max_date_key]


# WebSocket Handler
class MyWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    ping_interval = 30  # 设置心跳间隔（秒）

    # 客户端连接时调用
    def open(self):
        print("New client connected")
        MyWebSocketHandler.clients.add(self)
        MyWebSocketHandler.send_message_to_clients()  # 推送消息到 WebSocket 客户端
        self.keep_alive()  # 开始心跳

    # 收到消息时调用
    def on_message(self, message):
        print(f"Received message: {message}")
        # 向所有连接的客户端广播消息
        # for client in MyWebSocketHandler.clients:
        #     if client is not self:  # 防止向发送者自己发送
        #         client.write_message(f"Broadcast: Received")

    # 关闭连接时调用
    def on_close(self):
        print("Client disconnected")
        MyWebSocketHandler.clients.remove(self)

    # 处理跨域请求
    def check_origin(self, origin):
        return True

    # 广播消息给所有连接的客户端
    def broadcast_message(self, message):
        for client in MyWebSocketHandler.clients:
            if client is not self:  # 防止向发送者自己发送
                client.write_message(message)

    # 主动发送消息给所有客户端的方法
    @classmethod
    def send_message_to_clients(cls):
        if len(messages) > 0:
            # print(f"Sending messages:{messages}")
            for message in messages[:]:# [:] 创建列表的副本
                if len(cls.clients)>0:
                    for client in cls.clients:
                        client.write_message(message)
                        messages.remove(message)
                        # print(f"Sending message to clients: {client},message:{message}")

    # 开始心跳机制
    def keep_alive(self):
        # 每30秒发送一次 ping 消息
        self.ping_interval = 30
        tornado.ioloop.IOLoop.current().call_later(self.ping_interval, self.send_ping)

    # 发送 ping 消息
    def send_ping(self):
        if self.ws_connection:  # 确保连接仍然有效
            self.write_message("ping")  # 发送 ping 消息
            self.keep_alive()  # 重新安排下一次 ping


# 主应用配置
def make_app():
    return tornado.web.Application([
        (r"/v1/dailyInsight", DaliyHotHandler),  # 处理 HTTP 请求
        (r"/chat", RobotHandler),  # 处理 HTTP 请求
        (r"/v1/fish/msg", FeiShuHandler),  # 处理 HTTP 请求
        (r"/v1/yunxiao/msg", YunXiaoHandler),  # 处理 HTTP 请求
        (r"/ws", MyWebSocketHandler),  # 将 WebSocket 路径与 Handler 绑定
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # 在 8888 端口启动服务
    print("WebSocket server is running on ws://localhost:8888/ws")

    # 在 5 秒后，主动发送消息给所有客户端
    # def send_periodic_message():
    #     MyWebSocketHandler.send_message_to_clients("Hello from server")
    #
    # tornado.ioloop.PeriodicCallback(send_periodic_message, 5000).start()

    tornado.ioloop.IOLoop.current().start()
