### Note this is still a work in progress and still not functional. 

# kairo
a slackbot framework


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


