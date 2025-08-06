# API 接口文档

## 概述

抽奖系统 Webhook 中间件提供以下接口：

## 接口列表

### 1. 健康检查

**GET** `/health`

检查服务健康状态和配置。

**响应示例：**

```json
{
  "status": "healthy",
  "lottery_url_configured": true,
  "power_automate_url_configured": true,
  "timestamp": ""
}
```

### 2. 基础状态

**GET** `/`

获取基本服务信息。

**响应示例：**

```json
{
  "message": "抽奖系统Webhook中间件运行正常",
  "version": "1.0.0",
  "status": "healthy"
}
```

### 3. 金山表单 Webhook 接收

**POST** `/webhook/jinshan`

接收金山表单的 webhook 数据，转换后转发到抽奖系统和 Power Automate。

**请求格式：**

```json
{
  "rid": "表单响应ID",
  "formId": "表单ID",
  "formTitle": "表单标题",
  "aid": "答案ID",
  "eventTs": 1722844800000,
  "messageTs": 1722844800000,
  "creatorId": "创建者ID",
  "creatorName": "创建者姓名",
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
}
```

**成功响应：**

```json
{
  "bind_code": "20250805032323705837"
}
```

**注意事项：**

- 只处理 `event` 为 `"create_answer"` 的事件
- 必须包含所有必要字段：姓名、学号、邮箱、手机号
- qid 必须匹配预定义的字段映射

### 4. 抽奖系统测试

**POST** `/test/lottery`

测试抽奖系统连接状态。

**请求格式：**

```json
{
  "code": "TEST123",
  "name": "测试用户",
  "phone": "13800138000",
  "email": "test@unnc.edu.cn"
}
```

**响应示例：**

```json
{
  "test_result": {
    "success": true,
    "status_code": 200,
    "response": {}
  }
}
```

## 发送到抽奖系统的数据格式

中间件会将金山表单数据转换为以下格式发送到抽奖系统：

```json
{
  "code": "83483923",
  "participant_info": {
    "name": "测试用户",
    "phone": "18021553069",
    "email": "jwui2v67@nottingham.edu.cn"
  }
}
```

**字段说明：**

- `code`: 抽奖码（使用学号）
- `participant_info.name`: 参与者姓名
- `participant_info.phone`: 参与者手机号
- `participant_info.email`: 参与者邮箱

## 发送到 Power Automate 的数据格式

```json
{
  "name": "测试用户",
  "student_id": "83483923",
  "gender": "女",
  "email": "jwui2v67@nottingham.edu.cn",
  "phone": "18021553069",
  "form_id": "20250713140244212536986",
  "submission_time": "2025-08-05T03:23:23.000Z",
  "raw_data": {
    "rid": "...",
    "formId": "...",
    "// 完整的金山表单原始数据"
  }
}
```

## 错误响应

### 400 Bad Request

```json
{
  "detail": "数据转换失败: 缺少必要字段: 姓名, 学号"
}
```

### 500 Internal Server Error

```json
{
  "detail": "处理失败: 连接抽奖系统失败"
}
```

## 环境变量配置

确保配置以下环境变量：

```bash
# 抽奖系统配置
LOTTERY_WEBHOOK_URL=http://localhost:3000/api/webhook/activities/4189b01d72abbf9f381cb207953ba936/lottery-codes
LOTTERY_WEBHOOK_TOKEN=your-auth-token

# Power Automate 配置（可选）
POWER_AUTOMATE_WEBHOOK_URL=https://your-power-automate-webhook-url

# 服务配置
HOST=0.0.0.0
PORT=9732
DEBUG=true
```

## 金山表单字段映射

系统使用以下 qid 映射来提取表单数据：

| 字段   | qid    | 标题                      |
| ------ | ------ | ------------------------- |
| 姓名   | k9ce0p | 姓名｜ Name               |
| 学号   | br1kvx | 学号｜ Student ID         |
| 性别   | wdfqio | 性别 \| Gender            |
| 邮箱   | 30f4xe | UNNC 邮箱｜ UNNC Email    |
| 手机号 | 7wpvum | 手机号｜ Telephone Number |

## 使用示例

### 测试完整流程

```bash
# 1. 健康检查
curl http://localhost:9732/health

# 2. 测试抽奖系统连接
curl -X POST http://localhost:9732/test/lottery \
  -H "Content-Type: application/json" \
  -d '{
    "code": "TEST123",
    "name": "测试用户",
    "phone": "13800138000",
    "email": "test@unnc.edu.cn"
  }'

# 3. 模拟金山表单 webhook
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

## 日志和监控

- 服务日志会记录到 `middleware.log` 文件
- 所有 webhook 处理过程都会记录详细日志
- 可以通过 Docker 查看容器日志：`docker logs lottery-webhook-middleware-dev`
