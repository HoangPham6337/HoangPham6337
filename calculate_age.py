from datetime import datetime
from typing import Dict
import requests
import os

token = os.environ['GITHUB_TOKEN']
user = os.environ['USER_NAME']


def calculate_time_difference(end: datetime, start: datetime) -> Dict[str, int]:
    time_delta = int((end - start).total_seconds())
    years = time_delta // (86400 * 365)
    days = time_delta % (86400 * 365) // 86400
    hours = round(time_delta / 3600 % 24)
    minutes = round(time_delta / 60 % 60)
    seconds = time_delta % 60
    return {
        "years": years,
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }

def calculate_account_age(username: str) -> Dict[str, int]:
    response = requests.get(f"https://api.github.com/users/{username}").json()
    date_created = datetime.strptime(response['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.now()
    return calculate_time_difference(now, date_created)

def calculate_my_age(birthday: str) -> Dict[str, int]:
    date_born = datetime.strptime(birthday, "%d %B, %Y")
    now = datetime.now()
    return calculate_time_difference(now, date_born)


if __name__ == "__main__":
    print(calculate_account_age(user))
    print(calculate_my_age("12 March, 2004"))