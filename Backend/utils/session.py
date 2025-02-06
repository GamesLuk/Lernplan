from utils.system import debug

def set_Session_Value(request, name, value):
    request.session[f"{name}"] = value

def get_Session_Value(request, name):
    return request.session.get(f"{name}")

def get_User_Value(request, name):
    debug([f"User: {name} {request.session.get("user")[name][name]}"])
    return request.session.get("user")[name][name]