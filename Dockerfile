# 第一阶段：构建应用
FROM python:3.10-slim AS builder

WORKDIR /home/star

# 设置时区环境变量
ENV TZ=Asia/Shanghai

# 安装 tzdata 和其他依赖，并配置时区
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
 # 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 查看已安装的包（可选）
RUN pip freeze

# 复制应用代码
COPY src/ ./src/

# 第二阶段：仅复制依赖包和应用代码
FROM python:3.10-slim

WORKDIR /home/star

# 从 builder 阶段复制所有依赖包
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /home/star /home/star

# 暴露应用运行的端口
EXPOSE 30999

# 设置默认命令
CMD ["python", "-m", "src.main"]
