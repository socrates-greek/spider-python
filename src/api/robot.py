

# 读取 YAML 文件
import json
import threading

import tornado
import yaml

import SparkApi


ganswer = []
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 访问配置项
host = config['host']
port = config['port']
appid = config['spark']['appid']  # 填写控制台中获取的 APPID 信息
api_secret = config['spark']['api_secret']  # 填写控制台中获取的 APISecret 信息
api_key = config['spark']['api_key']  # 填写控制台中获取的 APIKey 信息
domain = config['spark']['domain']  # v3.0版本
Spark_url = config['spark']['spark_url']  # v3.5环服务地址


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