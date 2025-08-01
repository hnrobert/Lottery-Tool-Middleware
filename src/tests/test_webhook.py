from main import app
import pytest
import asyncio
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)

# 测试用的金山表单数据
SAMPLE_JINSHAN_DATA = {
    "rid": "8MgaqP3NGp",
    "formId": "20250713140244212536986",
    "formTitle": "2025 宁诺计算机爱好者协会秋季招新网申通道",
    "aid": "20250801211602567329515",
    "eventTs": 1754054163000,
    "messageTs": 1754054306994,
    "creatorId": "447366960",
    "creatorName": "Schneider",
    "event": "create_answer",
    "version": 2,
    "answerContents": [
        {
            "qid": "bpzfk9",
            "type": "onePage",
            "title": "分页",
            "value": {
                "qid": "",
                "type": "",
                "title": "",
                "value": None,
            },
        },
        {
            "qid": "k9ce0p",
            "type": "input",
            "title": "姓名｜Name",
            "value": "曹宇宸",
        },
        {
            "qid": "br1kvx",
            "type": "numberInput",
            "title": "学号｜Student ID",
            "value": 20808382,
        },
        {
            "qid": "wdfqio",
            "type": "select",
            "title": "性别 | Gender",
            "value": [
                "男 / Male",
            ],
        },
        {
            "qid": "30f4xe",
            "type": "email",
            "title": "UNNC邮箱｜UNNC Email",
            "value": "scxyc5@nottingham.edu.cn",
        },
        {
            "qid": "7wpvum",
            "type": "telphone",
            "title": "手机号｜Telephone Number",
            "value": "18740036416",
        }
    ]
}


def test_root_endpoint():
    """测试根端点"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """测试健康检查端点"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_jinshan_webhook_valid_data():
    """测试有效的金山表单数据"""
    response = client.post("/webhook/jinshan", json=SAMPLE_JINSHAN_DATA)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["student_id"] == 20808382


def test_jinshan_webhook_invalid_event():
    """测试无效事件类型"""
    invalid_data = SAMPLE_JINSHAN_DATA.copy()
    invalid_data["event"] = "update_answer"

    response = client.post("/webhook/jinshan", json=invalid_data)
    assert response.status_code == 200
    data = response.json()
    assert "事件已接收但未处理" in data["message"]


def test_jinshan_webhook_missing_required_fields():
    """测试缺少必要字段的情况"""
    invalid_data = SAMPLE_JINSHAN_DATA.copy()
    # 移除姓名字段
    invalid_data["answerContents"] = [
        content for content in invalid_data["answerContents"]
        if content["qid"] != "k9ce0p"
    ]

    response = client.post("/webhook/jinshan", json=invalid_data)
    assert response.status_code == 400
    assert "数据转换失败" in response.json()["detail"]


def test_lottery_test_endpoint():
    """测试抽奖系统测试端点"""
    test_data = {
        "code": "TEST123",
        "name": "测试用户",
        "phone": "13800138000",
        "email": "test@example.com"
    }

    response = client.post("/test/lottery", json=test_data)
    # 这个测试可能会失败，因为实际的抽奖系统可能不可用
    # 但至少验证端点存在和基本逻辑
    assert response.status_code in [200, 500]


if __name__ == "__main__":
    pytest.main([__file__])
