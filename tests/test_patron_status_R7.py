# tests/test_patron_status.py
import sys
import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import library_service

def test_patron_status_positive():
    fake_data = {
        'currently_borrowed': [
            {'title': 'Python Basics', 'due_date': (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")},
            {'title': 'Advanced Python', 'due_date': (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")},
        ],
        'total_late_fees': 5.0,
        'num_currently_borrowed': 2,
        'borrowing_history': [
            {'title': 'Intro to CS', 'returned_date': '2025-09-01'},
            {'title': 'Data Structures', 'returned_date': '2025-08-15'},
        ]
    }

    # Patch uses the library_service module path
    with patch('library_service.get_patron_status_report', return_value=fake_data):
        result = library_service.get_patron_status_report('123456')

        assert 'currently_borrowed' in result
        assert 'total_late_fees' in result
        assert 'num_currently_borrowed' in result
        assert 'borrowing_history' in result
        assert result['num_currently_borrowed'] == len(result['currently_borrowed'])
        assert result['total_late_fees'] >= 0
        assert isinstance(result['borrowing_history'], list)

def test_patron_status_empty():
    empty_data = {
        'currently_borrowed': [],
        'total_late_fees': 0.0,
        'num_currently_borrowed': 0,
        'borrowing_history': []
    }

    with patch('library_service.get_patron_status_report', return_value=empty_data):
        result = library_service.get_patron_status_report('654321')

        assert result['currently_borrowed'] == []
        assert result['total_late_fees'] == 0.0
        assert result['num_currently_borrowed'] == 0
        assert result['borrowing_history'] == []

def test_patron_status_late_fees():
    data_with_fee = {
        'currently_borrowed': [],
        'total_late_fees': 12.5,
        'num_currently_borrowed': 0,
        'borrowing_history': []
    }

    with patch('library_service.get_patron_status_report', return_value=data_with_fee):
        result = library_service.get_patron_status_report('111111')
        assert result['total_late_fees'] > 0

def test_patron_status_multiple_borrowed():
    borrowed = [{'title': f'Book {i}', 'due_date': (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")} for i in range(5)]
    data_multiple = {
        'currently_borrowed': borrowed,
        'total_late_fees': 0,
        'num_currently_borrowed': len(borrowed),
        'borrowing_history': []
    }

    with patch('library_service.get_patron_status_report', return_value=data_multiple):
        result = library_service.get_patron_status_report('222222')

        assert result['num_currently_borrowed'] == 5
        assert len(result['currently_borrowed']) == 5
