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
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


# 解析message对象
def print_info(one_list, msg, indent=0):
    tmp = {}
    # 如果索引是0的话,就代表是在刚开始解析,就可以获取头信息
    if indent == 0:
        # 邮件请求头
        from_email = msg.get("From")
        from_email_tmp = parseaddr(from_email)
        # 发送的邮件地址
        sender = from_email_tmp[1]
        tmp["sender"] = sender
        # 发件人的别名
        sender_alias = decode_str(from_email_tmp[0])
        tmp["sender_alias"] = sender_alias
        # 这是邮件主题
        subject = msg.get("Subject")
        subject = decode_str(subject)
        tmp['subject'] = subject
        # 邮件的收件人
        receiver = msg.get("To")
        receiver_tmp = parseaddr(receiver)
        # 接收的邮件地址
        receiver = receiver_tmp[1]
        tmp['receiver'] = receiver
        receiver_alias = decode_str(receiver_tmp[0])
        tmp["receiver_alias"] = receiver_alias
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
                content = content.decode(charset)
            tmp['content'] = content
        # 否则的话就不显示打印
        else:
            name_tmp = msg.get("Content-Type", "")
            name = "暂无数据"
            if "name" in name_tmp:
                name = str(name_tmp).split("name")[-1].split('"')[1]
            tmp['file_name'] = name
            data_type = msg.get("Content-Transfer-Encoding", "")
            tmp["file_type"] = data_type
            data = msg.get_payload()
            tmp['file_data'] = data
    one_list.append(tmp)
    return one_list


server = get_server()
# 返回所有邮件:
mails = server.list()[1]

# 获取具体的某封邮件, 注意索引号从1开始:
index = len(mails)
lines = server.retr(index)[1]

# lines存储了邮件的原始文本的每一行,
# 可以获得整个邮件的原始文本:
msg_content = b'\r\n'.join(lines).decode('utf-8')
# 获取Message对象:
msg = Parser().parsestr(msg_content)

one_list = []
new_list = print_info(one_list, msg)
print(len(new_list))
for one in new_list:
    print(one)

# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接:
server.quit()
