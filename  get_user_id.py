import requests

SLACK_BOT_TOKEN = "xoxb-8715634668211-8715649203555-RVSxeEIgEkNPHl3LuKSvLu3W"

def get_user_id():
    response = requests.get(
        "https://slack.com/api/users.list",
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
        }
    )
    users = response.json().get("members", [])
    for user in users:
        name = user.get("name")
        uid = user.get("id")
        is_bot = user.get("is_bot", False)
        deleted = user.get("deleted", False)
        if not is_bot and not deleted:
            print(f"👤 {name} ➤ {uid}")

get_user_id()
