import uuid

def generate_user_data():
    unique_id = uuid.uuid4().hex

    return {
        "email": f"test_{unique_id}@yandex.ru",
        "password": f"Password_{unique_id}",
        "name": f"TestUser_{unique_id}",
    }