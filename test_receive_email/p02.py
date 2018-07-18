import json
import os
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib


# 获取email的配置文件
def get_email_info():
    user_home = os.environ.get("HOME")
    conf_base_path = user_home + "/conf"
    email_conf_path = conf_base_path + "/email.conf"
    with open(email_conf_path, "r") as f1:
        res_str = f1.read()
    mysql_dict = json.loads(res_str)
    return mysql_dict


# 得到链接email的链接对象
def get_server():
    email_dict = get_email_info()
    email_addr = email_dict.get("email")
    email_password = email_dict.get("password")
    pop_server = email_dict.get("pop_server")
    # 连接到POP3服务器:
    server = poplib.POP3(pop_server)
    # 可以打开或关闭调试信息:
    server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))
    # 身份认证:
    server.user(email_addr)
    server.pass_(email_password)
    return server


# 解析邮件编码,使其正常显示
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


# 获取编码
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        print(pos)
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
        if charset == 'utf-8; format=flowed':
            charset = 'utf-8'
        print(charset)
    return charset


# 解析message对象
def print_info(one_list, msg, indent=0):
    tmp = {}
    # 如果索引是0的话,就代表是在刚开始解析,就可以获取头信息
    if indent == 0:
        tmp01 = {}
        # 邮件请求头
        from_email = msg.get("From")
        from_email_tmp = parseaddr(from_email)
        # 发送的邮件地址
        sender = from_email_tmp[1]
        tmp01["sender"] = sender
        # 发件人的别名
        sender_alias = decode_str(from_email_tmp[0])
        tmp01["sender_alias"] = sender_alias
        # 这是邮件主题
        subject = msg.get("Subject")
        subject = decode_str(subject)
        tmp01['subject'] = subject
        # 邮件的收件人
        receiver = msg.get("To")
        receiver_tmp = parseaddr(receiver)
        # 接收的邮件地址
        receiver = receiver_tmp[1]
        tmp01['receiver'] = receiver
        receiver_alias = decode_str(receiver_tmp[0])
        tmp01["receiver_alias"] = receiver_alias
        tmp['data'] = tmp01
        tmp['type'] = "header"
    # 如果这个信息是message类型,就递归遍历
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print_info(one_list, part, indent + 1)
    # 如果不是就进行解析,显示内容
    else:
        content_type = msg.get_content_type()
        # 如果这块内容是plain或者html格式的,就显示打印
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset, "ignore")
            tmp['content'] = content
            if content_type == 'text/plain':
                tmp['type'] = "text"
            else:
                tmp['type'] = 'html'
        # 否则的话就不显示打印
        else:
            tmp03 = {}
            name_tmp = msg.get("Content-Type", "")
            name = "暂无数据"
            if "name" in name_tmp:
                name = str(name_tmp).split("name")[-1].split('"')[1]
            tmp03['file_name'] = name
            data_type = msg.get("Content-Transfer-Encoding", "")
            tmp03["file_type"] = data_type
            data = msg.get_payload()
            tmp03['file_data'] = data
            tmp['data'] = tmp03
            tmp['type'] = 'file'
    one_list.append(tmp)
    return one_list


# 获取邮箱的所有邮件
def get_all_mails_and_length(server):
    mails = server.list()[1]
    length = len(mails)
    return mails, length


# 获取一封邮件的Message对象
def get_msg_obj(server, index):
    lines = server.retr(index)[1]
    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8', "ignore")
    # 获取Message对象:
    msg = Parser().parsestr(msg_content)
    return msg


if __name__ == '__main__':
    # 获取邮箱链接
    server = get_server()
    # 获取邮箱下的所有邮件
    mails, length = get_all_mails_and_length(server)
    # 遍历每个邮件,解析每个邮件
    for i in range(1, length + 1):
        # 获取每个邮件的Message对象
        one_list = []
        one_msg = get_msg_obj(server, i)
        # 解析每个邮件,如果邮件出错就跳过本次循环
        try:
            res_list = print_info(one_list, one_msg)
        except:
            continue
        for one in res_list:
            print(one)
    # 关闭连接:
    server.quit()
