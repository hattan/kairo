import os
import time
from functools import wraps

from slackclient import SlackClient


class Kairo:
    name = None
    slack_token = None
    slack_token_name = 'KAIRO_SLACK_TOKEN'
    slack_client = None
    users = None

    def __init__(self, name):
        self.name = name
        self.load_token_from_env(self.slack_token_name)

    def load_token_from_env(self, name):
        slack_token = os.environ.get(name)
        self.slack_token = slack_token

    def get_user_name_by_id(self, id):
        users = self.users
        return [user["profile"]["display_name"] for user in users.get("members", {}) if user["id"] == id][0]

    def get_sleep_time(self):
        return 1

    def running(self):
        return True

    def parse_slack_message(self, slack_incoming_message):
        output_list = slack_incoming_message
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output:
                    return output['text'].strip(), output['channel'], output['user']

        return None, None, None

    def parse_input(self, command):
        parts = command.split(' ')
        size = len(parts)
        command = parts[0] if size > 0 else None
        count = 1
        args = []
        while count < size:
            argument = parts[count].strip()
            if argument is not '':
                args.append(argument)
            count = count + 1
        return command, args

    def handle_command(self, text, channel, user):
        if text is not '':
            command, args = self.parse_input(text)
            key = self.get_key(command, args)
            if key in self.commands:
                action = self.commands[key]
                text = action(user, *args)

                if text is not None:
                    self.send_response(text, channel)

    def start_bot(self, token=None):
        slack_token = token if (token is not None) else self.slack_token
        if slack_token is None:
            raise RuntimeError('missing slack token')

        self.slack_client = SlackClient(slack_token)
        self.users = self.slack_client.api_call("users.list")
        bot_id = self.slack_client.api_call("auth.test")["user_id"]
        bot_name = self.get_user_name_by_id(bot_id)
        sleep_delay = self.get_sleep_time()

        if self.slack_client.rtm_connect():
            print(bot_name + " connected and running!")
            while self.running():
                text = self.slack_client.rtm_read()
                command, channel, user = self.parse_slack_message(text)
                if command and channel:
                    self.handle_command(command, channel, user)

                time.sleep(sleep_delay)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
        return True

    def send_response(self, text, channel):
        self.slack_client.api_call("chat.postMessage", channel=channel, text=text, as_user=True)

    def get_key(self, command, args):
        return command + str(len(args))

    commands = {}

    def parse_command(self, text, command_function):
        command, args = self.parse_input(text)
        key = self.get_key(command, args)
        self.commands[key] = command_function

    def command(self, text):
        def _command(command_function):
            self.parse_command(text, command_function)

            @wraps(command_function)
            def wrapper(*args):
                rv = command_function(*args)
                return rv

            return wrapper

        return _command
