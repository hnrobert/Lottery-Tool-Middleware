import logging
from datetime import datetime
from typing import Any

from models import (JinshanWebhookData, LotteryWebhookPayload, ParticipantInfo,
                    PowerAutomatePayload)

logger = logging.getLogger(__name__)


class DataTransformer:
    """数据转换器，用于将金山表单数据转换为抽奖系统和Power Automate格式"""

    # 字段映射配置
    FIELD_MAPPING = {
        "name": {"qid": "k9ce0p", "title": "姓名｜Name"},
        "student_id": {"qid": "br1kvx", "title": "学号｜Student ID"},
        "gender": {"qid": "wdfqio", "title": "性别 | Gender"},
        "email": {"qid": "30f4xe", "title": "UNNC邮箱｜UNNC Email"},
        "phone": {"qid": "7wpvum", "title": "手机号｜Telephone Number"},
    }

    @staticmethod
    def extract_field_value(answer_contents: list, qid: str) -> Any:
        """根据qid提取字段值"""
        for content in answer_contents:
            if content.get("qid") == qid:
                value = content.get("value")
                # 处理数组值（如性别选择）
                if isinstance(value, list) and len(value) > 0:
                    return value[0]
                return value
        return None

    @classmethod
    def transform_to_lottery_format(
        cls, jinshan_data: JinshanWebhookData
    ) -> LotteryWebhookPayload:
        """将金山表单数据转换为抽奖系统格式"""
        try:
            answer_contents = [
                content.dict() for content in jinshan_data.answerContents
            ]

            # 提取必要字段
            name = cls.extract_field_value(
                answer_contents, cls.FIELD_MAPPING["name"]["qid"]
            )
            student_id = cls.extract_field_value(
                answer_contents, cls.FIELD_MAPPING["student_id"]["qid"]
            )
            phone = cls.extract_field_value(
                answer_contents, cls.FIELD_MAPPING["phone"]["qid"]
            )
            email = cls.extract_field_value(
                answer_contents, cls.FIELD_MAPPING["email"]["qid"]
            )

            # 验证必要字段
            if not all([name, student_id, phone, email]):
                missing_fields = []
                if not name:
                    missing_fields.append("姓名")
                if not student_id:
                    missing_fields.append("学号")
                if not phone:
                    missing_fields.append("手机号")
                if not email:
                    missing_fields.append("邮箱")
                raise ValueError(f"缺少必要字段: {', '.join(missing_fields)}")

            # 转换学号为字符串作为抽奖码
            lottery_code = str(student_id)

            # 构建参与者信息
            participant_info = ParticipantInfo(
                name=str(name), phone=str(phone), email=str(email)
            )

            lottery_payload = LotteryWebhookPayload(
                code=lottery_code, participant_info=participant_info
            )

            logger.info(f"成功转换数据为抽奖格式，学号: {student_id}, 姓名: {name}")
            return lottery_payload

        except Exception as e:
            logger.error(f"转换抽奖格式失败: {str(e)}")
            raise

    @classmethod
    def transform_to_power_automate_format(
        cls, jinshan_data: JinshanWebhookData
    ) -> PowerAutomatePayload:
        """将金山表单数据转换为Power Automate格式"""
        try:
            answer_contents = [
                content.dict() for content in jinshan_data.answerContents
            ]

            # 提取字段
            name = cls.extract_field_value(
                answer_contents, cls.FIELD_MAPPING["name"]["qid"]
            )
            student_id = cls.extract_field_value(
                answer_contents, cls.FIELD_MAPPING["student_id"]["qid"]
            )
            gender = cls.extract_field_value(
                answer_contents, cls.FIELD_MAPPING["gender"]["qid"]
            )
            email = cls.extract_field_value(
                answer_contents, cls.FIELD_MAPPING["email"]["qid"]
            )
            phone = cls.extract_field_value(
                answer_contents, cls.FIELD_MAPPING["phone"]["qid"]
            )

            # 格式化提交时间
            submission_time = datetime.fromtimestamp(
                jinshan_data.eventTs / 1000
            ).isoformat()

            # 构建Power Automate载荷
            power_automate_payload = PowerAutomatePayload(
                name=str(name) if name else "",
                student_id=str(student_id) if student_id else "",
                gender=str(gender) if gender else "",
                email=str(email) if email else "",
                phone=str(phone) if phone else "",
                form_id=jinshan_data.formId,
                submission_time=submission_time,
                raw_data=jinshan_data.dict(),
            )

            logger.info(
                f"成功转换数据为Power Automate格式，学号: {student_id}, 姓名: {name}"
            )
            return power_automate_payload

        except Exception as e:
            logger.error(f"转换Power Automate格式失败: {str(e)}")
            raise
