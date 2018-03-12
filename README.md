# kairo
a slackbot framework


```python from kairo import Kairo
app = Kairo(__name__)

@command("/bot/hello/<name>"
def hello(name):
    return "Hello {name}".format(name=name)```
 
 In slack invoke bot using
 > bot hello foo


