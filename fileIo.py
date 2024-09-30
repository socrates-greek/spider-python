
import json
import os


def read_tou_tiao_hot():
    # 读取 CSV 文件
    file_name = 'data.json'
    # 检查文件是否存在
    if not os.path.isfile(file_name):
        print(f"{file_name} 不存在，正在创建...")
        # 创建一个示例 DataFrame
        my_map_read = {}
        write_tou_tiao_hot(my_map_read)
        print(f"{file_name} 已创建并写入数据。")
        return my_map_read
    else:
        print(f"{file_name} 已存在。")
        # 从 JSON 文件读取数据
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 打印恢复后的数据
        print("从 'data2.json' 读取的数据:")
        print(data)
        # 如果需要解析 JSON 字符串为列表
        # data['2024-08-06'] = json.loads(data['2024-08-06'])
        # print("解析后的数据:")
        # print(data)
        return data


def write_tou_tiao_hot(my_map):
    # 保存字典到 JSON 文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(my_map, f, ensure_ascii=False, indent=4)
    print("字典已保存到 'data2.json'")
