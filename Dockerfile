FROM python:3.11-alpine

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 安装系统依赖
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    && rm -rf /var/cache/apk/*

# 复制requirements文件并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY src/ ./src/
COPY .env.example .env.example

# 创建非root用户
RUN adduser -D -s /bin/sh app \
    && chown -R app:app /app
USER app

# 暴露端口
EXPOSE 9732

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:9732/health')"

# 设置Python路径
ENV PYTHONPATH=/app/src

# 启动命令
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "9732"]
