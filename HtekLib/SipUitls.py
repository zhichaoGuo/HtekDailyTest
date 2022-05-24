import uuid


def return_sip_method(buf):
    """
    输入sip消息，如果是request 返回method；如果是response 返回status code；
    接收 bytes类型及str类型
    返回 str类型
    """
    if type(buf) == bytes:
        data = str(buf)[2:-1]
    else:
        data = buf
    if data.split()[0] == 'SIP/2.0':
        message_method = data.split()[1]
    else:
        message_method = data.split()[0]
    return message_method


def gen_call_id():
    """
    生成15位的随机字符串作为call_id
    :return: str
    """
    call_id = ''.join(str(uuid.uuid1()).split('-'))
    return call_id[:15]


def gen_branch():
    """
    生成z9hG4bK开头的随机branch
    :return: str
    """
    branch = ''.join(str(uuid.uuid1()).split('-'))
    return 'z9hG4bK' + branch[:12]


def gen_tag():
    tag = ''.join(str(uuid.uuid1()).split('-'))
    return tag[:15]


def is_hold(buf):
    '''
    判断buf是否为INVITE中带有sendonly
    :param buf:
    :return:
    '''
    if return_sip_method(buf) != 'INVITE':
        print('message is not a INVITE message')
        return False
    if buf.find(b'\r\n\r\n') != -1:
        # 如果带有body
        # 去除b'转为str型
        buf_str = str(buf)[2:-1]
        header_list = buf_str.split('\\r\\n\\r\\n')[0].split('\\r\\n')[1:]
        body = buf_str.split('\\r\\n\\r\\n')[1]
        if body.find('a=sendonly') != -1:
            return True
        else:
            print('message do not have send only')
            return False
    else:
        # 未带body
        print('message do not have body!')
        return False


def is_resume(buf):
    if return_sip_method(buf) != 'INVITE':
        print('message is not a resume message')
        return False
    if is_hold(buf):
        print('message is a hold message')
        return False
    if str(buf)[2:-1].find('Subject: SIP Call') != -1:
        return False
    else:
        return True