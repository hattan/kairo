import sys
sys.path.append("kairo")

from mock import patch
from kairo import Kairo


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

 


            



