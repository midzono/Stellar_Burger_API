import allure
import requests

@allure.title("Создание заказа авторизованным пользователем")
def test_create_order_authorized(base_url, registered_user):
    response = requests.get(f"{base_url}/api/ingredients")
    ingredients = response.json()["data"]
    ingredient_ids = [ingredients[0]["_id"]]
    response = requests.post(
        f"{base_url}/api/orders",
        json={"ingredients": ingredient_ids},
        headers={
            "Authorization": registered_user["access_token"],
        },
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

@allure.title("Создание заказа без авторизации")
def test_create_order_unauthorized(base_url):
    response = requests.get(f"{base_url}/api/ingredients")
    ingredients = response.json()["data"]
    ingredient_ids = [ingredients[0]["_id"]]
    response = requests.post(
        f"{base_url}/api/orders",
        json={"ingredients": ingredient_ids},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

@allure.title("Создание заказа с ингредиентами")
def test_create_order_with_ingredients(base_url):
    response = requests.get(f"{base_url}/api/ingredients")
    ingredients = response.json()["data"]
    ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]
    response = requests.post(
        f"{base_url}/api/orders",
        json={"ingredients": ingredient_ids},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

@allure.title("Создание заказа без ингредиентов")
def test_create_order_without_ingredients(base_url):
    response = requests.post(
        f"{base_url}/api/orders",
        json={"ingredients": []},
    )
    assert response.status_code == 400
    assert response.json()["success"] is False

@allure.title("Создание заказа с неверным хешем ингредиента")
def test_create_order_with_invalid_ingredient_hash(base_url):
    response = requests.post(
        f"{base_url}/api/orders",
        json={"ingredients": ["invalid_ingredient_hash"]},
    )
    assert response.status_code == 500
