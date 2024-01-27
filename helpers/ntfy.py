import requests
from env import Ntfy


class NtfyLogging:
    def info(information):
        try:
            requests.post(url=f"https://ntfy.sh/{Ntfy.TOPIC_BOT}", data=f"Info: {information}")
        except Exception as error:
            print(error)
            pass


    def warning(error):
        try:
            requests.post(url=f"https://ntfy.sh/{Ntfy.TOPIC_BOT}", data=f"Waarschuwing: {error}")
        except Exception as error:
            print(error)
            pass


    def error(error):
        try:        
            requests.post(url=f"https://ntfy.sh/{Ntfy.TOPIC_BOT}", data=f"Error: {error}")
        except Exception as error:
            print(error)
            pass

