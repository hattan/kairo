import sys
sys.path.append("kairo")

import pytest
from .mock_helpers import fake_runner, api_call_side_effect, reset_count
from mock import MagicMock, patch
from slackclient import SlackClient
from kairo import Kairo

def test_Kairo_exists():
    assert Kairo != None

def test_Kairo_takes_name():
    k = Kairo("app")
    assert True

def test_parse_slack_message_with_none_passed_returns_none_tuple():
    k = Kairo("app")
    command, channel, user = k.parse_slack_message(None)
    assert command is None
    assert channel is None
    assert user is None

@patch('slackclient.SlackClient.api_call')
def test_send_response_calls_slack_client_api_call(fake_api_call):
    k = Kairo("app")
    k.slack_client = SlackClient("fake_token") #slack_client is instantiated in start_bot, calling this even to avoid mocking everything else.
    k.send_response("text1","channel2")
    fake_api_call.assert_called_with("chat.postMessage",channel="channel2",text="text1",as_user=True)

@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_Kairo_allows_to_specific_env_var_name(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time):
    #arrange
    reset_count()
    fake_running.side_effect=fake_runner
    fake_token_name = 'my_env_var'
    fake_api_call.side_effect = api_call_side_effect
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]    
    fake_rtm_connect.return_value = True
    fake_get_sleep_time.return_value = 0

    #act
    k = Kairo("app")
    k.load_token_from_env(name = fake_token_name)
    k.start_bot()
    
    #assert
    fake_env_get.assert_called_with(fake_token_name)    

def test_Kairo_has_users_member():
    #arrange
    k = Kairo("app")

    #assert
    assert k.users is None

def test_Kairo_has_slack_client_member():
    #arrange
    k = Kairo("app")

    #assert
    assert k.slack_client is None    


@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
def test_get_user_name_by_id_returns_username(fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time):
    #arrange
    k = Kairo("app")
    fake_api_call.side_effect = api_call_side_effect
    fake_get_sleep_time.return_value = 0
    reset_count()
    fake_running.side_effect=fake_runner
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]     

    #act
    k.start_bot("fake_token")
    name = k.get_user_name_by_id("1234")
    #assert
    assert name == "fake_bot"   


@patch('slackclient.SlackClient.api_call')
def test_get_sleep_time_returns_one(fake_api_call):
    #arrange
    k = Kairo("app")
    sleep_time = k.get_sleep_time()
    #assert
    assert sleep_time == 1 

def test_running_returns_true():
    #arrange
    k = Kairo("app")
    running = k.running()
    #assert
    assert running == 1 


def test_parse_slack_message_returns_text_from_message():
    #arrange
    fake_message = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]
    k = Kairo("app")
    #act
    message,channel,user = k.parse_slack_message(fake_message)
    #assert
    assert 'test 123' == message

def test_parse_slack_message_returns_channel_from_message():
    #arrange
    fake_message = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]
    k = Kairo("app")
    #act
    message,channel,user = k.parse_slack_message(fake_message)
    #assert
    assert 'foo' == channel

def test_parse_slack_message_returns_user_from_message():
    #arrange
    fake_message = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]
    k = Kairo("app")
    #act
    message,channel,user = k.parse_slack_message(fake_message)
    #assert
    assert 'bar' == user    




 


            



