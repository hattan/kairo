### Note this is still a work in progress and still not functional. 

# kairo
a slackbot framework


```python

from kairo import Kairo

app = Kairo(__name__)
app.start_bot()

@command("/bot/hello/<name>")
def hello(name):
    return "Hello {name}".format(name=name) 
```

 In slack invoke bot using
 > bot hello foo


