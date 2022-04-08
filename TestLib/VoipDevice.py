from TestLib import hl_request
from TestLib.Utils import postFormToDevice
from TestLib.cfg import CfgGenerator


class VoipDevice:
    def __init__(self, ip: str, port: str, user: str, password: str):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.version = self._get_version()
        self.model = self._get_model()

    def _get_version(self):
        version = ''
        return version

    def _get_model(self):
        model = ''
        return model

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
