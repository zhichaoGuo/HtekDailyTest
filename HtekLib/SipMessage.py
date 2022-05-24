import re
import time
from string import Template


from HtekLib.SipUitls import return_sip_method, gen_tag
from HtekLib.VoipDevice import VoipDevice

buf_100 = Template(
    "SIP/2.0 100 Trying\r\n" +
    "Via: SIP/2.0/UDP $dut_ip:$dut_port;branch=$branch\r\n" +
    "To: <sip:$server_account@$server_ip:$server_port>\r\n" +
    "From: <sip:$dut_account@$server_ip:$server_port>;tag=$from_tag;epid=$from_epid\r\n" +
    "Call-ID: $call_id\r\n" +
    "CSeq: $cseq_num $cseq_method\r\n" +
    "Content-Length: $content_len\r\n\r\n"
)
buf_180 = Template(
    "SIP/2.0 180 Ringing\r\n" +
    "Via: SIP/2.0/UDP $dut_ip:$dut_port;branch=$branch\r\n" +
    "Contact: <sip:$server_account@$server_ip:$server_port>\r\n" +
    "To: <sip:$server_account@$server_ip:$server_port>;tag=$to_tag\r\n" +
    "From: <sip:$dut_account@$server_ip:$server_port>;tag=$from_tag;epid=$from_epid\r\n" +
    "Call-ID: $call_id\r\n" +
    "CSeq: $cseq_num $cseq_method\r\n" +
    "User-Agent: Htek Abyss\r\n" +
    "Content-Length: $content_len\r\n\r\n"
)
buf_200_invite = Template(
    "SIP/2.0 200 OK\r\n" +
    "Via: SIP/2.0/UDP $dut_ip:$dut_port;branch=$branch\r\n" +
    "Contact: <sip:$server_account@$server_ip:$server_port>\r\n" +
    "To: <sip:$server_account@$server_ip:$server_port>;tag=$to_tag\r\n" +
    "From: <sip:$dut_account@$server_ip:$server_port>;tag=$from_tag;epid=$from_epid\r\n" +
    "Call-ID: $call_id\r\n" +
    "CSeq: $cseq_num $cseq_method\r\n" +
    "Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REGISTER, SUBSCRIBE, NOTIFY, REFER, INFO, MESSAGE, UPDATE\r\n"
    "Content-Type: $content_type\r\n" +
    "Supported: replaces, timer\r\n" +
    "User-Agent: Htek Abyss\r\n" +
    "Content-Length: $content_len\r\n\r\n" +
    "$body"
)
buf_100_hold = Template(
    "SIP/2.0 100 Trying\r\n" +
    "Via: SIP/2.0/UDP $dut_ip:$dut_port;branch=$branch\r\n" +
    "To: <sip:$server_account@$server_ip:$server_port>;tag=$to_tag\r\n" +
    "From: <sip:$dut_account@$server_ip:$server_port>;tag=$from_tag;epid=$from_epid\r\n" +
    "Call-ID: $call_id\r\n" +
    "CSeq: $cseq_num $cseq_method\r\n" +
    "Content-Length: $content_len\r\n\r\n"
)
buf_200_hold = Template(
    "SIP/2.0 200 OK\r\n" +
    "Via: SIP/2.0/UDP $dut_ip:$dut_port;branch=$branch\r\n" +
    "Contact: <sip:$server_account@$server_ip:$server_port>\r\n" +
    "To: <sip:$server_account@$server_ip:$server_port>;tag=$to_tag\r\n" +
    "From: <sip:$dut_account@$server_ip:$server_port>;tag=$from_tag;epid=$from_epid\r\n" +
    "Call-ID: $call_id\r\n" +
    "CSeq: $cseq_num INVITE\r\n" +
    "Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REGISTER, SUBSCRIBE, NOTIFY, REFER, INFO, MESSAGE, UPDATE\r\n"
    "Content-Type: $content_type\r\n" +
    "Supported: replaces, timer\r\n" +
    "User-Agent: Htek Abyss\r\n" +
    "Content-Length: $content_len\r\n\r\n" +
    "$body"
)
buf_200_register = Template(
    "SIP/2.0 200 OK\r\n" +
    "Via: SIP/2.0/UDP $dut_ip:$dut_port;branch=$branch\r\n" +
    "Contact: <sip:$dut_account@$dut_ip:$dut_port;transport=UDP>;expires=900\r\n" +
    "To: <sip:$dut_account@$server_ip:$server_port>;tag=$to_tag\r\n" +
    "From: <sip:$dut_account@$server_ip:$server_port>;tag=$from_tag;epid=$from_epid\r\n" +
    "Call-ID: $call_id\r\n" +
    "CSeq: $cseq_num REGISTER\r\n" +
    "User-Agent: Htek Abyss\r\n" +
    "Content-Length: 0\r\n\r\n"
)
buf_100_resume = Template(
    "SIP/2.0 100 Trying\r\n" +
    "Via: SIP/2.0/UDP $dut_ip:$dut_port;branch=$branch\r\n" +
    "To: <sip:$server_account@$server_ip:$server_port>;tag=$to_tag\r\n" +
    "From: <sip:$dut_account@$server_ip:$server_port>;tag=$from_tag;epid=$from_epid\r\n" +
    "Call-ID: $call_id\r\n" +
    "CSeq: $cseq_num INVITE\r\n" +
    "Content-Length: 0\r\n\r\n"
)
buf_200_resume = Template(
    "SIP/2.0 200 OK\r\n" +
    "Via: SIP/2.0/UDP $dut_ip:$dut_port;branch=$branch\r\n" +
    "Contact: <sip:$server_account@$server_ip:$server_port>\r\n" +
    "To: <sip:$server_account@$server_ip:$server_port>;tag=$to_tag\r\n" +
    "From: <sip:$dut_account@$server_ip:$server_port>;tag=$from_tag;epid=$from_epid\r\n" +
    "Call-ID: $call_id\r\n" +
    "CSeq: $cseq_num $cseq_method\r\n" +
    "Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REGISTER, SUBSCRIBE, NOTIFY, REFER, INFO, MESSAGE, UPDATE\r\n"
    "Content-Type: $content_type\r\n" +
    "Supported: replaces, timer\r\n" +
    "User-Agent: Htek Abyss\r\n" +
    "Content-Length: $content_len\r\n\r\n" +
    "$body"
)
buf_407 = Template(
    "SIP/2.0 407 Proxy Authentication Required\r\n" +
    "Via: SIP/2.0/UDP $dut_ip:$dut_port;branch=$branch\r\n" +
    'Proxy-Authenticate: Digest nonce="414d535c189d033824:3d732dcb3559ca71bc7daa6e1073df94",algorithm=MD5,realm="3CXPhoneSystem"\r\n' +
    "To: <sip:$dut_account@$server_ip:$server_port>;tag=$to_tag\r\n" +
    "From: <sip:$dut_account@$server_ip:$server_port>;tag=$from_tag;epid=$from_epid\r\n" +
    "Call-ID: $call_id\r\n" +
    "CSeq: $cseq_num REGISTER\r\n" +
    "Content-Length: 0\r\n\r\n"
)

buf_bye = Template(
    "BYE sip:$dut_account@$dut_ip:$dut_port;transport=UDP SIP/2.0\r\n" +
    "Via: SIP/2.0/UDP $server_ip:$server_port;branch=$branch;rport\r\n" +
    "Max-Forwards: $max_forwards\r\n" +
    "Contact: <sip:$server_account@$server_ip:$server_port>\r\n" +
    "To: <sip:$to_account@$server_ip:$server_port>;tag=$to_tag;epid=DP20462d\r\n" +
    "From: <sip:$from_account@$server_ip:$server_port>;tag=$from_tag\r\n" +
    "Call-ID: $call_id\r\n" +
    "CSeq: $cseq_num BYE\r\n" +
    "User-Agent: Htek Abyss\r\n" +
    "Content-Length: $content_len\r\n\r\n"
)
buf_ack = Template(
    "ACK sip:$dut_account@$server_ip:$server_port SIP/2.0\r\n" +
    "Via: SIP/2.0/UDP 10.3.2.75:5060;branch=z9hG4bK230970982\r\n" +
    "From: <sip:1504@192.168.0.68:5060>;tag=3627258a66f4aaf;epid=DP20462d\r\n" +
    "To: <sip:1503@192.168.0.68:5060>;tag=4032133d\r\n" +
    "Call-ID: 5d5ba82985cd78e@10.3.2.75\r\n" +
    "CSeq: 21 ACK\r\n" +
    "Contact: <sip:1504@10.3.2.75:5060;transport=UDP>\r\n" +
    "Max-Forwards: 70\r\n" +
    "User-Agent: Htek Abyss\r\n" +
    "Content-Length: $content_len\r\n\r\n"
)


class SipMessage:
    def __init__(self, buf: bytes):
        """
        将sip buf传入解析sip头
        :param buf:
        """
        self.buf = buf
        # 带body
        if buf.find(b'\r\n\r\n') != -1:
            buf_str = str(buf)[2:-1]
            header_list = buf_str.split('\\r\\n\\r\\n')[0].split('\\r\\n')[1:]
            body = buf_str.split('\\r\\n\\r\\n')[1]
        else:
            # 未带body
            buf_str = str(buf)[2:-1]
            # 去除method行分割为list
            header_list = buf_str.split('\\r\\n')[1:]
            body = ''
        try:
            for i in range(len(header_list)):
                # 跳过分割产生的空行
                if header_list[i] != '':
                    # 查找行模式：Via\From\To\Call-Id
                    line_method = header_list[i].split(': ')[0]
                    line_value = header_list[i].split(': ')[1]
                    # 在Via中匹配branch
                    # print(line_method + ':')
                    if line_method == 'Via':
                        self.Via = Via(line_value)
                    elif line_method == 'Contact':
                        self.Contact = Contact(line_value)
                    elif line_method == 'Proxy-Authorization':
                        self.ProxyAuth = ProxyAuth(line_value)
                    elif line_method == 'Max-Forwards':
                        self.MaxForwards = MaxForwards(line_value)
                    elif line_method == 'To':
                        self.To = To(line_value)
                    elif line_method == 'From':
                        self.From = From(line_value)
                    elif line_method == 'Call-ID':
                        self.CallId = CallId(line_value)
                    elif line_method == 'CSeq':
                        self.CSeq = CSeq(line_value)
                    elif line_method == 'Allow':
                        self.Allow = Allow(line_value)
                    elif line_method == 'Allow-Events':
                        self.AllowEvents = AllowEvents(line_value)
                    elif line_method == 'User-Agent':
                        self.UserAgent = UserAgent(line_value)
                    elif line_method == 'Supported':
                        self.Supported = Supported(line_value)
                    elif line_method == 'Subject':
                        self.Subject = Subject(line_value)
                    elif line_method == 'Expires':
                        self.Expires = Expires(line_value)
                    elif line_method == 'Event':
                        self.Event = Event(line_value)
                    elif line_method == 'Accept':
                        self.Accept = Accept(line_value)
                    elif line_method == 'Content-Length':
                        self.ContentLength = ContentLength(line_value)
                    elif line_method == 'Content-Type':
                        self.ContentType = ContentType(line_value)
                    # elif line_method == 'Contact':
                    #     self.Contact = Contact(line_value)
        except:
            pass
        # 都转完了之后，开始设置定义的type：incoming call,hold,resume,200_bye,200_cancel
        self.status_line = buf_str.split('\\r\\n')[0]
        if return_sip_method(self.status_line) == 'INVITE':
            if body.find('a=sendonly') != -1:
                self.message_type = 'hold'
            elif hasattr(self, 'Subject') is False:
                self.message_type = 'resume'
            else:
                self.message_type = 'INVITE'
        else:
            self.message_type = return_sip_method(self.status_line)

    def build_request(self, method):
        # 使用此方法生成request请求，如INVITE，HOLD,RESUME,BYE，CANCEL，ACK
        if method == 'BYE':
            return buf_bye.substitute()

    def build_response(self, method):
        # 使用此方法生成response回应，如100,180,200
        if method == '100':
            return buf_100.substitute(dut_ip=self.Via.ip,
                                      dut_port=self.Via.port,
                                      branch=self.Via.branch,
                                      server_account=self.To.account,
                                      server_ip=self.To.ip,
                                      server_port=self.To.port,
                                      dut_account=self.From.account,
                                      from_tag=self.From.tag,
                                      from_epid=self.From.epid,
                                      call_id=self.CallId.callid,
                                      cseq_num=self.CSeq.cseq_num,
                                      cseq_method=self.CSeq.cseq_method,
                                      content_len='0')
        if method == '100_hold':
            return buf_100_hold.substitute(dut_ip=self.Via.ip,
                                           dut_port=self.Via.port,
                                           branch=self.Via.branch,
                                           server_account=self.To.account,
                                           server_ip=self.To.ip,
                                           server_port=self.To.port,
                                           dut_account=self.From.account,
                                           to_tag=self.To.tag,
                                           from_tag=self.From.tag,
                                           from_epid=self.From.epid,
                                           call_id=self.CallId.callid,
                                           cseq_num=self.CSeq.cseq_num,
                                           cseq_method=self.CSeq.cseq_method,
                                           content_len='0')
        if method == '180':
            return buf_180.substitute(dut_ip=self.Via.ip,
                                      dut_port=self.Via.port,
                                      branch=self.Via.branch,
                                      server_account=self.To.account,
                                      server_ip=self.To.ip,
                                      server_port=self.To.port,
                                      dut_account=self.From.account,
                                      to_tag=self.To.tag,
                                      from_tag=self.From.tag,
                                      from_epid=self.From.epid,
                                      call_id=self.CallId.callid,
                                      cseq_num=self.CSeq.cseq_num,
                                      cseq_method=self.CSeq.cseq_method,
                                      content_len='0')
        if method == '200_invite':
            body = "v=0\r\n" \
                   f"o=3cxPS 458269655040 527375007745 IN IP4 {self.To.ip}\r\n" \
                   "s=3cxPS Audio call\r\n" \
                   f"c=IN IP4 {self.To.ip}\r\n" \
                   "t=0 0\r\n" \
                   "m=audio 12100 RTP/AVP 0 101\r\n" \
                   "a=rtpmap:0 PCMU/8000\r\n" \
                   "a=ptime:20\r\n" \
                   "a=rtpmap:101 telephone-event/8000\r\n" \
                   "a=fmtp:101 0-11,16\r\n" \
                   "a=sendrecv\r\n"

            return buf_200_invite.substitute(dut_ip=self.Via.ip,
                                             dut_port=self.Via.port,
                                             branch=self.Via.branch,
                                             server_account=self.To.account,
                                             server_ip=self.To.ip,
                                             server_port=self.To.port,
                                             dut_account=self.From.account,
                                             to_tag=self.To.tag,
                                             from_tag=self.From.tag,
                                             from_epid=self.From.epid,
                                             call_id=self.CallId.callid,
                                             cseq_num=self.CSeq.cseq_num,
                                             cseq_method=self.CSeq.cseq_method,
                                             content_type=self.ContentType.content_type,
                                             content_len=len(body),
                                             body=body)
        if method == '200_hold':
            body = 'v=0\r\n' \
                   f'o=3cxPS 165658230784 12935233537 IN IP4 {self.To.ip}\r\n' \
                   's=3cxPS Audio call\r\n' \
                   f'c=IN IP4 {self.To.ip}\r\n' \
                   't=0 0\r\n' \
                   'm=audio 7560 RTP/AVP 0 8 9 120 101\r\n' \
                   'a=rtpmap:0 PCMU/8000\r\n' \
                   'a=rtpmap:8 PCMA/8000\r\n' \
                   'a=rtpmap:9 G722/8000\r\n' \
                   'a=rtpmap:120 opus/48000/2\r\n' \
                   'a=fmtp:120 useinbandfec=1; usedtx=1; maxaveragebitrate=64000\r\n' \
                   'a=rtpmap:101 telephone-event/8000\r\n' \
                   'a=recvonly\r\n'
            return buf_200_hold.substitute(dut_ip=self.Via.ip,
                                           dut_port=self.Via.port,
                                           branch=self.Via.branch,
                                           server_account=self.To.account,
                                           server_ip=self.To.ip,
                                           server_port=self.To.port,
                                           dut_account=self.From.account,
                                           to_tag=self.To.tag,
                                           from_tag=self.From.tag,
                                           from_epid=self.From.epid,
                                           call_id=self.CallId.callid,
                                           cseq_num=self.CSeq.cseq_num,
                                           cseq_method=self.CSeq.cseq_method,
                                           content_type=self.ContentType.content_type,
                                           content_len=len(body),
                                           body=body)
        if method == '200_resume':
            body = 'v=0\r\n' \
                   f'o=3cxPS 458269655040 527375007746 IN IP4 {self.To.ip}\r\n' \
                   's=3cxPS Audio call\r\n' \
                   f'c=IN IP4 {self.To.ip}\r\n' \
                   't=0 0\r\n' \
                   'm=audio 12100 RTP/AVP 0 101\r\n' \
                   'a=rtpmap:0 PCMU/8000\r\n' \
                   'a=ptime:20\r\n' \
                   'a=rtpmap:101 telephone-event/8000\r\n' \
                   'a=fmtp:101 0-11,16\r\n' \
                   'a=sendrecv\r\n'
            return buf_200_resume.substitute(dut_ip=self.Via.ip,
                                             dut_port=self.Via.port,
                                             branch=self.Via.branch,
                                             server_account=self.To.account,
                                             server_ip=self.To.ip,
                                             server_port=self.To.port,
                                             dut_account=self.From.account,
                                             to_tag=self.To.tag,
                                             from_tag=self.From.tag,
                                             from_epid=self.From.epid,
                                             call_id=self.CallId.callid,
                                             cseq_num=self.CSeq.cseq_num,
                                             cseq_method=self.CSeq.cseq_method,
                                             content_type=self.ContentType.content_type,
                                             content_len=len(body),
                                             body=body)
        if method == '200_register':
            return buf_200_register.substitute(dut_ip=self.Via.ip,
                                               dut_port=self.Via.port,
                                               branch=self.Via.branch,
                                               server_account=self.To.account,
                                               server_ip=self.To.ip,
                                               server_port=self.To.port,
                                               dut_account=self.From.account,
                                               to_tag=self.To.tag,
                                               from_tag=self.From.tag,
                                               from_epid=self.From.epid,
                                               call_id=self.CallId.callid,
                                               cseq_num=self.CSeq.cseq_num)
        if method == '407':
            return buf_407.substitute(dut_ip=self.Via.ip,
                                      dut_port=self.Via.port,
                                      branch=self.Via.branch,
                                      server_account=self.To.account,
                                      server_ip=self.To.ip,
                                      server_port=self.To.port,
                                      dut_account=self.From.account,
                                      to_tag=gen_tag(),
                                      from_tag=self.From.tag,
                                      from_epid=self.From.epid,
                                      call_id=self.CallId.callid,
                                      cseq_num=self.CSeq.cseq_num)


class SipHeader:
    def __init__(self, text):
        self.text = text
        # print(buf)

    def __str__(self):
        return self.text


class Via(SipHeader):
    def __init__(self, buf: str):
        super().__init__(buf)
        try:
            # Via: SIP/2.0/UDP 192.168.0.68:5060;branch=z9hG4bK-524287-1---7b14111db5268839;rport
            re_via = (r'SIP/2.0/UDP (?P<ip>.+):(?P<port>.+);branch=(?P<branch>.+);rport')
            self.ip = re.search(re_via, self.text.strip(), re.U).groupdict()['ip']
            self.port = re.search(re_via, self.text.strip(), re.U).groupdict()['port']
            self.branch = re.search(re_via, self.text.strip(), re.U).groupdict()['branch']
        except:
            try:
                # Via: SIP/2.0/UDP 10.3.2.75:5060;branch=z9hG4bKae00a9bb
                re_via = (r'SIP/2.0/UDP (?P<ip>.+):(?P<port>.+);branch=(?P<branch>.+)')
                self.ip = re.search(re_via, self.text.strip(), re.U).groupdict()['ip']
                self.port = re.search(re_via, self.text.strip(), re.U).groupdict()['port']
                self.branch = re.search(re_via, self.text.strip(), re.U).groupdict()['branch']
            except:
                print('Parser Via ERR!!')
                self.ip = ''
                self.port = ''
                self.branch = ''


class Contact(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        try:
            # Contact: <sip:1503@10.3.3.116:5069;transport=UDP>;expires=900
            re_via = (r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>.+);transport=UDP>;expires=(?P<expires>.+)')
            self.account = re.search(re_via, self.text.strip(), re.U).groupdict()['account']
            self.ip = re.search(re_via, self.text.strip(), re.U).groupdict()['ip']
            self.port = re.search(re_via, self.text.strip(), re.U).groupdict()['port']
            self.expires = re.search(re_via, self.text.strip(), re.U).groupdict()['expires']
        except:
            try:
                # Contact: <sip:1504@10.3.2.75:5060;transport=UDP>
                re_via = (r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>.+);transport=UDP')
                self.account = re.search(re_via, self.text.strip(), re.U).groupdict()['account']
                self.ip = re.search(re_via, self.text.strip(), re.U).groupdict()['ip']
                self.port = re.search(re_via, self.text.strip(), re.U).groupdict()['port']
            except:
                try:
                    # Contact: <sip:1503@192.168.0.68:5060>
                    re_via = (r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>.+)>')
                    self.account = re.search(re_via, self.text.strip(), re.U).groupdict()['account']
                    self.ip = re.search(re_via, self.text.strip(), re.U).groupdict()['ip']
                    self.port = re.search(re_via, self.text.strip(), re.U).groupdict()['port']
                except:
                    print('Parser Contact ERR!!')
                    self.account = ''
                    self.ip = ''
                    self.port = ''


class ProxyAuth(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        # Proxy-Authorization: Digest username="1505", realm="3CXPhoneSystem",
        # nonce="414d535c189d033824:3d732dcb3559ca71bc7daa6e1073df94", uri="sip:192.168.0.68:5060",
        # response="dfaafa509306745676264b275b12e085", algorithm=MD5
        self.proxyauth = self.text
        self.proxy_dic = {}
        for i in buf.split(','):
            j = (i.strip().split('='))
            self.proxy_dic[j[0]] = j[1]


class MaxForwards(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        self.maxforwards = self.text


class To(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        try:
            # To: <sip:1503@192.168.0.68:5060>
            re_via = (r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>.+)>')
            self.account = re.search(re_via, self.text.strip(), re.U).groupdict()['account']
            self.ip = re.search(re_via, self.text.strip(), re.U).groupdict()['ip']
            self.port = re.search(re_via, self.text.strip(), re.U).groupdict()['port']
        except:
            try:
                # To: <sip:1503@192.168.0.68:5060>;tag=4032133d
                re_via = (r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>.+);tag=(?P<tag>.+)')
                self.account = re.search(re_via, self.text.strip(), re.U).groupdict()['account']
                self.ip = re.search(re_via, self.text.strip(), re.U).groupdict()['ip']
                self.port = re.search(re_via, self.text.strip(), re.U).groupdict()['port']
                self.tag = re.search(re_via, self.text.strip(), re.U).groupdict()['tag']
            except:
                print('Parser To ERR!!')
                self.account = ''
                self.ip = ''
                self.port = ''
        self.tag = 'htek20180905'


class From(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        try:
            # From: <sip:1504@192.168.0.68:5060>;tag=3627258a66f4aaf;epid=DP20462d
            re_via = (r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>.+)>;tag=(?P<tag>.+);epid=(?P<epid>.+)')
            self.account = re.search(re_via, self.text.strip(), re.U).groupdict()['account']
            self.ip = re.search(re_via, self.text.strip(), re.U).groupdict()['ip']
            self.port = re.search(re_via, self.text.strip(), re.U).groupdict()['port']
            self.tag = re.search(re_via, self.text.strip(), re.U).groupdict()['tag']
            self.epid = re.search(re_via, self.text.strip(), re.U).groupdict()['epid']
        except:
            try:
                # From: <sip:1503@192.168.0.68:5060>;tag=4032133d
                re_via = (r'<sip:(?P<account>.+)@(?P<ip>.+):(?P<port>.+);tag=(?P<tag>.+)')
                self.account = re.search(re_via, self.text.strip(), re.U).groupdict()['account']
                self.ip = re.search(re_via, self.text.strip(), re.U).groupdict()['ip']
                self.port = re.search(re_via, self.text.strip(), re.U).groupdict()['port']
                self.tag = re.search(re_via, self.text.strip(), re.U).groupdict()['tag']
            except:
                try:
                    # From: <sip:1500@10.3.2.242>;tag=1571e36d3692605;epid=DP1fa80e
                    re_via = (r'<sip:(?P<account>.+)@(?P<ip>.+);tag=(?P<tag>.+);epid=(?P<epid>.+)')
                    self.account = re.search(re_via, self.text.strip(), re.U).groupdict()['account']
                    self.ip = re.search(re_via, self.text.strip(), re.U).groupdict()['ip']
                    self.tag = re.search(re_via, self.text.strip(), re.U).groupdict()['tag']
                    self.epid = re.search(re_via, self.text.strip(), re.U).groupdict()['epid']
                except:
                    print('Parser From ERR!!')
                    self.account = ''
                    self.ip = ''
                    self.port = ''
                    self.tag = ''
                    self.epid = ''


class CallId(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        try:
            # Call-ID: 5d5ba82985cd78e@10.3.2.75
            self.callid = self.text
        except:
            print('Parser CallId ERR!!')
            self.callid = ''


class CSeq(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        try:
            # CSeq: 20 INVITE
            re_via = (r'(?P<cseq_num>.+) (?P<cseq_method>.+)')
            self.cseq_num = re.search(re_via, self.text.strip(), re.U).groupdict()['cseq_num']
            self.cseq_method = re.search(re_via, self.text.strip(), re.U).groupdict()['cseq_method']
        except:
            print('Parser CSeq ERR!!')
            self.cseq_num = ''
            self.cseq_method = ''


class Allow(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        try:
            # Allow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK
            self.allow = self.text
            self.allow_list = self.text.split(', ')
        except:
            print('Parser Allow ERR!!')
            self.allow = ''
            self.allow_list = ''


class AllowEvents(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        try:
            # Allow-Events: talk,hold,conference,refer,check-sync
            self.allow_events = self.text
            self.allow_events_list = self.text.split(',')
        except:
            print('Parser AllowEvents ERR!!')
            self.allow_events = ''
            self.allow_events_list = ''


class Supported(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        try:
            # Supported: replaces, timer
            self.supported = self.text
            self.supported_list = self.text.split(', ')
        except:
            print('Parser Supported ERR!!')
            self.supported = ''
            self.supported_list = ''


class Subject(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        # Subject: SIP Call
        self.subject = self.text


class UserAgent(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        # User-Agent: Htek UC902S V2.22.5.20.i 001fc120462d
        self.user_agent = self.text


class Expires(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        # Expires: 120
        self.expires = self.text


class Event(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)


class Accept(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)


class ContentLength(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        self.content_len = self.text


class ContentType(SipHeader):
    def __init__(self, buf):
        super().__init__(buf)
        self.content_type = self.text


if __name__ == '__main__':
    # buf = b'REGISTER sip:1501@10.3.2.242:5066 SIP/2.0\r\nVia: SIP/2.0/UDP 10.20.0.16:5060;branch=z9hG4bK1938747582\r\nFrom: <sip:1500@10.3.2.242>;tag=1571e36d3692605;epid=DP1fa80e\r\nTo: <sip:1501@10.3.2.242:5066>\r\nCall-ID: ab6e010ad2e7cf2@10.20.0.16\r\nCSeq: 20 INVITE\r\nContact: <sip:1500@10.20.0.16:5060;transport=UDP>\r\nMax-Forwards: 70\r\nUser-Agent: Htek UC924U V2.42.6.5.13 001fc11fa80e\r\nSupported: replaces\r\nSubject: SIP Call\r\nExpires: 120\r\nAllow-Events: talk,hold,conference,refer,check-sync\r\nAllow: INVITE, ACK, UPDATE, INFO, CANCEL, BYE, OPTIONS, REFER, SUBSCRIBE, NOTIFY, MESSAGE, PRACK\r\nContent-Type: application/sdp\r\nContent-Length: 423\r\n\r\nv=0\r\no=- 782 781 IN IP4 10.20.0.16\r\ns=SIP Call\r\nc=IN IP4 10.20.0.16\r\nt=0 0\r\nm=audio 12100 RTP/AVP 0 8 9 97 120 102 101\r\na=rtpmap:0 PCMU/8000\r\na=ptime:20\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:9 G722/8000\r\na=rtpmap:97 iLBC/8000\r\na=fmtp:97 mode=20\r\na=rtpmap:120 opus/48000/2\r\na=fmtp:120 useinbandfec=1; usedtx=1; maxaveragebitrate=64000\r\na=rtpmap:102 G726-32/8000\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:101 0-11,16\r\na=sendrecv\r\n'
    # message = SipMessage(buf)
    # print(message.build_response('200_resume'))
    from HtekLib.SipServer import Server3cx

