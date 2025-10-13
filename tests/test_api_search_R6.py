# tests/test_api_search.py
import pytest
from flask import Flask
from routes.api_routes import api_bp
import routes.api_routes as api_routes


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(api_bp)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# -------------------------
# Title Search Tests
# -------------------------
def test_search_title_partial(client, monkeypatch):
    """Partial title matches should return correct results."""
    monkeypatch.setattr(api_routes, "search_books_in_catalog",
                        lambda term, typ: [{"title": "Python Basics", "author": "Alice", "isbn": "1234567890123"}]
                        if "python" in term.lower() else [])

    # positive: exact term
    response = client.get("/api/search?q=Python&type=title")
    data = response.get_json()
    assert response.status_code == 200
    assert data['count'] == 1
    assert data['results'][0]['title'] == "Python Basics"

    # positive: case-insensitive
    response = client.get("/api/search?q=python&type=title")
    data = response.get_json()
    assert data['count'] == 1

    # negative: no match
    response = client.get("/api/search?q=Java&type=title")
    data = response.get_json()
    assert data['count'] == 0
    assert data['results'] == []

    # edge: partial match in middle of string
    monkeypatch.setattr(api_routes, "search_books_in_catalog",
                        lambda term, typ: [{"title": "Learn Python Quickly", "author": "Bob", "isbn": "9876543210123"}]
                        if "python" in term.lower() else [])
    response = client.get("/api/search?q=Python&type=title")
    data = response.get_json()
    assert data['count'] == 1
    assert "Python" in data['results'][0]['title']


# -------------------------
# Author Search Tests
# -------------------------
def test_search_author_partial(client, monkeypatch):
    """Partial author matches should return correct results."""
    monkeypatch.setattr(api_routes, "search_books_in_catalog",
                        lambda term, typ: [{"title": "Python Basics", "author": "Alice", "isbn": "1234567890123"}]
                        if "ali" in term.lower() else [])

    # positive: partial name
    response = client.get("/api/search?q=Ali&type=author")
    data = response.get_json()
    assert response.status_code == 200
    assert data['count'] == 1
    assert data['results'][0]['author'] == "Alice"

    # positive: full name
    response = client.get("/api/search?q=Alice&type=author")
    data = response.get_json()
    assert data['count'] == 1

    # negative: no match
    response = client.get("/api/search?q=Bob&type=author")
    data = response.get_json()
    assert data['count'] == 0

    # edge: case-insensitive
    response = client.get("/api/search?q=alice&type=author")
    data = response.get_json()
    assert data['count'] == 1


# -------------------------
# ISBN Search Tests
# -------------------------
def test_search_isbn_exact(client, monkeypatch):
    """Exact ISBN matches should return correct results."""
    monkeypatch.setattr(api_routes, "search_books_in_catalog",
                        lambda term, typ: [{"title": "Python Basics", "author": "Alice", "isbn": "1234567890123"}]
                        if term == "1234567890123" else [])

    # positive: exact ISBN
    response = client.get("/api/search?q=1234567890123&type=isbn")
    data = response.get_json()
    assert response.status_code == 200
    assert data['count'] == 1
    assert data['results'][0]['isbn'] == "1234567890123"

    # negative: wrong ISBN
    response = client.get("/api/search?q=9876543210123&type=isbn")
    data = response.get_json()
    assert data['count'] == 0

    # edge: empty string
    response = client.get("/api/search?q=&type=isbn")
    data = response.get_json()
    assert response.status_code == 400
    assert 'error' in data

    # edge: partial digits (should not match)
    response = client.get("/api/search?q=123&type=isbn")
    data = response.get_json()
    assert data['count'] == 0


# -------------------------
# Empty Query / Error Tests
# -------------------------
def test_search_empty_query(client):
    """Empty search queries should return a 400 error."""
    response = client.get("/api/search?q=&type=title")
    data = response.get_json()
    assert response.status_code == 400
    assert 'error' in data

    response = client.get("/api/search?q=&type=author")
    data = response.get_json()
    assert response.status_code == 400
    assert 'error' in data

    response = client.get("/api/search?q=&type=isbn")
    data = response.get_json()
    assert response.status_code == 400
    assert 'error' in data
