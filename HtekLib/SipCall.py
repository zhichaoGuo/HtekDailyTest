from HtekLib.SipMessage import SipMessage


class SipCall:
    def __init__(self,sip_message:SipMessage,sip_server):
        self.message = sip_message
        self.server = sip_server
    # send message
    def answer(self):
        str = self.message.build_response('200_invite')
        self.server.send_str(str)

    def reject(self):
        pass

    def cancel(self):
        pass

    def end_call(self):
        str = self.message.build_request('BYE')
        self.server.send_str(str)

    # receive message
    def receive(self, method):
        pass

    def send_100(self):
        pass
