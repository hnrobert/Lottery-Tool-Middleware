from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AnswerContent(BaseModel):
    qid: str
    type: str
    title: str
    value: Any


class JinshanWebhookData(BaseModel):
    rid: str
    formId: str
    formTitle: str
    aid: str
    eventTs: int
    messageTs: int
    creatorId: str
    creatorName: str
    event: str
    version: int
    answerContents: List[AnswerContent]


class ParticipantInfo(BaseModel):
    name: str
    phone: str
    email: str


class LotteryWebhookPayload(BaseModel):
    code: str
    participant_info: ParticipantInfo


class PowerAutomatePayload(BaseModel):
    """Power Automate 邮箱数据格式"""

    name: str
    student_id: str
    gender: str
    email: str
    phone: str
    form_id: str
    submission_time: str
    raw_data: Dict[str, Any]
