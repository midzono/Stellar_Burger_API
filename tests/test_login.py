import allure
import requests

@allure.title("Успешный вход зарегистрированного пользователя")
def test_login_successful(base_url, registered_user):
    response = requests.post(
        f"{base_url}/api/auth/login",
        json={
            "email": registered_user["data"]["email"],
            "password": registered_user["data"]["password"],
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is True
    assert response_data["user"]["email"] == registered_user["data"]["email"]

@allure.title("Вход с неправильными учётными данными")
def test_login_with_wrong_credentials(base_url, registered_user):
    response = requests.post(
        f"{base_url}/api/auth/login",
        json={
            "email": registered_user["data"]["email"],
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401
    assert response.json()["success"] is False