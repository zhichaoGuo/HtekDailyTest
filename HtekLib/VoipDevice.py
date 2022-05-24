import re
import time
from urllib import parse

import allure

from HtekLib.TestUtils import hl_request


class VoipDevice:
    def __init__(self, ip: str, port: int, http_port=80,user='admin', password='admin'):
        self.ip = ip
        self.port = port
        self.http_port = http_port
        self.user = user
        self.password = password
        self.root_url = 'http://%s:%s' % (self.ip, self.http_port)
        self.auth = (self.user, self.password)
        self.page = hl_request('GET', f'{self.root_url}/index.htm', auth=self.auth, timeout=1).text
        self.mac = self._get_mac()
        self.version = self._get_version()

    def _get_mac(self):
        text = self.page
        re_1 = 'jscs.mac_address'
        re_2 = '</td>'
        text = text[re.search(re_1, text, re.U).span()[1] + 45:]
        text = text[:re.search(re_2, text, re.U).span()[0]]
        return text

    def _get_version(self):
        text = self.page
        re_1 = 'ROM--'
        re_2 = '\\('
        try:
            text = text[re.search(re_1, text, re.U).span()[1]:]
            text = text[:re.search(re_2, text, re.U).span()[0]]
        # except AttributeError:
        except Exception:
            time.sleep(10)
            text = text[re.search(re_1, text, re.U).span()[1]:]
            text = text[:re.search(re_2, text, re.U).span()[0]]
        return text

    def _get_model(self):
        text = self.page
        re_1 = 'jscs.product_type'
        re_2 = '</td>'
        text = text[re.search(re_1, text, re.U).span()[1] + 44:]
        text = text[:re.search(re_2, text, re.U).span()[0]]
        return text

    def _enable_auto_test(self):
        url = self.root_url + '/enable_autotest_api'
        r = hl_request('GET', url, auth=self.auth)
        if r is False:
            return False
        elif r.status_code != 200:
            return False
        return True

    def _enable_telnet(self):
        url = self.root_url + '/AutoTest&action=enabletelnet'
        r = hl_request('GET', url, auth=self.auth)
        if r is False:
            return False
        elif r.status_code != 200:
            return False
        return True

    def _enable_ftp(self):
        url = self.root_url + '/AutoTest&action=enableftp'
        r = hl_request('GET', url, auth=self.auth)
        if r is False:
            return False
        elif r.status_code != 200:
            return False
        return True

    @allure.step('允许debug模式')
    def enable_debug(self):
        if self._enable_auto_test():
            if self._enable_telnet() and self._enable_ftp():
                return True
            else:
                return False
        else:
            return False

    @allure.step('允许自动化测试接口')
    def enable_autotest(self):
        if self._enable_auto_test():
            return True
        else:
            return False

    @allure.step('重启话机')
    def reboot(self):
        url = self.root_url + '/rb_phone.htm'
        r = hl_request('GET', url, auth=self.auth)
        if r is False:
            return False
        elif r.status_code != 200:
            return False
        return True

    @allure.step('执行恢复出厂')
    def factory(self):
        # url = self.root_url + '/rsf.htm'
        url = self.root_url + "/Abyss/FactoryReset"
        r = hl_request('GET', url, auth=self.auth)
        if r is False:
            return False
        elif r.status_code != 200:
            return False
        return True

    @allure.step('跳过rom版本检查')
    def skip_rom_check(self):
        url = self.root_url + "/skip_rom_check"
        r = hl_request('GET', url, auth=self.auth)
        if r is False:
            return False
        elif r.status_code != 200:
            return False
        return True

    @allure.step('执行ap')
    def auto_provision(self):
        pValues = {
            "P900000": ''
        }
        self.skip_rom_check()
        url = self.root_url + "/now_auto_provision.htm"
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
        data = parse.urlencode(pValues).encode(encoding="utf-8")
        r = hl_request('POST', url, headers=headers,auth=self.auth,data=data)
        if r is False:
            return False
        elif r.status_code != 200:
            return False
        return True

    @allure.step('make call')
    def call(self, aim_account):
        url = self.root_url + "/Phone_ActionURL&Command=1&Number=%s&Account=1" % aim_account
        r = hl_request('GET', url, auth=self.auth)
        if r is False:
            return False
        elif r.status_code != 200:
            return False
        return True

    @allure.step('执行按键')
    def send_key(self, key_code):
        url = self.root_url + "/Phone_ActionURL&Command=3&key=%s" % key_code
        headers = {'Connection': 'close'}
        r = hl_request('GET', url, headers=headers, auth=self.auth)
        if r is False:
            return False
        elif r.status_code != 200:
            return False
        return True

    @allure.step('设置P值')
    def set_p(self, p_num, p_value):
        pass

    @allure.step('检查P值')
    def check_p(self, p_num, p_value):
        pass

    @allure.step('注册账号')
    def register(self, sip_server, name_id, auth_id, auth_password, account_num=1):
        pass

    @allure.step('账号去注册')
    def remove_reg(self, account_num=1):
        pass

    @allure.step('检查版本')
    def check_version(self, version):
        pass

    @allure.step('检查是否在线')
    def is_power_on(self):
        pass

    @allure.step('保存截屏')
    def save_screen(self, src_dir):
        pass

    @allure.step('保存log文件')
    def save_log(self, src_dir):
        pass

    @allure.step('保存配置文件')
    def save_cfg(self, src_dir, cfg_type='xml'):
        pass


if __name__ == '__main__':
    A = VoipDevice('10.3.3.116', 80)
    print(A.mac)
