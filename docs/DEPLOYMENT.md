# 部署和运维指南

## 部署方式

### 1. 本地开发部署

适用于开发和测试环境。

```bash
# 1. 克隆项目
git clone <repository-url>
cd Lottery-Tool-Middleware

# 2. 配置环境
cp .env.example .env
# 编辑 .env 文件

# 3. 启动服务
./scripts/start.sh --install
```

### 2. Docker 开发部署

适用于团队开发环境，确保环境一致性。

```bash
# 启动开发环境（支持热重载）
./scripts/docker.sh --dev

# 查看日志
./scripts/docker.sh --dev --logs

# 重建镜像
./scripts/docker.sh --dev --build
```

### 3. Docker 生产部署

推荐的生产环境部署方式。

```bash
# 基础部署
./scripts/docker.sh --prod

# 包含 Nginx 的完整部署
docker-compose --profile production up -d
```

### 4. 云平台部署

#### AWS ECS

```bash
# 构建并推送镜像到 ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t lottery-middleware .
docker tag lottery-middleware:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/lottery-middleware:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/lottery-middleware:latest
```

#### Google Cloud Run

```bash
# 部署到 Cloud Run
gcloud builds submit --tag gcr.io/<project-id>/lottery-middleware
gcloud run deploy --image gcr.io/<project-id>/lottery-middleware --platform managed
```

## 监控和日志

### 1. 日志管理

```bash
# Docker 日志
docker-compose logs -f lottery-middleware

# 本地日志
tail -f middleware.log

# 结构化日志搜索
grep "ERROR" middleware.log
grep "lottery_system.*success.*false" middleware.log
```

### 2. 健康检查

```bash
# 基本健康检查
curl http://localhost:8000/health

# 详细状态检查
curl -s http://localhost:8000/health | jq .
```

### 3. 性能监控

建议监控指标：

- HTTP 请求响应时间
- 请求成功率
- 内存使用率
- CPU 使用率
- 错误日志频率

### 4. Prometheus 监控（可选）

添加 Prometheus 指标收集：

```python
# 在 main.py 中添加
from prometheus_client import Counter, Histogram, generate_latest
import time

REQUEST_COUNT = Counter('webhook_requests_total', 'Total webhook requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('webhook_request_duration_seconds', 'Request latency')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.observe(time.time() - start_time)
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## 故障排除

### 常见问题

#### 1. 服务无法启动

```bash
# 检查端口占用
lsof -i :8000

# 检查环境变量
cat .env

# 检查依赖
pip list | grep fastapi
```

#### 2. Docker 构建失败

```bash
# 清理 Docker 缓存
docker system prune -a

# 检查 Dockerfile 语法
docker build --no-cache -t lottery-middleware .
```

**常见 Docker 构建问题：**

1. **磁盘空间不足**

   ```text
   no space left on device
   ```

   解决方案：清理 Docker 缓存和未使用的镜像

   ```bash
   docker system prune -a --volumes
   docker image prune -a
   ```

2. **网络连接问题**

   ```bash
   # 使用国内镜像源
   docker build --build-arg http_proxy=http://proxy:port --build-arg https_proxy=http://proxy:port .
   ```

3. **依赖安装失败**

   ```bash
   # 更新pip并重试
   docker build --build-arg PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple .
   ```

#### 3. 转发失败

```bash
# 测试网络连通性
curl -v http://localhost:3000/api/webhook/activities/4189b01d72abbf9f381cb207953ba936/lottery-codes

# 检查认证
curl -H "Authorization: Bearer your-token" http://lottery-system/api/test
```

#### 4. 数据转换错误

```bash
# 测试数据转换
curl -X POST http://localhost:8000/webhook/jinshan \
  -H "Content-Type: application/json" \
  -d @test-data.json
```

### 日志分析

#### 错误模式识别

```bash
# 统计错误类型
grep ERROR middleware.log | awk '{print $4}' | sort | uniq -c

# 分析响应时间
grep "处理完成" middleware.log | awk '{print $5}' | sort -n
```

## 安全考虑

### 1. 网络安全

- 使用 HTTPS（生产环境）
- 配置防火墙规则
- 限制 API 访问频率

### 2. 应用安全

- 验证输入数据
- 使用环境变量存储敏感信息
- 定期更新依赖包

### 3. 容器安全

- 使用非 root 用户运行
- 最小化镜像体积
- 定期更新基础镜像

## 扩展和优化

### 1. 性能优化

- 配置连接池
- 启用 HTTP/2
- 使用缓存机制

### 2. 高可用部署

```yaml
# docker-compose.ha.yml
version: "3.8"
services:
  lottery-middleware:
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure

  nginx:
    deploy:
      replicas: 2
```

### 3. 数据持久化

- 配置日志轮转
- 设置数据备份策略
- 监控磁盘使用率
