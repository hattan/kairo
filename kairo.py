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
        self.load_token_from_env(self.slack_token_name)

    def load_token_from_env(self,name):
        slack_token = os.environ.get(name)
        self.slack_token = slack_token

    def start_bot(self,token=None):
        slack_token = token if (token is not None) else self.slack_token
        if(slack_token is None):
            raise RuntimeError('missing slack token')
        return True