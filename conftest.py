import allure
import pytest
import requests

from constants import BASE_URL
from helpers import generate_user_data

@pytest.fixture
def registered_user():
    user_data = generate_user_data()
    access_token = None

    try:
        with allure.step("Зарегистрировать тестового пользователя"):
            response = requests.post(
                f"{BASE_URL}/api/auth/register",
                json=user_data,
            )

        response_data = response.json()
        access_token = response_data.get("accessToken")

        yield {
            "data": user_data,
            "access_token": access_token,
            "response": response,
            "response_data": response_data,
        }

    finally:
        if access_token:
            with allure.step("Удалить тестового пользователя"):
                requests.delete(
                    f"{BASE_URL}/api/auth/user",
                    headers={"Authorization": access_token},
                )