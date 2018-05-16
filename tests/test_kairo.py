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