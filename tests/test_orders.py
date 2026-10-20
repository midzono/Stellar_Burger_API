import allure
import requests

from constants import BASE_URL

class TestOrders:

    def get_ingredient_ids(self):
        with allure.step("Получить список ингредиентов"):
            response = requests.get(
                f"{BASE_URL}/api/ingredients"
            )
        assert response.status_code == 200
        ingredients = response.json()["data"]
        return [ingredients[0]["_id"], ingredients[1]["_id"]]

    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_authorized(self, registered_user):
        ingredient_ids = self.get_ingredient_ids()
        with allure.step("Создать заказ с авторизацией"):
            response = requests.post(
                f"{BASE_URL}/api/orders",
                json={"ingredients": ingredient_ids},
                headers={
                    "Authorization": registered_user["access_token"]
                },
            )
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self):
        ingredient_ids = self.get_ingredient_ids()
        with allure.step("Создать заказ без авторизации"):
            response = requests.post(
                f"{BASE_URL}/api/orders",
                json={"ingredients": ingredient_ids},
            )
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self):
        ingredient_ids = self.get_ingredient_ids()
        with allure.step("Создать заказ с ингредиентами"):
            response = requests.post(
                f"{BASE_URL}/api/orders",
                json={"ingredients": ingredient_ids},
            )
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        with allure.step("Создать заказ без ингредиентов"):
            response = requests.post(
                f"{BASE_URL}/api/orders",
                json={"ingredients": []},
            )
        assert response.status_code == 400
        assert response.json()["success"] is False

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self):
        with allure.step("Создать заказ с неверным хешем"):
            response = requests.post(
                f"{BASE_URL}/api/orders",
                json={"ingredients": ["invalid_ingredient_hash"]},
            )
        assert response.status_code == 500