# 抽奖系统 Webhook 中间件使用指南

## 快速启动

### 方式 1: 本地启动

1. **配置环境变量**

   ```bash
   cp .env.example .env
   # 编辑 .env 文件，配置 Power Automate URL
   ```

2. **启动服务**

   ```bash
   # 使用脚本启动（推荐）
   ./scripts/start.sh

   # 或手动启动
   source .venv/bin/activate
   export PYTHONPATH="$PWD/src:$PYTHONPATH"
   python src/main.py
   ```

### 方式 2: Docker 启动

```bash
# 开发环境
./scripts/docker.sh --dev

# 生产环境
./scripts/docker.sh --prod
```

### 3. **验证服务**

访问 <http://localhost:8000> 查看服务状态

## 金山表单 Webhook 配置

在金山表单中配置 webhook URL：

```text
http://your-server:8000/webhook/jinshan
```

## 测试

### 基本测试

```bash
# 健康检查
curl http://localhost:8000/health

# 测试抽奖系统连接
curl -X POST http://localhost:8000/test/lottery \
  -H "Content-Type: application/json" \
  -d '{"code": "TEST123", "name": "测试用户", "phone": "13800138000", "email": "test@example.com"}'
```

### Webhook 测试

使用 curl 测试完整的 webhook 流程：

```bash
curl -X POST http://localhost:8000/webhook/jinshan \
  -H "Content-Type: application/json" \
  -d '{
    "rid": "test123",
    "formId": "20250713140244212536986",
    "formTitle": "测试表单",
    "aid": "test_aid",
    "eventTs": 1754054163000,
    "messageTs": 1754054306994,
    "creatorId": "447366960",
    "creatorName": "Test User",
    "event": "create_answer",
    "version": 2,
    "answerContents": [
      {
        "qid": "k9ce0p",
        "type": "input",
        "title": "姓名｜Name",
        "value": "测试用户"
      },
      {
        "qid": "br1kvx",
        "type": "numberInput",
        "title": "学号｜Student ID",
        "value": 12345678
      },
      {
        "qid": "30f4xe",
        "type": "email",
        "title": "UNNC邮箱｜UNNC Email",
        "value": "test@nottingham.edu.cn"
      },
      {
        "qid": "7wpvum",
        "type": "telphone",
        "title": "手机号｜Telephone Number",
        "value": "13800138000"
      }
    ]
  }'
```

## 日志查看

服务运行时会在控制台和 `middleware.log` 文件中记录日志。

## 故障排除

1. **端口占用**：修改 `.env` 中的 `PORT` 配置
2. **权限问题**：确保脚本有执行权限 `chmod +x start.sh`
3. **依赖问题**：运行 `./start.sh --install` 重新安装依赖
