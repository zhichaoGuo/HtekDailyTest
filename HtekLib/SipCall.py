from HtekLib.SipMessage import SipMessage


class SipCall:
    def __init__(self, sip_message: SipMessage, sip_server, call_type):
        self.message = sip_message
        self.server = sip_server
        self.call_type = call_type  # 0 incoming call  1 outgoing call

    # send message
    def answer(self):
        self.server.send_str(self.message.build_response('200_invite'))

    def reject(self):
        pass

    def cancel(self):
        pass

    def end_call(self):
        self.server.send_str(self.message.build_request('BYE',self.call_type))

    # receive message
    def receive(self, method):
        pass

    def send_100(self):
        pass
