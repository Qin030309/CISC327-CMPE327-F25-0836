import pytest
from flask import Flask, jsonify, Blueprint

# 假设 api_bp 在 routes.api_routes 中定义
from routes.api_routes import api_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# --------------------------
# R5: Late Fee Calculation
# --------------------------

# Helper to simulate API response
def mock_late_fee(days_overdue, fee_amount, status="success"):
    return {"days_overdue": days_overdue, "fee_amount": fee_amount, "status": status}

def test_late_fee_not_implemented(client, monkeypatch):
    # 未实现功能返回 501
    monkeypatch.setattr(
        "routes.api_routes.calculate_late_fee_for_book",
        lambda pid, bid: {"days_overdue": 0, "fee_amount": 0.0, "status": "Late fee calculation not implemented"}
    )

    response = client.get("/api/late_fee/123456/1")
    assert response.status_code == 501
    data = response.get_json()
    assert data["status"] == "Late fee calculation not implemented"

def test_late_fee_on_time(client, monkeypatch):
    monkeypatch.setattr(
        "routes.api_routes.calculate_late_fee_for_book",
        lambda pid, bid: mock_late_fee(0, 0.0)
    )

    response = client.get("/api/late_fee/123456/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"days_overdue": 0, "fee_amount": 0.0, "status": "success"}

def test_late_fee_overdue_less_than_7(client, monkeypatch):
    monkeypatch.setattr(
        "routes.api_routes.calculate_late_fee_for_book",
        lambda pid, bid: mock_late_fee(5, 2.5)
    )

    response = client.get("/api/late_fee/123456/2")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"days_overdue": 5, "fee_amount": 2.5, "status": "success"}

def test_late_fee_overdue_more_than_7(client, monkeypatch):
    monkeypatch.setattr(
        "routes.api_routes.calculate_late_fee_for_book",
        lambda pid, bid: mock_late_fee(10, 8.0)
    )

    response = client.get("/api/late_fee/123456/3")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"days_overdue": 10, "fee_amount": 8.0, "status": "success"}

def test_late_fee_overdue_max_fee(client, monkeypatch):
    monkeypatch.setattr(
        "routes.api_routes.calculate_late_fee_for_book",
        lambda pid, bid: mock_late_fee(30, 15.0)
    )

    response = client.get("/api/late_fee/123456/4")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"days_overdue": 30, "fee_amount": 15.0, "status": "success"}
