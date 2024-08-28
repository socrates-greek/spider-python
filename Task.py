import datetime
from datetime import datetime
import requests
from fileIo import ReadTouTiaoHot, WriteToutiaoHot
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