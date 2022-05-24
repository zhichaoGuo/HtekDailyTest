import time

from HtekLib.SipServer import Server3cx
from HtekLib.VoipDevice import VoipDevice

if __name__ == '__main__':
    DUT = VoipDevice('10.3.3.116', 5069, 80, 'admin', 'admin')
    # 再实例化sip服务将设备传入
    server = Server3cx('10.3.3.49', 5061, DUT)
    # 启动设备
    server.start()
    # DUT call SERVER, S answer, S end call
    server.rev_message('REGISTER',time_out=60)
    DUT.call('1501')
    call_0 = server.receive_call()
    call_0.answer()
    time.sleep(3)
    call_0.end_call()
