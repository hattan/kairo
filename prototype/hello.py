#note this is non funcitoning code and is simply a proposed design !!


from kairo import Kairo,Text,Attachement

k = Kairo("app")

@k.command("hello <f_name> <l_name>")
def foo(user,f_name,l_name):
    return "Hello {f_name} {l_name}, it's nice to meet you!".format(f_name=f_name,l_name=l_name)
    
@k.command("hey <f_name> <l_name>")
def moo(user,f_name,l_name):
    return Text("Hello {f_name} {l_name}, it's nice to meet you!".format(f_name=f_name,l_name=l_name))

@k.command("yo <f_name> <l_name>")
def boo(user,f_name,l_name):
    return Attachment(title="my response",text="this is text",image_url="https://www.google.com")

k.start_bot()