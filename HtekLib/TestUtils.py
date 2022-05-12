import time
import requests


def hl_request(method, url, retry=0, **kwargs):
    time.sleep(0.5)
    if retry == 3:
        return False
    try:
        print('[%d] send %s request to %s' % (retry, method, url))
        req = requests.request(method, url, **kwargs)
        if (req.status_code == 401) | (req.status_code == 403):
            req = requests.request(method, url, **kwargs)
    except Exception as err:
        print(err)
        return hl_request(method, url, retry + 1, **kwargs)
    time.sleep(0.5)
    return req
