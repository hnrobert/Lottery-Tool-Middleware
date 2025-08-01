# 抽奖系统 Webhook 中间件

一个用于处理金山表单 webhook 并转发到抽奖系统和 Power Automate 的 Python 中间件服务。

## 📁 项目结构

```text
Lottery-Tool-Middleware/
├── src/                    # 源代码目录
│   ├── main.py            # 主应用文件
│   ├── models.py          # 数据模型
│   ├── transformer.py     # 数据转换器
│   ├── webhook_client.py  # HTTP客户端
│   └── tests/             # 测试文件
├── scripts/               # 脚本目录
│   ├── start.sh          # 本地启动脚本
│   └── docker.sh         # Docker部署脚本
├── docker-compose.yml     # 生产环境Docker配置
├── docker-compose.dev.yml # 开发环境Docker配置
├── Dockerfile            # Docker镜像配置
├── nginx.conf           # Nginx配置模板
├── requirements.txt     # Python依赖
├── .env.example        # 环境变量示例
└── README.md           # 项目文档
```

## 功能特性

- 🎯 接收金山表单的 webhook 请求
- 🔄 数据格式转换（金山表单 → 抽奖系统格式）
- 📧 同时转发到抽奖系统和 Power Automate 邮箱
- ⚡ 异步处理，快速响应
- 🛡️ 完整的错误处理和日志记录
- 🧪 包含单元测试
- 🐳 支持 Docker 部署（基于 Alpine Linux）
- 🌐 包含 Nginx 反向代理配置

## 快速开始

📚 **推荐阅读顺序：**

1. 📖 [快速部署指南](QUICK_START.md) - 选择适合的部署方式
2. 📋 [使用指南](USAGE.md) - 了解如何使用和测试
3. 🚀 [部署和运维指南](DEPLOYMENT.md) - 生产环境部署详情

### 最快上手方式

```bash
# 1. 配置环境
cp .env.example .env
# 编辑 .env 文件

# 2. 启动服务（三选一）
./scripts/start.sh --install                    # 本地开发
./scripts/docker.sh --dev                       # Docker 开发
./scripts/docker.sh --prod                      # Docker 生产

# 3. 验证服务
curl http://localhost:8000/health
```

#### 或手动安装和启动

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="$PWD/src:$PYTHONPATH"
python src/main.py

### 方式2: Docker 部署（推荐生产环境）

#### 开发环境

```bash
# 构建并启动开发环境
./scripts/docker.sh --dev

# 查看日志
./scripts/docker.sh --dev --logs

# 停止服务
./scripts/docker.sh --dev --down
```

#### 生产环境

```bash
# 构建并启动生产环境
./scripts/docker.sh --prod

# 查看服务状态
docker-compose ps

# 查看日志
./scripts/docker.sh --logs

# 停止服务
./scripts/docker.sh --down
```

#### 使用 Nginx 反向代理（生产环境）

```bash
# 启动包含 Nginx 的完整生产环境
docker-compose --profile production up -d
```

服务将在以下地址可用：

- 直接访问：`http://localhost:8000`
- 通过 Nginx：`http://localhost:80`

## API 端点

### 健康检查

- `GET /` - 基本健康检查
- `GET /health` - 详细健康状态

### Webhook 处理

- `POST /webhook/jinshan` - 接收金山表单 webhook

### 测试端点

- `POST /test/lottery` - 测试抽奖系统连接

- `POST /test/lottery` - 测试抽奖系统连接

## 数据格式

### 金山表单输入格式

```json
{
  "rid": "8MgaqP3NGp",
  "formId": "20250713140244212536986",
  "formTitle": "2025 宁诺计算机爱好者协会秋季招新网申通道",
  "event": "create_answer",
  "answerContents": [
    {
      "qid": "k9ce0p",
      "type": "input",
      "title": "姓名｜Name",
      "value": "曹宇宸"
    },
    {
      "qid": "br1kvx",
      "type": "numberInput",
      "title": "学号｜Student ID",
      "value": 20808382
    },
    {
      "qid": "30f4xe",
      "type": "email",
      "title": "UNNC邮箱｜UNNC Email",
      "value": "scxyc5@nottingham.edu.cn"
    },
    {
      "qid": "7wpvum",
      "type": "telphone",
      "title": "手机号｜Telephone Number",
      "value": "18740036416"
    }
  ]
}
```

### 抽奖系统输出格式

```json
{
  "lottery_codes": [
    {
      "code": "20808382",
      "participant_info": {
        "name": "曹宇宸",
        "phone": "18740036416",
        "email": "scxyc5@nottingham.edu.cn"
      }
    }
  ]
}
```

## 字段映射

| 金山表单字段 | QID    | 抽奖系统字段 | 描述               |
| ------------ | ------ | ------------ | ------------------ |
| 姓名         | k9ce0p | name         | 参与者姓名         |
| 学号         | br1kvx | code         | 抽奖码（使用学号） |
| 邮箱         | 30f4xe | email        | 联系邮箱           |
| 手机号       | 7wpvum | phone        | 联系电话           |

## 运行测试

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行测试
python -m pytest tests/ -v
```

## 日志记录

服务会在以下位置记录日志：

- 控制台输出
- `middleware.log` 文件

日志级别可通过环境变量 `LOG_LEVEL` 配置。

## 错误处理

- 数据验证失败：返回 400 状态码
- 必要字段缺失：返回 400 状态码，详细说明缺失字段
- 转发失败：记录错误但不影响响应（后台处理）
- 服务器错误：返回 500 状态码

## 安全考虑

- 支持 Bearer Token 认证（抽奖系统）
- CORS 配置
- 请求日志记录
- 输入数据验证

## 部署建议

### 开发环境(dev)

```bash
python main.py
```

### 生产环境(prod)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 监控

建议监控以下指标：

- HTTP 请求成功率
- 响应时间
- 转发成功率
- 错误日志频率

## 故障排除

### 常见问题

1. **端口已被占用**

   ```bash
   # 更改环境变量中的PORT
   PORT=8001 python main.py
   ```

2. **抽奖系统连接失败**

   - 检查`LOTTERY_WEBHOOK_URL`和`LOTTERY_WEBHOOK_TOKEN`
   - 确认网络连通性
   - 查看日志文件

3. **数据转换失败**
   - 检查金山表单字段映射
   - 确认必要字段存在

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request。
