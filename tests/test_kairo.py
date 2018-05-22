import pytest
from mock import MagicMock,patch
from slackclient import SlackClient

from kairo import Kairo

def test_Kairo_exists():
    assert Kairo != None

def test_Kairo_takes_name():
    k = Kairo("app")
    assert True

@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_Kairo_has_start_bot_method(fake_env_get,fake_api_call):
    #arrange
    fake_api_call.side_effect = api_call_side_effect 
    fake_env_get.return_value = "1234"  
    
    #act
    k = Kairo("app")
    k.start_bot()
    
    #assert
    assert True

@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_start_bot_throws_error_if_slack_token_not_in_environment_var(fake_env_get,fake_api_call,fake_rtm_connect):
    fake_api_call.side_effect = api_call_side_effect
    fake_env_get.return_value = None
    fake_rtm_connect.return_value = True

    with pytest.raises(RuntimeError) as excinfo:
        k = Kairo("app")
        k.start_bot()

    assert 'missing slack token' in str(excinfo.value)

count = 0
def fake_runner():
    global count 
    count = count + 1
    return count < 2

@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_Kairo_allows_to_specific_env_var_name(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_token_name = 'my_env_var'
    fake_api_call.side_effect = api_call_side_effect
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]    
    fake_rtm_connect.return_value = True
    
    #act
    k = Kairo("app")
    k.load_token_from_env(name = fake_token_name)
    k.start_bot()
    
    #assert
    fake_env_get.assert_called_with(fake_token_name)    

@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
def test_start_bot_takes_in_optional_slack_token(fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]     

    slack_token = "fake_slack_token"
    fake_api_call.side_effect = api_call_side_effect

    #act
    k = Kairo("app")
    k.start_bot(slack_token)
    
    #assert
    assert True # no failures

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

@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
def test_start_bot_populates_user_list(fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]         
    k = Kairo("app")
    fake_api_call.side_effect = api_call_side_effect

    #act
    k.start_bot()

    #assert
    assert k.users is not None
    assert len(k.users) > 0 

@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
def test_get_user_name_by_id_returns_username(fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running):
    #arrange
    k = Kairo("app")
    fake_api_call.side_effect = api_call_side_effect
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]     

    #act
    k.start_bot()
    name = k.get_user_name_by_id("1234")
    #assert
    assert name == "fake_bot"   

def api_call_side_effect(input):
    if input == "users.list":
        return {"members" : [{"id" : "1234", "profile" : {"display_name" : "fake_bot"}}]}
    else:
        return {"user_id" : "1234"} 

@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_start_bot_prints_message_if_slack_client_cant_connect(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,capsys):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]         
    k = Kairo("app")
    fake_rtm_connect.return_value = False
    fake_api_call.side_effect = api_call_side_effect
    #act
    k.start_bot()
    #assert
    out, err = capsys.readouterr()
    assert out == "Connection failed. Invalid Slack token or bot ID?\n"


@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_start_bot_success_prints_connected_message(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,capsys):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]        
    k = Kairo("app")
    fake_rtm_connect.return_value = True
    fake_api_call.side_effect = api_call_side_effect
    #act
    k.start_bot()
    #assert
    out, err = capsys.readouterr()
    print(out)
    assert  "fake_bot connected and running!\n" == out

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
     
 


            



