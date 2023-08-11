import requests
from dotenv import load_dotenv
import os

webhook_url_moderator_only = os.environ["webhook_url_moderator_only"]
github_release_url = "https://api.github.com/repos/kelvin-codes-stuff/AllDayBot/releases/latest"


#
# release info
#
github_release_repo = requests.get(github_release_url).json()

changes = str(github_release_repo["body"]).split("*")
list_changes = ""
changelog_url = f"https://github.com/kelvin-codes-stuff/AllDayBot/commits/{github_release_repo['tag_name']}"

for item in changes:
    if "What's Changed" not in item: 
        item = item.replace("\r", "")
        item = item.replace("https://github.com/kelvin-codes-stuff/AllDayBot/pull/", "pull request ")
        list_changes = list_changes + f"- {item}"

list_changes = list_changes.replace(f"- - Full Changelog- - : https://github.com/kelvin-codes-stuff/AllDayBot/commits/{github_release_repo['tag_name']}", "")


#
# Webhook 
# 
data = {
    "username": "Github AllDayBot"
}

data["embeds"] = [{
        "title" : "AllDayBot heeft een nieuwe release!",
        "description" : f"**Versie: `{github_release_repo['tag_name']}`**",
        "fields": [{"name": "Wijzigingen:", "value": str(list_changes)}] # For loop for release notes
}]

res = requests.post(url=webhook_url_moderator_only, json=data)

try:
    res.raise_for_status()
except requests.exceptions.HTTPError as error:
    print(error)
else:
    print(f"Done! status code: {res.status_code}")
