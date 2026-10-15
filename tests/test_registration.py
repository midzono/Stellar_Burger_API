import allure
import requests

@allure.title("Успешное создание уникального пользователя")
def test_create_user_successful(base_url, user_data):
    response = requests.post(
        f"{base_url}/api/auth/register",
        json=user_data,
    )
    assert response.status_code == 200
    response_data = response.json()

    assert response_data["success"] is True
    assert response_data["user"]["email"] == user_data["email"]

    access_token = response_data.get("accessToken")
    if access_token:
        requests.delete(
        f"{base_url}/api/auth/user",
        headers={"Authorization": access_token},
    )

@allure.title("Повторное создание уже зарегистрированного пользователя")
def test_create_duplicate_user(base_url, registered_user):
    response = requests.post(
        f"{base_url}/api/auth/register",
        json=registered_user["data"],
    )
    assert response.status_code == 403
    assert response.json()["success"] is False

@allure.title("Создание пользователя без обязательного поля")
def test_create_user_without_required_field(base_url, user_data):
    user_data.pop("name")
    response = requests.post(
        f"{base_url}/api/auth/register",
        json=user_data,
    )
    assert response.status_code == 403
    assert response.json()["success"] is False