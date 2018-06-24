
count = 0

#side effects
def api_call_side_effect(input):
    if input == "users.list":
        return {"members" : [{"id" : "1234", "profile" : {"display_name" : "fake_bot"}}]}
    else:
        return {"user_id" : "1234"}

def fake_runner():
    global count
    count = count + 1
    return count < 2

def reset_count():
    global count
    count = 0
