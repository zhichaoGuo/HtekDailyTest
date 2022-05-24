import pytest
import yaml

from HtekLib.SipServer import Server3cx
from HtekLib.VoipDevice import VoipDevice


class TestBaseCall:
    # f = yaml.safe_load(open("upgrade_url.yml", encoding='utf-8'))

    # @pytest.mark.parametrize('dut', [f["DUT"][0]])
    def test_DUTcallA_AanswerDUT(self):
        # 先实例化待测设备
        DUT = VoipDevice('10.3.3.116', 5069, 80, 'admin', 'admin')
        # 再实例化sip服务将设备传入
        server = Server3cx('10.3.3.49', 5061, DUT)
        # 启动设备
        server.start()
        # DUT call SERVER, S answer, S end call
        DUT.call('1501')
        call_0 = server.receive_call()
        call_0.answer()
        call_0.end_call()

        # # DUT call Server, s answer, DUT end call
        # DUT.call('1501')
        # call_0 = server.receive_call()
        # call_0.answer()
        # DUT.send_key('F4')
        #
        # # Server call DUT, DUT answer, DUT end call
        # call_1 = server.make_call('1503')
        # call_1.receive('100')
        # call_1.receive('180')
        # DUT.send_key('F1')
        # call_1.receive('200_invite')
        # DUT.send_key('F4')
        # call_1.receive('BYE')
        #
        # # Server call DUT, DUT answer, Server end call
        # call_1 = server.make_call('1503')
        # call_1.receive('100')
        # call_1.receive('180')
        # DUT.send_key('F1')
        # call_1.receive('200_invite')
        # call_1.end_call()

