import queue
import select
import socket
import time
from threading import Thread

from HtekLib.SipCall import SipCall
from HtekLib.SipMessage import SipMessage
from HtekLib.SipUitls import return_sip_method
from HtekLib.VoipDevice import VoipDevice


class SipServer:
    def __init__(self, host_ip, host_port, device: VoipDevice):
        self.host_ip = host_ip
        self.host_port = host_port
        self.dut_ip = device.ip
        self.dut_port = device.port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 进行socket配置，使其支持端口复用，否则发送方绑定5066，则无法使用该端口进行接收
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(True)
        self.socket.bind((host_ip, host_port))
        self.rev_message_que = queue.Queue()

    def start(self):
        thread = Thread(target=self.select_thread())
        # 设置成守护线程
        thread.setDaemon(True)
        # 启动线程
        thread.start()

    def stop(self):
        pass

    def make_call(self,call_type=1):
        return SipCall()

    def receive_call(self,call_type=0):
        return self._rev_message('INVITE')

    def _rev_message(self, method, time_out=5):
        time.sleep(0.5)
        time_flag = int(time.time())
        while 1:
            if self.rev_message_que.empty() is False:
                message = self.rev_message_que.get()
                print('从队列中取出【%s】消息' % message.message_type)
                if message.message_type == method:
                    print('[ %s ]消息为我所期待' % message.message_type)
                    break
                else:
                    print('[ %s ]消息 舍弃' % message.message_type)
                # 超时退出 默认5s
                if (int(time.time()) - time_flag) > time_out:
                    assert False
        if method == 'INVITE':
            return SipCall(message.buf,call_type=0)
        else:
            return message


    def select_thread(self):
        s_input = [self.socket, ]
        s_output = []
        while True:
            readable, writeable, exeptional = select.select(s_input, s_output, s_input)
            # 读取数据
            for s in readable:  # 每个s就是一个socket
                if s is self.socket:
                    # 接受信息,判断模式，如果为空就放弃，否则解析消息
                    buf, (dut_ip, dut_port) = s.recvfrom(1500)
                    # 如果不是目标设备，跳过此包
                    if (dut_ip != self.dut_ip) | (dut_port != self.dut_port):
                        break
                    print('++++ rev %s message from %s:%s' % (buf, dut_ip, dut_port))
                    # 粗解包，使目标包进入流程，其他包舍弃
                    method = return_sip_method(buf)  # 这里的method 可能是\r\n\r\n 空消息
                    if method == '\\r\\n\\r\\n':
                        pass
                    elif method in ['INVITE', '100', '180', '200', '486', 'BYE', '302', 'ACK', 'REFER', 'CANCEL']:
                        message = SipMessage(buf)
                        self.rev_message_que.put(message)


class Server3cx(SipServer):
    def select_thread(self):
        print('self')




if __name__ == '__main__':
    server = Server3cx('10.3.3.49', 5061)
    server.start()
