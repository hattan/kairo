import os
import glob
import importlib
import inspect
import time
from slackclient import SlackClient

class Kairo:
    name = None
    slack_token = None
    slack_token_name = 'KARIO_SLACK_TOKEN'

    def __init__(self,name):
        self.name = name
        self.load_token_from_env()

    def load_token_from_env(self):
        slack_token = os.environ.get(self.slack_token_name)
        self.slack_token = slack_token

    def start_bot(self):
        if(self.slack_token is None):
            raise RuntimeError('missing slack token')
        return True