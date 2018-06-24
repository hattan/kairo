# kairo
a slackbot framework

### Installation

In order to use kairo with slack, you need to create a [slack app](https://api.slack.com/apps?new_app=1). After creating an app, you need to get you API Token. That token needs to be added to an environment variable named 'KAIRO_SLACK_TOKEN'. 
You can also configure the Slack API token using other mechanisms. See (Slack Token Configuration below.)

Install deps : 

    pip install -r requirements.text 

#### Create a bot script (eg example.py)    
The bot should be up and running.
example:
```python

from kairo import Kairo

app = Kairo(__name__)

@app.command("hello <name>")
def hello(name):
    return "Hello {name}".format(name=name) 

app.start_bot()    
```

 In slack invoke bot using
 > bot hello foo

#### Start bot
```python example.py```


### Slack Token Configuration
Kairo has multiple methods in which you can configure the slack api token. 

* Create an environment variable called KAIRO_SLACK_TOKEN. Kairo will look for this token and use it if found.
* Call the method load_token_from_env with the name of the environment varible you would like to use
```python
from kairo import Kairo

app = Kairo(__name__)
app.load_token_from_env("CUSTOM_ENVIRONMENT_VARIABLE")
```
* Don't want to use environment variables? No problem! Pass a token to the start_bot method.
```python
from kairo import Kairo

app = Kairo(__name__)

@app.command("hello <name>")
def hello(name):
    return "Hello {name}".format(name=name) 

app.start_bot("slack_api_token_here")    
```