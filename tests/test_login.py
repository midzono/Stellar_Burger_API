import allure
import requests

from constants import BASE_URL

class TestLogin:

    @allure.title("Успешный вход зарегистрированного пользователя")
    def test_login_successful(self, registered_user):
        user_data = registered_user["data"]
        with allure.step("Отправить запрос на вход"):
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={
                    "email": user_data["email"],
                    "password": user_data["password"],
                },
            )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["success"] is True
        assert response_data["user"]["email"] == user_data["email"]

    @allure.title("Вход с неверным паролем")
    def test_login_with_wrong_password(self, registered_user):
        user_data = registered_user["data"]
        with allure.step("Отправить запрос с неверным паролем"):
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={
                    "email": user_data["email"],
                    "password": "WrongPassword123",
                },
            )
        assert response.status_code == 401
        assert response.json()["success"] is False