import json

import requests
from apscheduler.triggers.interval import IntervalTrigger

import SparkApi
from flask_cors import CORS
from flask import Flask, request, jsonify, Response
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from fileIo import ReadTouTiaoHot, WriteToutiaoHot

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

ganswer = []
answerLen = 0
# 以下密钥信息从控制台获取   https://console.xfyun.cn/services/bm35
appid = "5ad1cf2f"  # 填写控制台中获取的 APPID 信息
api_secret = "5fa688019c7eef19f159b90f68195a15"  # 填写控制台中获取的 APISecret 信息
api_key = "b329304e215f13d57369a0a7f2ffa1a8"  # 填写控制台中获取的 APIKey 信息

domain = "general"  # v3.0版本

Spark_url = 'wss://spark-api.xf-yun.com/v1.1/chat'  # v3.5环服务地址

# 初始上下文内容，当前可传system、user、assistant 等角色
text = [
    # {"role": "system", "content": "你现在扮演李白，你豪情万丈，狂放不羁；接下来请用李白的口吻和用户对话。"} , # 设置对话背景或者模型角色
    # {"role": "user", "content": "你是谁"},  # 用户的历史问题
    # {"role": "assistant", "content": "....."} , # AI的历史回答结果
    # # ....... 省略的历史对话
    # {"role": "user", "content": "你会做什么"}  # 最新的一条问题，如无需上下文，可只传最新一条问题
]


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


# 主动买
@app.route('/chat', methods=['POST'])
def ask():
    print(request)
    data = request.json
    question = data.get('message')
    print(question)
    question = checklen(getText("user", question))
    SparkApi.answer = ""
    print("星火:", end="")
    thread = threading.Thread(target=SparkApi.main, args=(appid, api_key, api_secret, Spark_url, domain, question))
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
            getText("assistant", SparkApi.answer)
        except GeneratorExit:
            print("Client closed connection")
        except Exception as e:
            print(f"An error occurred: {e}")

    return Response(generate(), mimetype='text/event-stream')

    # return jsonify({
    #     "message": "Successfully bought stock",
    #     "response": SparkApi.answer,
    # }), 200


@app.route('/v1/dailyInsight', methods=['GET'])
def dailyInsight():
    print(request)
    my_map = ReadTouTiaoHot()
    key,data=find_max_date_element(my_map)
    # 检查请求是否成功
    if len(data) > 0:
        # 解析响应内容
        return jsonify({
            "message": "Successfully bought stock",
            "response": data
        }), 200
    else:
        return jsonify({
            "message": "Failed",
            "response": "",
        }), 500

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


def toutiaoHotSearch():
    url = 'https://api.oioweb.cn/api/common/fetchHotSearchBoard?type=toutiao'
    # 发送GET请求
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析响应内容
        data = response.json()
        print('响应数据:', data)
        result = data.get('result')  # 使用 get() 方法以避免 KeyError
        result_str = str(result)
        # 打印转换后的字符串
        print('转换后的 result 字段:', result_str)
        return result_str
    else:
        print('请求失败，状态码:', response.status_code)
        return []


def task1():
    print(f"任务1今日头条热榜: {datetime.now()}")
    # 获取当前日期和时间
    now = datetime.now()
    # 格式化日期为字符串
    date_str = now.strftime("%Y-%m-%d")
    # date_str = "2024-08-07"
    my_map = ReadTouTiaoHot()
    data = toutiaoHotSearch()
    my_map[date_str] = data
    WriteToutiaoHot(my_map)

def task2():
    print(f"任务2执行时间: {datetime.now()}")


def task3():
    print(f"任务3执行时间: {datetime.now()}")


scheduler = BlockingScheduler()

# 每天14:30执行任务1
scheduler.add_job(task1, 'cron', hour=6, minute=0)
# scheduler.add_job(task1, IntervalTrigger(seconds=30))


# 每周一至周五的9:00执行任务2
scheduler.add_job(task2, 'cron', day_of_week='mon-fri', hour=9, minute=0)

# 每月1号的12:00执行任务3
scheduler.add_job(task3, 'cron', day=1, hour=12, minute=0)


# 创建一个运行调度器的函数
def run_scheduler():
    try:
        print("定时任务已启动...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    # 在单独的线程中运行调度器
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # 启动Flask应用
    app.run(host='0.0.0.0', port=30999)

    # while(1):
    #     Input = input("\n" +"我:")
    #     question = checklen(getText("user",Input))
    #     SparkApi.answer =""
    #     print("星火:",end ="")
    #     SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    #     # print(SparkApi.answer)
    #     getText("assistant",SparkApi.answer)
