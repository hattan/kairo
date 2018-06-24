import sys
sys.path.append("kairo")

import pytest
from .mock_helpers import fake_runner, api_call_side_effect, reset_count
from mock import MagicMock, patch
from slackclient import SlackClient
from kairo import Kairo

@patch('kairo.Kairo.get_sleep_time')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_Kairo_has_start_bot_method(fake_env_get,fake_api_call,fake_get_sleep_time):
    #arrange
    fake_api_call.side_effect = api_call_side_effect 
    fake_env_get.return_value = "1234"  
    fake_get_sleep_time.return_value = 0

    #act
    k = Kairo("app")
    k.start_bot()
    
    #assert
    assert True

@patch('kairo.Kairo.get_sleep_time')  
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_start_bot_throws_error_if_slack_token_not_in_environment_var(fake_env_get,fake_api_call,fake_rtm_connect,fake_get_sleep_time):
    fake_api_call.side_effect = api_call_side_effect
    fake_env_get.return_value = None
    fake_rtm_connect.return_value = True
    fake_get_sleep_time.return_value = 0

    with pytest.raises(RuntimeError) as excinfo:
        k = Kairo("app")
        k.start_bot()

    assert 'missing slack token' in str(excinfo.value)

@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
def test_start_bot_takes_in_optional_slack_token(fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time):
    #arrange
    reset_count
    fake_running.side_effect=fake_runner
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]     
    fake_get_sleep_time.return_value = 0

    slack_token = "fake_slack_token"
    fake_api_call.side_effect = api_call_side_effect

    #act
    k = Kairo("app")
    k.start_bot(slack_token)
    
    #assert
    assert True # no failures

@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
def test_start_bot_populates_user_list(fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time):
    #arrange
    reset_count()
    fake_running.side_effect=fake_runner
    fake_get_sleep_time.return_value = 0    
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]         
    k = Kairo("app")
    fake_api_call.side_effect = api_call_side_effect

    #act
    k.start_bot("fake_slack_token")

    #assert
    assert k.users is not None
    assert len(k.users) > 0 

@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_start_bot_prints_message_if_slack_client_cant_connect(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,capsys):
    #arrange
    reset_count()
    fake_running.side_effect=fake_runner
    fake_get_sleep_time.return_value = 0       
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]         
    k = Kairo("app")
    fake_rtm_connect.return_value = False
    fake_api_call.side_effect = api_call_side_effect
    #act
    k.start_bot()
    #assert
    out, err = capsys.readouterr()
    assert out == "Connection failed. Invalid Slack token or bot ID?\n"

@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_start_bot_success_prints_connected_message(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,capsys):
    #arrange
    reset_count()
    fake_running.side_effect=fake_runner
    fake_get_sleep_time.return_value = 0        
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]        
    k = Kairo("app")
    fake_rtm_connect.return_value = True
    fake_api_call.side_effect = api_call_side_effect
    #act
    k.start_bot()
    #assert
    out, err = capsys.readouterr()
    assert  "fake_bot connected and running!\n" == out

@patch('kairo.Kairo.parse_slack_message')
@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_start_bot_read_passed_to_parse_slack_message(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,fake_parse_slack_message,capsys):
    #arrange
    reset_count()
    fake_running.side_effect=fake_runner
    fake_get_sleep_time.return_value = 0        
    fake_message = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]
    fake_rtm_read.return_value = fake_message        
    k = Kairo("app")
    fake_rtm_connect.return_value = True
    fake_parse_slack_message.return_value = None,None,None
    fake_api_call.side_effect = api_call_side_effect
    #act
    k.start_bot()
    #assert
    fake_parse_slack_message.assert_called_with(fake_message)



 


            



