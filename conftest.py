import uuid

import pytest
import requests

BASE_URL = "https://stellarburgers.education-services.ru"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def user_data():
    unique_id = uuid.uuid4().hex

    return {
        "email": f"test_{unique_id}@yandex.ru",
        "password": f"Password_{unique_id}",
        "name": f"TestUser_{unique_id}",
    }

@pytest.fixture
def registered_user(base_url, user_data):
    response = requests.post(
        f"{base_url}/api/auth/register",
        json=user_data,
    )

    assert response.status_code == 200, (
        f"Не удалось создать тестового пользователя: "
        f"{response.status_code}, {response.text}"
    )

    response_data = response.json()
    access_token = response_data.get("accessToken")

    yield {
        "data": user_data,
        "access_token": access_token,
        "response": response_data,
    }

    if access_token:
        requests.delete(
            f"{base_url}/api/auth/user",
            headers={"Authorization": access_token},
        )