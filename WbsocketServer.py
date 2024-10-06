import base64
import json
import random
import string
import tornado.ioloop
import tornado.web
import tornado.websocket
import yaml
from flask import Flask
from flask_cors import CORS
import emails
import imaplib
import email
# 邮箱账号信息
import ssl
from datetime import datetime
from email.header import decode_header

from src.api.api import DaliyHotHandler
from src.api.robot import RobotHandler
from src.api.work import WorkListHandler

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

messages = []
emailMessages = []

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

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
            random_str = generate_random_string(20)
            messages.append({"id": random_str, "sender": sender, "message": msg, "sendTime": sendTime, "type": "fs"})
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
                random_str = generate_random_string(20)
                messages.append(
                    {"id": random_str, "sender": sender, "message": msg, "sendTime": sendTime, "type": "yx"})
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



# WebSocket Handler
class MyWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    ping_interval = 30  # 设置心跳间隔（秒）

    # 客户端连接时调用
    def open(self):
        print("New client connected")
        MyWebSocketHandler.clients.add(self)
        MyWebSocketHandler.send_message_to_clients()  # 推送消息到 WebSocket 客户端
        # self.keep_alive()  # 开始心跳

    # 收到消息时调用
    def on_message(self, message):
        print(f"Received message: {message}")
        try:
            data = json.loads(message)
            tp = data.get("type")
            msg_id = data.get("msgId")
            print(f"Received message type: {tp}, msgId: {msg_id}")
            # 处理不同类型的消息
            if tp == "read":
                print(f"Processing read for msgId: {msg_id}")
                # 向特定客户端发送消息
                response_msg = {"msgId": msg_id, "option": "close"}
                self.write_message(json.dumps(response_msg))  # 发送回发送者

                # 如果需要，可以广播消息给所有其他客户端
                for client in MyWebSocketHandler.clients:
                    if client is not self:  # 防止向发送者自己发送
                        client.write_message(json.dumps({"msgId": msg_id, "option": "close"}))
                        print(f"Sent notification to another client: {msg_id}")

        except json.JSONDecodeError:
            print("Failed to decode JSON")
        except Exception as e:
            print(f"An error occurred: {e}")

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
            for message in messages[:]:  # [:] 创建列表的副本
                try:
                    if len(cls.clients) > 0:
                        for client in cls.clients:
                            client.write_message(message)
                            messages.remove(message)
                            # print(f"Sending message to clients: {client},message:{message}")
                except Exception as e:
                    print(f"An error occurred: {e}")

    @classmethod
    def send_emails_to_clients(cls):
        if len(emailMessages) > 0:
            print(f"Sending messages:{emailMessages}")
            for message in emailMessages[:]:  # [:] 创建列表的副本
                try:
                    if len(cls.clients) > 0:
                        for client in cls.clients:
                            client.write_message(message)
                            emailMessages.remove(message)
                            # print(f"Sending message to clients: {client},message:{message}")
                except Exception as e:
                    print(f"An error occurred: {e}")

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


# 创建自定义的 SSL 上下文
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def clean(text):
    # 去掉文件名中的非法字符
    return "".join(c if c.isalnum() else "_" for c in text)


def fetch_emails_simba():
    username = config['simba']['username']
    password = config['simba']['password']
    # 连接到邮箱的IMAP服务器 (Gmail IMAP 服务器为imap.gmail.com)
    imap_server = config['simba']['imap_server']
    fetch_emails(username, password, imap_server)


def fetch_emails_163():
    username = config['wangyi']['username']
    password = config['wangyi']['password']
    # 连接到邮箱的IMAP服务器 (Gmail IMAP 服务器为imap.gmail.com)
    imap_server = config['wangyi']['imap_server']
    fetch_emails(username, password, imap_server)


def fetch_emails(username, password, imap_server):
    # 登录到服务器
    mail = imaplib.IMAP4_SSL(imap_server, ssl_context=ssl_context)
    # mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)

    # 选择收件箱
    mail.select("inbox")

    # 搜索所有邮件 (你也可以使用其他搜索条件)
    status, eMsg = mail.search(None, "UNSEEN")

    # 获取邮件ID列表
    email_ids = eMsg[0].split()
    print("获取邮件", email_ids)
    # 遍历所有邮件
    for mail_id in email_ids:
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # 解析邮件内容
                msg = email.message_from_bytes(response_part[1])
                # 解码邮件标题
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # 如果标题是bytes，需要进行解码
                    subject = subject.decode(encoding if encoding else "utf-8")

                # 解码发件人信息
                from_ = msg.get("From")

                # 获取并解析 "Date" 头字段
                sendTime = ''
                date_tuple = email.utils.parsedate_tz(msg["Date"])
                if date_tuple:
                    local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                    print("发送时间:", local_date.strftime("%Y-%m-%d %H:%M:%S"))
                    sendTime = local_date.strftime("%Y-%m-%d %H:%M:%S")

                print("Subject:", subject)
                print("From:", from_)
                contents = ''

                # 检查邮件是否有多个部分
                if msg.is_multipart():
                    for part in msg.walk():
                        # 如果是文本/HTML邮件内容
                        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                            try:
                                body = part.get_payload(decode=True).decode()
                                # print("Body:", body)
                                contents = body
                            except:
                                pass
                else:
                    # 如果邮件不是multipart，直接获取内容
                    body = msg.get_payload(decode=True).decode()
                    print("Body:", body)
                    contents = body

                random_str = generate_random_string(10)
                emailMessages.append(
                    {"id": random_str, "sender": from_, "message": contents, "sendTime": sendTime, "subject": subject,
                     "type": "email"})
                MyWebSocketHandler.send_emails_to_clients()
                # 关闭与服务器的连接
        # 将邮件标记为已读
        mail.store(mail_id, '+FLAGS', '\\Seen')
    mail.close()
    mail.logout()


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits  # 包含字母和数字
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


# email测试
class EmailHandler(tornado.web.RequestHandler):
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
            random_str = generate_random_string(10)
            emailMessages.append(
                {"id": random_str, "sender": "from_", "message": "contents", "sendTime": "", "subject": "subject",
                 "type": "email"})
            # print(msg, sender, sendTime)
            MyWebSocketHandler.send_emails_to_clients()  # 推送消息到 WebSocket 客户端
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


# email发送周报
class EmailSendHandler(tornado.web.RequestHandler):
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
            print(data)
            emails.send_email(data)
            self.write({"code": 200, "message": "success", "data": ""})  # 返回成功响应
            self.flush()
        except  Exception as e:
            print(f"An error occurred: {e}")
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


# 主应用配置
def make_app():
    return tornado.web.Application([
        (r"/v1/dailyInsight", DaliyHotHandler),  # 处理 HTTP 请求
        (r"/chat", RobotHandler),  # 处理 HTTP 请求
        (r"/v1/fish/msg", FeiShuHandler),  # 处理 HTTP 请求
        (r"/v1/yunxiao/msg", YunXiaoHandler),  # 处理 HTTP 请求
        (r"/ws", MyWebSocketHandler),  # 将 WebSocket 路径与 Handler 绑定
        (r"/v1/email/send", EmailSendHandler),  # 处理 HTTP 请求
        (r"/v1/upload", emails.EmailUploadHandler),  # 处理 HTTP 请求
        (r"/v1/work/(create|update|query|delete|batchFinish|getALLFinish)", WorkListHandler),  # 处理 HTTP 请求

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
