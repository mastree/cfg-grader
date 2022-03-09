def get_response(err: bool, msg: str, data, status_code: int = 200):
    ret = {
        "error": err,
        "message": msg
    }
    if data:
        if hasattr(data, '__dict__'):
            ret["data"] = data.__dict__
        else:
            ret["data"] = data
    return ret, status_code
