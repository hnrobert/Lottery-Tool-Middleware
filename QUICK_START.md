# 快速部署指南

## 🚀 部署选项总览

根据你的环境和需求，选择最适合的部署方式：

### 1. 🛠️ 本地开发（推荐用于开发和测试）

```bash
# 快速启动
./scripts/start.sh --install

# 验证服务
curl http://localhost:8000/health
```

**优点：** 快速上手，便于调试
**适用：** 开发、测试、本地演示

### 2. 🐳 Docker 开发环境

```bash
# 启动开发环境（支持热重载）
./scripts/docker.sh --dev

# 查看日志
./scripts/docker.sh --dev --logs

# 重建镜像
./scripts/docker.sh --dev --build
```

**优点：** 环境一致性，支持热重载，基于 Alpine Linux 轻量镜像
**适用：** 团队开发、CI/CD

### 3. 🏭 Docker 生产环境

```bash
# 生产部署
./scripts/docker.sh --prod

# 包含 Nginx 的完整生产环境
docker-compose --profile production up -d
```

**优点：** 生产就绪，包含反向代理，基于 Alpine Linux
**适用：** 生产环境、正式部署

## 🔧 故障排除

### Docker 构建问题

如果遇到磁盘空间不足：

```bash
# 清理 Docker 缓存
docker system prune -a --volumes

# 清理未使用的镜像
docker image prune -a
```

### 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
./scripts/docker.sh --logs

# 重启服务
./scripts/docker.sh --restart

# 停止服务
./scripts/docker.sh --down
```

## ⚡ 快速测试

部署完成后，运行以下命令测试：

```bash
# 健康检查
curl http://localhost:8000/health

# 测试抽奖系统连接
curl -X POST http://localhost:8000/test/lottery \
  -H "Content-Type: application/json" \
  -d '{"code": "TEST123", "name": "测试用户", "phone": "13800138000", "email": "test@example.com"}'
```

## 📋 配置检查清单

- ✅ 复制并编辑 `.env` 文件
- ✅ 配置 `POWER_AUTOMATE_WEBHOOK_URL`（如需要）
- ✅ 验证抽奖系统连接
- ✅ 配置金山表单 webhook URL
- ✅ 设置生产环境 HTTPS（生产部署）

## 🌐 访问地址

| 部署方式    | 访问地址                | 说明       |
| ----------- | ----------------------- | ---------- |
| 本地开发    | <http://localhost:8000> | 直接访问   |
| Docker 开发 | <http://localhost:8000> | 直接访问   |
| Docker 生产 | <http://localhost:8000> | 直接访问   |
| 完整生产    | <http://localhost:80>   | 通过 Nginx |

选择适合你的部署方式，开始使用吧！🎉
