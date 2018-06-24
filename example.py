from kairo import Kairo

k = Kairo("app")

@k.command("hello <f_name> <l_name>")
def foo(user,f_name,l_name):
    return "Hello {f_name} {l_name}, it's nice to meet you!".format(f_name=f_name,l_name=l_name) 
        
k.start_bot("slack_api_token_here")