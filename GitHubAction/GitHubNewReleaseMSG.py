import requests
from dotenv import load_dotenv
import os

webhook_url_moderator_only = os.environ["webhook_url_moderator_only"]
webhook_url_alldaybot = os.environ["webhook_url_alldaybot"]

github_release_url = "https://api.github.com/repos/kelvin-codes-stuff/AllDayBot/releases/latest"


# Release info
github_release_repo = requests.get(github_release_url).json()

changes = str(github_release_repo["body"]).split("*")
list_changes = ""
changelog_url = f"https://github.com/kelvin-codes-stuff/AllDayBot/commits/{github_release_repo['tag_name']}"

for item in changes:
    if "What's Changed" not in item: 
        item = item.replace("\r", "")
        item = item.replace("https://github.com/kelvin-codes-stuff/AllDayBot/pull/", "pull request ")
        list_changes = list_changes + f"- {item}"

list_changes = list_changes.replace(f"- - Full Changelog- - :", "- Alle wijzigingen:")


# Webhook 
data = {
    "username": "Github AllDayBot"
}

data["embeds"] = [{
        "title" : "AllDayBot heeft een nieuwe release!",
        "description" : f"**Versie: `{github_release_repo['tag_name']}`**",
        "fields": [{"name": "Wijzigingen:", "value": str(list_changes)}] # For loop for release notes
}]

moderator_embed = requests.post(url=webhook_url_moderator_only, json=data)
alldaybot_embed = requests.post(url=webhook_url_alldaybot, json=data)

try:
    moderator_embed.raise_for_status()
    alldaybot_embed.raise_for_status()
except requests.exceptions.HTTPError as error:
    print(error)
else:
    print(f"Done! status code embed 1: {moderator_embed.status_code}. Status code embed 2: {alldaybot_embed.status_code}")
