#!/bin/bash

# 抽奖系统Webhook中间件启动脚本

echo "正在启动抽奖系统Webhook中间件..."

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "项目根目录: $PROJECT_ROOT"

# 检查Python环境
if [ ! -f ".venv/bin/python" ]; then
    echo "错误: 未找到虚拟环境，请先运行 python -m venv .venv"
    exit 1
fi

# 检查环境配置文件
if [ ! -f ".env" ]; then
    echo "警告: 未找到.env文件，正在从示例文件创建..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "已创建.env文件，请编辑配置后重新运行"
        exit 1
    else
        echo "错误: 未找到.env.example文件"
        exit 1
    fi
fi

# 激活虚拟环境
source .venv/bin/activate
echo "已激活Python虚拟环境"

# 安装依赖（如果需要）
if [ "$1" = "--install" ]; then
    echo "正在安装依赖包..."
    pip install -r requirements.txt
fi

# 设置Python路径
export PYTHONPATH="$PROJECT_ROOT/src:$PYTHONPATH"

# 启动服务
echo "正在启动FastAPI服务器..."
echo "服务将在 http://localhost:9732 启动"
python src/main.py
