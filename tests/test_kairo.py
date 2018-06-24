import pytest
from mock import MagicMock,patch
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
@patch('os.environ.get')
def test_Kairo_allows_to_specific_env_var_name(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time):
    #arrange
    global count 
    count = 0
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

@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
def test_start_bot_takes_in_optional_slack_token(fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time):
    #arrange
    global count 
    count = 0
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
def test_start_bot_populates_user_list(fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time):
    #arrange
    global count 
    count = 0
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
def test_get_user_name_by_id_returns_username(fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time):
    #arrange
    k = Kairo("app")
    fake_api_call.side_effect = api_call_side_effect
    fake_get_sleep_time.return_value = 0        
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_rtm_read.return_value = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]     

    #act
    k.start_bot("fake_token")
    name = k.get_user_name_by_id("1234")
    #assert
    assert name == "fake_bot"   

@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_start_bot_prints_message_if_slack_client_cant_connect(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,capsys):
    #arrange
    global count 
    count = 0
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
    global count 
    count = 0
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

@patch('kairo.Kairo.parse_slack_message')
@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_start_bot_read_passed_to_parse_slack_message(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,fake_parse_slack_message,capsys):
    #arrange
    global count 
    count = 0
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

@patch('kairo.Kairo.parse_slack_message')
@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_command_decorator_is_parsed(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,fake_parse_slack_message,capsys):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_get_sleep_time.return_value = 0        
    fake_message = [{'text' : 'test 123' , 'channel' : 'foo', 'user' : 'bar'}]
    fake_rtm_read.return_value = fake_message   
    fake_rtm_connect.return_value = True
    fake_parse_slack_message.return_value = None,None,None
    fake_api_call.side_effect = api_call_side_effect

    #act
    k = Kairo("app")
    k.start_bot()

    @k.command("hello <name>")
    def foo():
        return True
        
    #assert
    assert "hello1" in k.commands

@patch('kairo.Kairo.send_response')
@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_command_decorator_invokes_function(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,fake_send_response):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_get_sleep_time.return_value = 0        
    fake_message = [{'text' : 'hello bob' , 'channel' : 'foo', 'user' : 'bar'}]
    fake_rtm_read.return_value = fake_message   
    fake_rtm_connect.return_value = True
    fake_api_call.side_effect = api_call_side_effect

    #act
    k = Kairo("app")

    @k.command("hello <name>")
    def foo(user,name):
        return "bar bar"

    k.start_bot()

    #assert
    fake_send_response.assert_called_with('bar bar','foo')

@patch('kairo.Kairo.send_response')
@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_command_decorator_invokes_function_with_parameter(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,fake_send_response):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_get_sleep_time.return_value = 0        
    fake_message = [{'text' : 'hello bob' , 'channel' : 'foo', 'user' : 'bar'}]
    fake_rtm_read.return_value = fake_message   
    fake_rtm_connect.return_value = True
    fake_api_call.side_effect = api_call_side_effect

    #act
    k = Kairo("app")

    @k.command("hello <name>")
    def foo(user,name):
        return name == "bob"
            
    k.start_bot()

    #assert
    fake_send_response.assert_called_with(True,"foo")

@patch('kairo.Kairo.send_response')
@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_command_decorator_invokes_function_with_multiple_parameter(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,fake_send_response):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_get_sleep_time.return_value = 0        
    fake_message = [{'text' : 'hello bob smith' , 'channel' : 'foo', 'user' : 'bar'}]
    fake_rtm_read.return_value = fake_message   
    fake_rtm_connect.return_value = True
    fake_api_call.side_effect = api_call_side_effect

    #act
    k = Kairo("app")

    @k.command("hello <f_name> <l_name>")
    def foo(user,f_name,l_name):
        return f_name == "bob" and l_name == "smith"
            
    k.start_bot()

    #assert
    fake_send_response.assert_called_with(True,"foo")    

@patch('kairo.Kairo.send_response')
@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_command_routes_with_different_params_work(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,fake_send_response):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_get_sleep_time.return_value = 0        
    fake_message = [{'text' : 'hello bob smith' , 'channel' : 'foo', 'user' : 'bar'}]
    fake_rtm_read.return_value = fake_message   
    fake_rtm_connect.return_value = True
    fake_api_call.side_effect = api_call_side_effect

    #act
    k = Kairo("app")

    @k.command("hello <f_name> <l_name>")
    def foo(user,f_name,l_name):
        return f_name == "bob" and l_name == "smith"

    @k.command("hello <f_name>")
    def bar(user,f_name,l_name):
        return f_name == "mike" 

    @k.command("hello")
    def bar(user,f_name,l_name):
        return f_name == "john" 

    k.start_bot()

    #assert
    fake_send_response.assert_called_with(True,"foo")   

@patch('kairo.Kairo.send_response')
@patch('kairo.Kairo.get_sleep_time')  
@patch('kairo.Kairo.running')    
@patch('slackclient.SlackClient.rtm_read')
@patch('slackclient.SlackClient.rtm_connect')
@patch('slackclient.SlackClient.api_call')
@patch('os.environ.get')
def test_command_routes_with_different_params_paramless_command_works(fake_env_get,fake_api_call,fake_rtm_connect,fake_rtm_read,fake_running,fake_get_sleep_time,fake_send_response):
    #arrange
    global count 
    count = 0
    fake_running.side_effect=fake_runner
    fake_get_sleep_time.return_value = 0        
    fake_message = [{'text' : 'hello' , 'channel' : 'foo', 'user' : 'bar'}]
    fake_rtm_read.return_value = fake_message   
    fake_rtm_connect.return_value = True
    fake_api_call.side_effect = api_call_side_effect

    #act
    k = Kairo("app")
    
    @k.command("hello <f_name> <l_name>")
    def foo(user,f_name,l_name):
        return f_name == "bob" and l_name == "smith"

    @k.command("hello <f_name>")
    def bar(user,f_name,l_name):
        return f_name == "mike" 

    @k.command("hello")
    def moo(user):
        return True 
    
    k.start_bot()
    

    #assert
    fake_send_response.assert_called_with(True,"foo")   

#side effects
def api_call_side_effect(input):
    if input == "users.list":
        return {"members" : [{"id" : "1234", "profile" : {"display_name" : "fake_bot"}}]}
    else:
        return {"user_id" : "1234"} 

count = 0
def fake_runner():
    global count 
    count = count + 1
    return count < 2    
     
 


            



