import io
import json
import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'Intent' in res.data


def test_analyze_mock(client):
    payload = {'data': 'We are seeing increased churn and loss of revenue.'}
    res = client.post('/analyze', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert 'status' in data or 'risk_level' in data


def test_upload_csv(client):
    csv_content = 'date,value\n2020-01,100\n2020-02,110\n2020-03,120\n'
    data = {
        'file': (io.BytesIO(csv_content.encode('utf-8')), 'sample.csv')
    }
    res = client.post('/upload', data=data, content_type='multipart/form-data')
    assert res.status_code == 200
    d = res.get_json()
    assert d['status'] == 'success'
    assert isinstance(d['values'], list) and len(d['values']) == 3


def test_export_pdf(client):
    payload = {
        'summary': 'Test summary',
        'risk': 'Medium',
        'predictions': [{'metric': 'M', 'trend': '+1%', 'status': 'OK'}],
        'recommendations': ['Do X'],
        'chart': None
    }
    res = client.post('/export', json=payload)
    assert res.status_code == 200
    assert res.content_type == 'application/pdf'
    assert len(res.data) > 100
