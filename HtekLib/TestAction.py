from with_pytest.HtekLib.SipServer import Server3cx
from with_pytest.HtekLib.VoipDevice import VoipDevice


def wait_phone_up(phone: VoipDevice):
    pass


def start_sip_server(host_ip, host_port, server_type='3cx'):
    if server_type =='3cx':
        server = Server3cx(host_ip,host_port)
        server.start()
    return server
