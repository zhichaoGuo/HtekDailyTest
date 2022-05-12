import sys
sys.path.append('E:\\pythonProject\\HtekDailyTest')
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from random import random

import allure
import pytest as pytest
import yaml

from TestLib.DeviceAction import *
from TestLib.VoipDevice import VoipDevice


@allure.feature("升级测试套件")
class TestApUpgrade:
    f = yaml.safe_load(open("upgrade_url.yml", encoding='utf-8'))

    @pytest.mark.fw520M
    @pytest.mark.parametrize('dut', [f["DUT"][0]])
    @pytest.mark.parametrize('rom_version', f["rom_version"],ids=[str(f["rom_version"])[-6:-2]])
    @pytest.mark.parametrize('assist_rom_version', f["assist_rom_version"],ids=[str(f["assist_rom_version"])[-6:-2]])
    @pytest.mark.parametrize('url', f["url"])
    @allure.story("升降级测试用例")
    def test_520M(self, dut, rom_version, assist_rom_version, url):
        print('DUT is %s:%s %s:%s' % (dut[0], dut[1], dut[2], dut[3]))
        print('rom_version :%s' % rom_version)
        print('assist_rom_version :%s' % assist_rom_version)
        print(url)
        sleep_time = 30
        for r in url:
            if 'tftp' in r:
                sleep_time = 60
        DUT = VoipDevice(dut[0], dut[1], dut[2], dut[3])
        print('set DUT')
        DUT.set_rom_path(url[0])
        print('set rom path')
        print(DUT.get_version())
        if DUT.get_version() != rom_version:
            auto_provision(DUT)
            sleep_phone_down(DUT)
            time.sleep(sleep_time)
        sleep_phone_up(DUT)
        print(type(DUT.get_version()))

        print(rom_version)
        print(type(rom_version))
        assert DUT.get_version() == rom_version
        DUT.set_rom_path(url[1])
        auto_provision(DUT)
        sleep_phone_down(DUT)
        time.sleep(sleep_time)
        sleep_phone_up(DUT)
        assert DUT.get_version() == assist_rom_version

    @pytest.mark.fw520U
    @pytest.mark.parametrize('dut', [f["DUT"][1]])
    @pytest.mark.parametrize('rom_version', f["rom_version"], ids=[str(f["rom_version"])[-6:-2]])
    @pytest.mark.parametrize('assist_rom_version', f["assist_rom_version"], ids=[str(f["assist_rom_version"])[-6:-2]])
    @pytest.mark.parametrize('url', f["url"])
    @allure.story("升降级测试用例")
    def test_520U(self, dut, rom_version, assist_rom_version, url):
        print('DUT is %s:%s %s:%s' % (dut[0], dut[1], dut[2], dut[3]))
        print('rom_version :%s' % rom_version)
        print('assist_rom_version :%s' % assist_rom_version)
        print(url)
        sleep_time = 450
        for r in url:
            if 'tftp' in r:
                sleep_time = 550
        time.sleep(random())
        DUT = VoipDevice(dut[0], dut[1], dut[2], dut[3])
        DUT.set_rom_path(url[0])
        auto_provision(DUT)
        time.sleep(sleep_time)
        sleep_phone_up(DUT)
        assert DUT.get_version() == rom_version
        DUT.set_rom_path(url[1])
        auto_provision(DUT)
        time.sleep(sleep_time)
        sleep_phone_up(DUT)
        assert DUT.get_version() == assist_rom_version

    @pytest.mark.fw920U
    @pytest.mark.parametrize('dut', [f["DUT"][2]])
    @pytest.mark.parametrize('rom_version', f["rom_version"], ids=[str(f["rom_version"])[-6:-2]])
    @pytest.mark.parametrize('assist_rom_version', f["assist_rom_version"], ids=[str(f["assist_rom_version"])[-6:-2]])
    @pytest.mark.parametrize('url', f["url"])
    @allure.story("升降级测试用例")
    def test_920U(self, dut, rom_version, assist_rom_version, url):
        print('DUT is %s:%s %s:%s' % (dut[0], dut[1], dut[2], dut[3]))
        print('rom_version :%s' % rom_version)
        print('assist_rom_version :%s' % assist_rom_version)
        print(url)
        sleep_time = 450
        for r in url:
            if 'tftp' in r:
                sleep_time = 550
        time.sleep(random())
        DUT = VoipDevice(dut[0], dut[1], dut[2], dut[3])
        DUT.set_rom_path(url[0])
        auto_provision(DUT)
        time.sleep(sleep_time)
        sleep_phone_up(DUT)
        assert DUT.get_version() == rom_version
        DUT.set_rom_path(url[1])
        auto_provision(DUT)
        time.sleep(sleep_time)
        sleep_phone_up(DUT)
        assert DUT.get_version() == assist_rom_version

    @pytest.mark.fw920M
    @pytest.mark.parametrize('dut', [f["DUT"][3]])
    @pytest.mark.parametrize('rom_version', f["rom_version"], ids=[str(f["rom_version"])[-6:-2]])
    @pytest.mark.parametrize('assist_rom_version', f["assist_rom_version"], ids=[str(f["assist_rom_version"])[-6:-2]])
    @pytest.mark.parametrize('url', f["url"])
    @allure.story("升降级测试用例")
    def test_920M(self, dut, rom_version, assist_rom_version, url):
        print('DUT is %s:%s %s:%s' % (dut[0], dut[1], dut[2], dut[3]))
        print('rom_version :%s' % rom_version)
        print('assist_rom_version :%s' % assist_rom_version)
        print(url)
        sleep_time = 450
        for r in url:
            if 'tftp' in r:
                sleep_time = 550
        time.sleep(random())
        DUT = VoipDevice(dut[0], dut[1], dut[2], dut[3])
        DUT.set_rom_path(url[0])
        auto_provision(DUT)
        time.sleep(sleep_time)
        sleep_phone_up(DUT)
        assert DUT.get_version() == rom_version
        DUT.set_rom_path(url[1])
        auto_provision(DUT)
        time.sleep(sleep_time)
        sleep_phone_up(DUT)
        assert DUT.get_version() == assist_rom_version

    @pytest.mark.fw910M
    @pytest.mark.parametrize('dut', [f["DUT"][4]])
    @pytest.mark.parametrize('rom_version', f["rom_version"], ids=[str(f["rom_version"])[-6:-2]])
    @pytest.mark.parametrize('assist_rom_version', f["assist_rom_version"], ids=[str(f["assist_rom_version"])[-6:-2]])
    @pytest.mark.parametrize('url', f["url"])
    @allure.story("升降级测试用例")
    def test_910M(self, dut, rom_version, assist_rom_version, url):
        print('DUT is %s:%s %s:%s' % (dut[0], dut[1], dut[2], dut[3]))
        print('rom_version :%s' % rom_version)
        print('assist_rom_version :%s' % assist_rom_version)
        print(url)
        sleep_time = 350
        for r in url:
            if 'tftp' in r:
                sleep_time = 500
        time.sleep(random())
        DUT = VoipDevice(dut[0], dut[1], dut[2], dut[3])
        DUT.set_rom_path(url[0])
        auto_provision(DUT)
        time.sleep(sleep_time)
        sleep_phone_up(DUT)
        assert DUT.get_version() == rom_version
        DUT.set_rom_path(url[1])
        auto_provision(DUT)
        time.sleep(sleep_time)
        sleep_phone_up(DUT)
        assert DUT.get_version() == assist_rom_version

def exec_test(name: list):
    with ThreadPoolExecutor(max_workers=4) as p:
        for man in name:
            p.submit(worker, man)
    print('Finished')


def worker():
    pytest.main(['-s', '-v', '.\\TestUpgrade.py'])


if __name__ == '__main__':

    pytest.main(['-s', '-v', '–alluredir', 'E:\\pythonProject\\HtekDailyTest\\TestTask\\report\\result1', '.\\TestUpgrade.py'])
    p1 = 'pytest -s -v .\TestUpgrade.py --alluredir E:\\pythonProject\\HtekDailyTest\\TestTask\\report\\result1'
    t1 = 'allure generate E:\pythonProject\HtekDailyTest\TestTask\report\result1 - o E:\pythonProject\HtekDailyTest\TestTask\dut1 - -clean'
