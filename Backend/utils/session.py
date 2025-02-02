
def set_Session_Value(request, name, value):
    request.session[name] = value

def get_Session_Value(request, name):
    return request.session.get(name)

def get_User_Value(request, name):
    return request.session.get("user").get(name)[name]