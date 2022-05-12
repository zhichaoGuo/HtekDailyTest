import re
import time

import allure

from HtekLib.TestUtils import hl_request


class VoipDevice:
    def __init__(self, ip: str, port: int, user='admin', password='admin'):
        self.ip = ip
        self.port = port
        self.mac = self._get_mac()
        self.version = self._get_version()
        self.user = user
        self.password = password
        self.page = hl_request('GET', 'http://%s/index.htm' % self.ip, auth=(self.user, self.password), timeout=1).text

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
        pass

    def _enable_telnet(self):
        pass

    def _enable_ftp(self):
        pass

    @allure.step('允许debug模式')
    def enable_debug(self):
        pass

    @allure.step('重启话机')
    def reboot(self):
        pass

    @allure.step('执行恢复出厂')
    def factory(self):
        pass

    @allure.step('跳过rom版本检查')
    def skip_rom_check(self):
        pass

    @allure.step('执行ap')
    def auto_provision(self):
        pass

    @allure.step('make call')
    def call(self, aim_ip):
        pass

    @allure.step('执行按键')
    def send_key(self, key_code):
        pass

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
    def save_screen(self,src_dir):
        pass

    @allure.step('保存log文件')
    def save_log(self,src_dir):
        pass

    @allure.step('保存配置文件')
    def save_cfg(self,src_dir,cfg_type='xml'):
        pass




if __name__ == '__main__':
    A = VoipDevice('10.3.3.116', 5060)
