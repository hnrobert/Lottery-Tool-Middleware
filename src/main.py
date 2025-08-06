import asyncio
import logging
import os
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import JinshanWebhookData
from transformer import DataTransformer
from webhook_client import WebhookClient

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('middleware.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="抽奖系统Webhook中间件",
    description="处理金山表单数据并转发到抽奖系统和Power Automate",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 从环境变量获取配置
LOTTERY_WEBHOOK_URL = os.getenv("LOTTERY_WEBHOOK_URL")
LOTTERY_WEBHOOK_TOKEN = os.getenv("LOTTERY_WEBHOOK_TOKEN")
POWER_AUTOMATE_WEBHOOK_URL = os.getenv("POWER_AUTOMATE_WEBHOOK_URL")

if not LOTTERY_WEBHOOK_URL or not LOTTERY_WEBHOOK_TOKEN:
    raise ValueError("必须配置 LOTTERY_WEBHOOK_URL 和 LOTTERY_WEBHOOK_TOKEN")

# 初始化WebhookClient
webhook_client = WebhookClient(
    lottery_url=LOTTERY_WEBHOOK_URL,
    lottery_token=LOTTERY_WEBHOOK_TOKEN,
    power_automate_url=POWER_AUTOMATE_WEBHOOK_URL
)


async def process_webhooks(lottery_payload, power_automate_payload):
    """后台处理webhook转发"""
    results = {}

    # 并发发送到两个系统
    tasks = [
        webhook_client.send_to_lottery_system(lottery_payload),
        webhook_client.send_to_power_automate(power_automate_payload)
    ]

    try:
        lottery_result, power_automate_result = await asyncio.gather(*tasks, return_exceptions=True)

        results["lottery_system"] = lottery_result if not isinstance(
            lottery_result, Exception) else {"success": False, "error": str(lottery_result)}
        results["power_automate"] = power_automate_result if not isinstance(
            power_automate_result, Exception) else {"success": False, "error": str(power_automate_result)}

        logger.info(f"Webhook转发完成: {results}")

    except Exception as e:
        logger.error(f"批量处理webhook失败: {str(e)}")
        results["error"] = str(e)

    return results


@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "message": "抽奖系统Webhook中间件运行正常",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """详细健康检查"""
    return {
        "status": "healthy",
        "lottery_url_configured": bool(LOTTERY_WEBHOOK_URL),
        "power_automate_url_configured": bool(POWER_AUTOMATE_WEBHOOK_URL),
        "timestamp": logging.Formatter().format(logging.LogRecord(
            name="health", level=logging.INFO, pathname="", lineno=0,
            msg="", args=(), exc_info=None
        ))
    }


@app.post("/webhook/jinshan")
async def handle_jinshan_webhook(
    jinshan_data: JinshanWebhookData,
    background_tasks: BackgroundTasks,
    request: Request
):
    """处理金山表单的webhook请求"""
    try:
        logger.info(
            f"收到金山表单webhook: FormID={jinshan_data.formId}, Event={jinshan_data.event}")

        # 只处理创建答案事件
        if jinshan_data.event != "create_answer":
            logger.info(f"跳过非创建事件: {jinshan_data.event}")
            return JSONResponse(
                status_code=200,
                content={"message": "事件已接收但未处理", "event": jinshan_data.event}
            )

        # 数据转换
        try:
            lottery_payload = DataTransformer.transform_to_lottery_format(
                jinshan_data)
            power_automate_payload = DataTransformer.transform_to_power_automate_format(
                jinshan_data)
        except ValueError as e:
            logger.error(f"数据转换失败: {str(e)}")
            raise HTTPException(status_code=400, detail=f"数据转换失败: {str(e)}")

        # 在后台处理webhook转发
        background_tasks.add_task(
            process_webhooks, lottery_payload, power_automate_payload)

        # 生成绑定码并立即返回
        bind_code = DataTransformer.generate_bind_code()

        return JSONResponse(
            status_code=200,
            content={"bind_code": bind_code}
        )

    except Exception as e:
        logger.error(f"处理webhook失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@app.post("/test/power-automate")
async def test_power_automate_webhook(test_data: Dict[str, Any]):
    """测试Power Automate webhook连接"""
    try:
        simple_payload = {
            "name": test_data.get("name", "测试用户"),
            "email": test_data.get("email", "test@example.com")
        }

        result = await webhook_client.send_to_power_automate_simple(simple_payload)
        return {"test_result": result}

    except Exception as e:
        logger.error(f"测试Power Automate失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"测试失败: {str(e)}")


@app.post("/test/lottery")
async def test_lottery_webhook(test_data: Dict[str, Any]):
    """测试抽奖系统webhook连接"""
    try:
        from models import LotteryWebhookPayload, ParticipantInfo

        # 创建测试数据 - 使用新的单对象格式
        test_lottery_payload = LotteryWebhookPayload(
            code=test_data.get("code", "TEST123"),
            participant_info=ParticipantInfo(
                name=test_data.get("name", "测试用户"),
                phone=test_data.get("phone", "13800138000"),
                email=test_data.get("email", "test@example.com")
            )
        )

        result = await webhook_client.send_to_lottery_system(test_lottery_payload)
        return {"test_result": result}

    except Exception as e:
        logger.error(f"测试抽奖系统失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"测试失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 9732))
    debug = os.getenv("DEBUG", "True").lower() == "true"

    logger.info(f"启动服务器: {host}:{port}, Debug: {debug}")
    uvicorn.run(app, host=host, port=port, reload=debug)
