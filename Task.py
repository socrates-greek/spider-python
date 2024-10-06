import datetime
from datetime import datetime
import requests

from FileIo import read_tou_tiao_hot, write_tou_tiao_hot
from apscheduler.schedulers.blocking import BlockingScheduler


def task1():
    print(f"任务1今日头条热榜: {datetime.now()}")
    # 获取当前日期和时间
    now = datetime.now()
    # 格式化日期为字符串
    date_str = now.strftime("%Y-%m-%d")
    # date_str = "2024-08-07"
    my_map = read_tou_tiao_hot()
    data = tou_tiao_hot_search()
    my_map[date_str] = data
    write_tou_tiao_hot(my_map)


def task2():
    print(f"任务2执行时间: {datetime.now()}")
    # 调用函数接收邮件
    # fetch_emails()


def task3():
    print(f"任务3执行时间: {datetime.now()}")


scheduler = BlockingScheduler()

# 每天14:30执行任务1
scheduler.add_job(task1, 'cron', hour=6, minute=15)
# scheduler.add_job(task1, IntervalTrigger(seconds=30))

# 每周一至周五的9:00执行任务2
# scheduler.add_job(task2, 'cron', day_of_week='mon-fri', hour=9, minute=0)
# scheduler.add_job(task2, 'cron', minute='*')

# 每月1号的12:00执行任务3
scheduler.add_job(task3, 'cron', day=1, hour=12, minute=0)


# 创建一个运行调度器的函数
def run_scheduler():
    try:
        print("定时任务已启动...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

def tou_tiao_hot_search():
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
