from HtekLib.SipMessage import SipMessage


class SipCall(SipMessage):
    # send message
    def answer(self):
        pass

    def reject(self):
        pass

    def cancel(self):
        pass

    def end_call(self):
        pass

    # receive message
    def receive(self, method):
        pass

    def send_100(self):
        pass
