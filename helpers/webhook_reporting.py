import requests
from env import Webhooks

class Logging:
    # Error logging
    def error(event, error):
        data = {
            "username": "Error report"
        }

        data["embeds"] = [
            {
                "title": event,
                "description": error
            } 
        ]

        res = requests.post("https://discord.com/api/webhooks/1227696726509359267/U0RRy8Lmn6ywYkijLbarqSRFR_xrE319PhyCNlwL0HgiDGRWRfAjn5NPOpJGpV-UOQZQ", json=data) # Temp webhook

        try: 
            res.raise_for_status()
        except Exception as error:
            print(error)
            return
        
        print("Done!")

