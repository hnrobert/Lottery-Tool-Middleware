# 快速部署指南

选择最适合你的部署方式，3 种选项任选其一：

## 🚀 部署选项对比

| 部署方式       | 启动时间 | 适用场景   | 优势               |
| -------------- | -------- | ---------- | ------------------ |
| 🛠️ 本地开发    | 30 秒    | 开发、调试 | 快速启动，便于调试 |
| 🐳 Docker 开发 | 1 分钟   | 团队开发   | 环境一致，热重载   |
| 🏭 Docker 生产 | 2 分钟   | 生产部署   | 生产就绪，包含代理 |

## 🛠️ 方式 1：本地开发（推荐新手）

**一行命令启动：**

```bash
./scripts/start.sh --install
```

**手动启动：**

```bash
# 1. 创建虚拟环境
python -m venv .venv && source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
export PYTHONPATH="$PWD/src:$PYTHONPATH"
python src/main.py
```

✅ **验证：** `curl http://localhost:9732/health`

## 🐳 方式 2：Docker 开发（推荐团队）

```bash
# 启动开发环境（支持代码热重载）
./scripts/docker.sh --dev

# 查看实时日志
./scripts/docker.sh --dev --logs

# 重建镜像（代码变更后）
./scripts/docker.sh --dev --build
```

**特性：**

- ✅ 代码热重载
- ✅ 环境一致性
- ✅ Alpine Linux 轻量镜像

## 🏭 方式 3：Docker 生产（推荐部署）

```bash
# 启动生产环境
./scripts/docker.sh --prod

# 或启动完整生产环境（包含Nginx）
docker-compose --profile production up -d
```

**生产特性：**

- ✅ Nginx 反向代理
- ✅ 优化的容器配置
- ✅ 生产级日志记录

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
- ✅ 配置 `BIND_CODE` 环境变量（必需）
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
