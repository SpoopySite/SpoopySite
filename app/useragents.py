import json
import random


def get_random_user_agent() -> str:
    with open("./app/useragents.json") as file:
        data = json.load(file)
        return random.choice(data.get("urls"))
