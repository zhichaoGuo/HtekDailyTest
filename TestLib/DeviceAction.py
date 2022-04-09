import time
from urllib import parse

from TestLib import hl_request
from TestLib.VoipDevice import VoipDevice


def reboot(device: VoipDevice):
    url = 'http://%s/rb_phone.htm' % device.ip
    r = hl_request('GET', url, auth=(device.user, device.password), timeout=1)
    if r.status_code == 200:
        return True
    else:
        return False


def enable_autotest(device: VoipDevice):
    url = 'http://%s/enable_autotest_api' % device.ip
    r = hl_request('GET', url, auth=(device.user, device.password), timeout=1)
    if r.status_code == 200:
        return True
    else:
        return False


def reset_factory(device: VoipDevice):
    url = 'http://%s/Abyss/FactoryReset' % device.ip
    r = hl_request('GET', url, auth=(device.user, device.password), timeout=1)
    if r.status_code == 200:
        return True
    else:
        return False


def skip_rom_check(device: VoipDevice):
    url = "http://%s/skip_rom_check" % device.ip
    r = hl_request('GET', url, auth=(device.user, device.password), timeout=1)
    if r.status_code == 200:
        return True
    else:
        return False


def auto_provision(device: VoipDevice):
    pValues = {"P900000": ''}
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    url = "http://%s/now_auto_provision.htm" % device.ip
    data = parse.urlencode(pValues).encode(encoding="utf-8")
    req = hl_request('POST', url, headers=headers, data=data, auth=(device.user, device.password), timeout=1)
    if req.status_code == 200:
        return True
    else:
        return False


def sleep_phone_up(device: VoipDevice, timeout=600, loop_time=10):
    url = "http://%s:%s/index.htm" % (device.ip, device.port)
    start_time = time.time()
    time.sleep(loop_time)
    for i in range(int(timeout / loop_time)):
        try:
            r = hl_request('GET', url, auth=(device.user, device.password), timeout=loop_time)
            print('wait %s s phone up' % (time.time() - start_time))
            return True
        except Exception as err:
            print('phone stil not get up %s' % (time.time() - start_time))
    print('wait phone up time out:%s' % (start_time - time.time()))
    return False
