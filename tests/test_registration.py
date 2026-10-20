import allure
import requests

from constants import BASE_URL
from helpers import generate_user_data

class TestRegistration:

    @allure.title("Успешная регистрация пользователя")
    def test_create_user_successful(self, registered_user):
        response = registered_user["response"]
        response_data = registered_user["response_data"]
        user_data = registered_user["data"]
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["user"]["email"] == user_data["email"]

    @allure.title("Регистрация уже существующего пользователя")
    def test_create_duplicate_user(self, registered_user):
        with allure.step("Повторно отправить запрос регистрации"):
            response = requests.post(
                f"{BASE_URL}/api/auth/register",
                json=registered_user["data"],
            )
        assert response.status_code == 403
        assert response.json()["success"] is False

    @allure.title("Регистрация без обязательного поля")
    def test_create_user_without_required_field(self):
        user_data = generate_user_data()
        user_data.pop("name")
        with allure.step("Отправить запрос без имени"):
            response = requests.post(
                f"{BASE_URL}/api/auth/register",
                json=user_data,
            )
        assert response.status_code == 403
        assert response.json()["success"] is False