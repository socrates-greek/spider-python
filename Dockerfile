FROM python:3.10-slim AS builder
WORKDIR /home/star
RUN pip install  --progress-bar off --debug flask
RUN pip install --progress-bar off  flask-cors
RUN pip install  --progress-bar off --upgrade spark_ai_python
RUN pip install apscheduler -i  https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install websocket-client
# 查看已安装的包
RUN pip freeze
COPY . .
# 第二阶段：仅复制编译后的结果
FROM python:3.10-slim
WORKDIR /home/star
# 从 builder 阶段复制所有依赖包
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /home/star /home/star
# 暴露应用运行的端口
EXPOSE 30999
CMD ["python", "SparkPython.py"]
