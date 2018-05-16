import pytest
from mock import MagicMock,patch

from kairo import Kairo

def test_Kairo_exists():
    assert Kairo != None

def test_Kairo_takes_name():
    k = Kairo("app")
    assert True

@patch('os.environ.get')
def test_Kairo_has_start_bot_method(fake_env_get):
    #arrange
    fake_env_get.return_value = "1234"  
    
    #act
    k = Kairo("app")
    k.start_bot()
    
    #assert
    assert True

def test_start_bot_throws_error_if_slack_token_not_in_environment_var():
    with pytest.raises(RuntimeError) as excinfo:
        k = Kairo("app")
        k.start_bot()

    assert 'missing slack token' in str(excinfo.value)

@patch('os.environ.get')
def test_Kairo_allows_to_specific_env_var_name(fake_env_get):
    #arrange
    fake_token_name = 'my_env_var'
    
    #act
    k = Kairo("app")
    k.load_token_from_env(name = fake_token_name)
    k.start_bot()
    
    #assert
    fake_env_get.assert_called_with(fake_token_name)

def test_start_bot_takes_in_optional_slack_token():
    #arrange
    slack_token = "fake_slack_token"

    #act
    k = Kairo("app")
    k.start_bot(slack_token)
    
    #assert
    assert True # no failures



