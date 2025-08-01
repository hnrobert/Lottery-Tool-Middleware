#!/bin/bash

# Docker启动脚本

set -e

echo "🚀 抽奖系统Webhook中间件 Docker 部署"

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# 检查环境配置文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env文件，正在从示例文件创建..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ 已创建.env文件，请编辑配置后重新运行"
        echo "📝 请编辑 .env 文件中的以下配置："
        echo "   - POWER_AUTOMATE_WEBHOOK_URL"
        exit 1
    else
        echo "❌ 错误: 未找到.env.example文件"
        exit 1
    fi
fi

# 解析命令行参数
MODE="production"
ACTION="up"

while [[ $# -gt 0 ]]; do
    case $1 in
        --dev)
            MODE="development"
            shift
            ;;
        --prod)
            MODE="production"
            shift
            ;;
        --build)
            ACTION="build"
            shift
            ;;
        --down)
            ACTION="down"
            shift
            ;;
        --logs)
            ACTION="logs"
            shift
            ;;
        --restart)
            ACTION="restart"
            shift
            ;;
        *)
            echo "未知参数: $1"
            echo "用法: $0 [--dev|--prod] [--build|--down|--logs|--restart]"
            exit 1
            ;;
    esac
done

# 选择compose文件
COMPOSE_FILE="docker-compose.yml"
if [ "$MODE" = "development" ]; then
    COMPOSE_FILE="docker-compose.dev.yml"
    echo "🔧 使用开发模式"
else
    echo "🏭 使用生产模式"
fi

# 执行操作
case $ACTION in
    "build")
        echo "🔨 构建Docker镜像（Alpine Linux）..."
        docker-compose -f "$COMPOSE_FILE" build
        ;;
    "up")
        echo "▶️  启动服务（Alpine Linux）..."
        docker-compose -f "$COMPOSE_FILE" up -d
        echo "✅ 服务已启动"
        echo "🌐 访问地址: http://localhost:9732"
        echo "📊 健康检查: http://localhost:9732/health"
        ;;
    "down")
        echo "⏹️  停止服务..."
        docker-compose -f "$COMPOSE_FILE" down
        echo "✅ 服务已停止"
        ;;
    "logs")
        echo "📋 查看日志..."
        docker-compose -f "$COMPOSE_FILE" logs -f
        ;;
    "restart")
        echo "🔄 重启服务..."
        docker-compose -f "$COMPOSE_FILE" restart
        echo "✅ 服务已重启"
        ;;
esac

# 显示运行状态
if [ "$ACTION" = "up" ] || [ "$ACTION" = "restart" ]; then
    echo ""
    echo "📋 服务状态："
    docker-compose -f "$COMPOSE_FILE" ps
fi
