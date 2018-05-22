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

    def get_sleep_time(self):
        return 1 #second delay between reading from firehose

    def running(self):
        return True

    def parse_slack_message(self,slack_incoming_message):
        output_list = slack_incoming_message
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output:
                    return output['text'].strip(), output['channel'], output['user']

        return None, None, None

    def start_bot(self,token=None):
        slack_token = token if (token is not None) else self.slack_token
        if(slack_token is None):
            raise RuntimeError('missing slack token')

        self.slack_client = SlackClient(slack_token)
        self.users = self.slack_client.api_call("users.list")
        bot_id = self.slack_client.api_call("auth.test")["user_id"]
        bot_name = self.get_user_name_by_id(bot_id)
        READ_WEBSOCKET_DELAY = self.get_sleep_time()

        if self.slack_client.rtm_connect():
            print(bot_name + " connected and running!")
            while self.running():
                command, channel, user = self.parse_slack_message(self.slack_client.rtm_read())
                time.sleep(READ_WEBSOCKET_DELAY)            
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
        return True