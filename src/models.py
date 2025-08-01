from pydantic import BaseModel
from typing import List, Dict, Any, Optional


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


class LotteryCode(BaseModel):
    code: str
    participant_info: ParticipantInfo


class LotteryWebhookPayload(BaseModel):
    lottery_codes: List[LotteryCode]


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
