class SipServer:
    def __init__(self):
        self.host_ip = None
        self.host_port = None

    def start(self):
        self.select_thread()

    def stop(self):
        pass

    def send(self):
        print(self.host_ip)
        # pass

    def receive(self):
        pass

    def select_thread(self):
        pass


class Server3cx(SipServer):
    def __init__(self,host_ip,host_port):
        super().__init__()
        self.host_ip = host_ip
        self.host_port = host_port

    def select_thread(self):
        print('self')



if __name__ =='__main__':
    server=Server3cx('10.3.3.49', 5061)
    server.start()