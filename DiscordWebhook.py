import requests
import json


class DiscordWebhook:
    webhook = None

    def __init__(self, filepath_webhook: str):
        # load secret discord webhook from file
        with open(filepath_webhook, "r") as file_webhook:
            self.webhook = file_webhook.readline().rstrip('\n')
            file_webhook.close()
        # if not self.webhook:
            # this file had no webhook
            # return

    def send_msg(self, msg: str):
        out = True
        headers = {'Content-type': 'application/json'}
        payload = {"content": msg}
        try:
            request = requests.post(self.webhook, data=json.dumps(payload), headers=headers)
        except requests.exceptions.RequestException as e:
            # sth went wrong when HTTP POSTing message to Discord Webhook
            out = False
        else:
            request.close()
        return out
