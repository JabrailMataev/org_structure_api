import pytest
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_create_department(client):
    response = client.post('/org_structure_app/departments/', {'name': 'IT'})
    assert response.status_code == 201
    assert response.data['name'] == 'IT'