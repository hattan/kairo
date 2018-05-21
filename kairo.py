import os
import glob
import importlib
import inspect
import time
from slackclient import SlackClient

class Kairo:
    name = None
    slack_token = None
    slack_token_name = 'KAIRO_SLACK_TOKEN'
    slack_client = None
    users = None

    def __init__(self,name):
        self.name = name
        self.load_token_from_env(self.slack_token_name)

    def load_token_from_env(self,name):
        slack_token = os.environ.get(name)
        self.slack_token = slack_token

    def get_user_name_by_id(self,id):
        users = self.users
        return [user["profile"]["display_name"] for user in users.get("members",{}) if user["id"] == id][0]

    def start_bot(self,token=None):
        slack_token = token if (token is not None) else self.slack_token
        if(slack_token is None):
            raise RuntimeError('missing slack token')

        self.slack_client = SlackClient(slack_token)
        self.users = self.slack_client.api_call("users.list")
        bot_id = self.slack_client.api_call("auth.test")["user_id"]
        return True