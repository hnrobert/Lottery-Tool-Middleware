import logging
from typing import Any, Dict, Optional

import requests

from models import LotteryWebhookPayload, PowerAutomatePayload

logger = logging.getLogger(__name__)


class WebhookClient:
    """处理对外部webhook的HTTP请求"""

    def __init__(
        self,
        lottery_url: str,
        lottery_token: str,
        power_automate_url: Optional[str] = None,
    ):
        self.lottery_url = lottery_url
        self.lottery_token = lottery_token
        self.power_automate_url = power_automate_url
        self.session = requests.Session()

        # 设置请求头
        self.session.headers.update(
            {"Content-Type": "application/json",
                "User-Agent": "Lottery-Middleware/1.0"}
        )

    async def send_to_lottery_system(
        self, payload: LotteryWebhookPayload
    ) -> Dict[str, Any]:
        """发送数据到抽奖系统"""
        try:
            headers = {
                "Authorization": f"Bearer {self.lottery_token}",
                "Content-Type": "application/json",
            }

            response = self.session.post(
                self.lottery_url, json=[payload.dict()], headers=headers, timeout=30
            )

            response.raise_for_status()

            logger.info(f"成功发送到抽奖系统，状态码: {response.status_code}")
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json() if response.content else {},
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"发送到抽奖系统失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status_code": (
                    getattr(e.response, "status_code", None)
                    if hasattr(e, "response")
                    else None
                ),
            }

    async def send_to_power_automate(
        self, payload: PowerAutomatePayload
    ) -> Dict[str, Any]:
        """发送数据到Power Automate"""
        if not self.power_automate_url:
            logger.warning("Power Automate URL未配置，跳过发送")
            return {"success": False, "error": "Power Automate URL未配置"}

        try:
            response = self.session.post(
                self.power_automate_url, json=payload.dict(), timeout=30
            )

            response.raise_for_status()

            logger.info(f"成功发送到Power Automate，状态码: {response.status_code}")
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.text,
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"发送到Power Automate失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status_code": (
                    getattr(e.response, "status_code", None)
                    if hasattr(e, "response")
                    else None
                ),
            }

    async def send_to_power_automate_simple(
        self, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """发送简化数据到Power Automate（仅包含name和email）"""
        if not self.power_automate_url:
            logger.warning("Power Automate URL未配置，跳过发送")
            return {"success": False, "error": "Power Automate URL未配置"}

        try:
            logger.info(f"发送简化数据到Power Automate: {payload}")
            response = self.session.post(
                self.power_automate_url, json=payload, timeout=30
            )

            response.raise_for_status()

            logger.info(f"成功发送到Power Automate，状态码: {response.status_code}")
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.text,
                "sent_data": payload,
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"发送到Power Automate失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status_code": (
                    getattr(e.response, "status_code", None)
                    if hasattr(e, "response")
                    else None
                ),
                "sent_data": payload,
            }
