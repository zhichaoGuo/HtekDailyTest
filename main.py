from HtekLib.SipServer import Server3cx
from HtekLib.VoipDevice import VoipDevice

if __name__ == '__main__':
    DUT = VoipDevice('10.3.3.116', 5069, 80, 'admin', 'admin')
    print(1)
    # 再实例化sip服务将设备传入
    server = Server3cx('10.3.3.49', 5061, DUT)
    print(2)
    # 启动设备
    server.start()
    print(3)
    # DUT call SERVER, S answer, S end call
    DUT.call('1501')
    call_0 = server.receive_call()
    call_0.answer()
    call_0.end_call()
