import uuid
import requests

from constants import BASE_URL

def generate_user_data():
    unique_id = uuid.uuid4().hex
    
    return {
        "email": f"test_{unique_id}@yandex.ru",
        "password": f"Password_{unique_id}",
        "name": f"TestUser_{unique_id}",
    }

def get_ingredient_ids():
    with requests.get(f"{BASE_URL}/api/ingredients") as response:
        ingredients = response.json()["data"]
    return [ingredients[0]["_id"], ingredients[1]["_id"]]