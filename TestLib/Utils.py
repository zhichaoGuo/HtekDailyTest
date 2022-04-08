import requests
from urllib import parse


def hl_request(method, url, **kwargs):
    r = requests.request(method, url, **kwargs)
    return r


def postFormToDevice(url: str, user: str, password: str, values: dict):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    auth = (user, password)
    try:
        data = parse.urlencode(values).encode(encoding="utf-8")

        req = hl_request('POST', url, headers=headers, data=data, auth=auth)
        if req.status_code == 200:
            return True
    except Exception as err:
        print("postFormToDevice err:", err)
        return False
    return True
