import re

from TestLib import hl_request
from TestLib.Utils import postFormToDevice
from TestLib.cfg import CfgGenerator


class VoipDevice:
    def __init__(self, ip: str, port: str, user: str, password: str):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        text = hl_request('GET', 'http://%s/index.htm' % ip, auth=(user, password), timeout=1).text
        self.version = self._get_version(text)
        self.model = self._get_model(text)
        self.mac = self._get_mac(text)

    def _get_version(self, text):
        re_1 = 'ROM--'
        re_2 = '\('
        text = text[re.search(re_1, text, re.U).span()[1]:]
        text = text[:re.search(re_2, text, re.U).span()[0]]
        return text

    def _get_model(self, text):
        re_1 = 'jscs.product_type'
        re_2 = '</td>'
        text = text[re.search(re_1, text, re.U).span()[1] + 44:]
        text = text[:re.search(re_2, text, re.U).span()[0]]
        return text

    def _get_mac(self,text):
        re_1 = 'jscs.mac_address'
        re_2 = '</td>'
        text = text[re.search(re_1, text, re.U).span()[1] + 45:]
        text = text[:re.search(re_2, text, re.U).span()[0]]
        return text

    def sendKey(self, keyCode: str):
        url = "http://%s:%s/Phone_ActionURL&Command=3&key=%s" % (self.ip, self.port, keyCode)
        headers = {'Connection': 'close', }
        auth = (self.user, self.password)
        try:
            r = hl_request('GET', url, auth=auth, timeout=15, headers=headers)
            if r.status_code == 200:
                return True
            else:
                print("sendKey r.status_code", r.status_code)
        except Exception as err:
            print("LaunchApp err: ", err)
            return False
        return False

    def set_rom_path(self, rom_path_url):
        pValues = {"P192": rom_path_url}
        url = "http://%s:%s/save_managerment.htm" % (self.ip, self.port)
        return postFormToDevice(url, self.user, self.password, pValues)

    def WebSaveCfg(self, PStrValues: dict):
        pValues = CfgGenerator.transforPStrToPNo(PStrValues)
        url = "http://%s:%s/save_managerment.htm" % (self.ip, self.port)
        return postFormToDevice(url, self.user, self.password, pValues)
