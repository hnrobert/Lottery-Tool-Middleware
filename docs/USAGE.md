# 使用指南

## 🔧 配置步骤

### 1. 环境变量配置

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
nano .env  # 或使用你喜欢的编辑器
```

**必需配置：**

```bash
# 抽奖系统配置（必填）
LOTTERY_WEBHOOK_URL=http://your-lottery-system/api/webhook/activities/xxx/lottery-codes
LOTTERY_WEBHOOK_TOKEN=your-auth-token

# 服务配置
HOST=0.0.0.0
PORT=9732
DEBUG=true
```

**可选配置：**

```bash
# Power Automate 邮箱通知（可选）
POWER_AUTOMATE_WEBHOOK_URL=https://prod-xx.logic.azure.com/workflows/xxx/triggers/manual/paths/invoke?xxx
```

### 2. 金山表单配置

在金山表单的 webhook 设置中配置：

```url
http://your-server:9732/webhook/jinshan
```

## 🧪 测试验证

### 基本测试

```bash
# 1. 健康检查
curl http://localhost:9732/health

# 2. 测试抽奖系统连接
curl -X POST http://localhost:9732/test/lottery \
  -H "Content-Type: application/json" \
  -d '{"code": "TEST123", "name": "测试用户", "phone": "13800138000", "email": "test@unnc.edu.cn"}'

# 3. 测试 Power Automate 连接
curl -X POST http://localhost:9732/test/power-automate \
  -H "Content-Type: application/json" \
  -d '{"name": "测试用户", "email": "test@example.com"}'
```

### 完整 Webhook 测试

模拟金山表单发送完整的 webhook 数据：

```bash
curl -X POST http://localhost:9732/webhook/jinshan \
  -H "Content-Type: application/json" \
  -d '{
    "rid": "test_rid_001",
    "formId": "test_form_123",
    "formTitle": "测试抽奖报名表",
    "aid": "test_answer_456",
    "eventTs": 1722844800000,
    "messageTs": 1722844800000,
    "creatorId": "test_creator",
    "creatorName": "测试创建者",
    "event": "create_answer",
    "version": 1,
    "answerContents": [
      {
        "qid": "k9ce0p",
        "type": "text",
        "title": "姓名｜Name",
        "value": "张三"
      },
      {
        "qid": "br1kvx",
        "type": "text",
        "title": "学号｜Student ID",
        "value": "2023001"
      },
      {
        "qid": "wdfqio",
        "type": "text",
        "title": "性别 | Gender",
        "value": "男"
      },
      {
        "qid": "30f4xe",
        "type": "email",
        "title": "UNNC邮箱｜UNNC Email",
        "value": "zhangsan@unnc.edu.cn"
      },
      {
        "qid": "7wpvum",
        "type": "phone",
        "title": "手机号｜Telephone Number",
        "value": "13800138000"
      }
    ]
  }'
```

**期望响应：**

```json
{ "bind_code": "20250805032323705837" }
```

## 📋 日志监控

### 查看日志

```bash
# 本地日志
tail -f middleware.log

# Docker日志
docker logs lottery-webhook-middleware-dev -f

# 查看最近的转发记录
docker logs lottery-webhook-middleware-dev --tail 20 | grep "转发完成"
```

### 日志说明

- `收到金山表单webhook`: 接收到数据
- `成功转换数据为抽奖格式`: 数据转换成功
- `成功发送到抽奖系统/Power Automate`: 转发成功
- `Webhook转发完成`: 后台处理完成

## ⚠️ 故障排除

### 常见问题

#### 1. 服务无法启动

```bash
# 检查端口占用
lsof -i :9732

# 检查环境变量
cat .env

# 检查Python环境
python --version && pip list | grep fastapi
```

#### 2. 数据转换失败

**错误**: `缺少必要字段: 姓名, 学号`

**解决**: 检查金山表单的 qid 映射是否正确：

- 姓名: `k9ce0p`
- 学号: `br1kvx`
- 邮箱: `30f4xe`
- 手机号: `7wpvum`

#### 3. 抽奖系统连接失败

**错误**: `Connection refused`

**解决**: 检查抽奖系统是否运行，URL 和 Token 是否正确

#### 4. Power Automate 连接失败

**错误**: `Invalid URL`

**解决**: 检查 Power Automate URL 格式，确保包含完整的查询参数

### 环境检查清单

- ✅ `.env`文件已配置
- ✅ 必需的环境变量已设置
- ✅ 端口 9732 未被占用
- ✅ 抽奖系统可访问
- ✅ Power Automate URL 有效（如果使用）
- ✅ 金山表单 webhook URL 配置正确
