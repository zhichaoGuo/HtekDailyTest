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