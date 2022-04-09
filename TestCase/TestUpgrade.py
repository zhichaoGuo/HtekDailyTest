import pytest as pytest
import yaml

from TestLib.DeviceAction import *
from TestLib.VoipDevice import VoipDevice


class TestApUpgrade:
    f = yaml.safe_load(open("demo.yml", encoding='utf-8'))

    @pytest.mark.parametrize('rom_version','assist_rom_version', [f["rom_version"],f["assist_rom_version"]])
    def test_ap_http(self, rom_version,assist_rom_version):
        DUT = VoipDevice('10.20.0.32', '5060', 'admin', 'admin')
        DUT.set_rom_path('http://10.3.3.49/fw/abyss/server1')
        auto_provision(DUT)
        sleep_phone_up(DUT)
        assert DUT.version() == rom_version
        DUT.set_rom_path('http://10.3.3.49/fw/abyss/server2')
        auto_provision(DUT)
        sleep_phone_up(DUT)
        assert DUT.version() == assist_rom_version

    @pytest.mark.parametrize('rom_version', 'assist_rom_version', [f["rom_version"], f["assist_rom_version"]])
    def test_ap_https(self, rom_version, assist_rom_version):
        DUT = VoipDevice('10.20.0.32', '5060', 'admin', 'admin')
        DUT.set_rom_path('https://10.3.3.49:8668/fw/abyss/server1')
        auto_provision(DUT)
        sleep_phone_up(DUT)
        assert DUT.version() == rom_version
        DUT.set_rom_path('https://10.3.3.49:8668/fw/abyss/server2')
        auto_provision(DUT)
        sleep_phone_up(DUT)
        assert DUT.version() == assist_rom_version