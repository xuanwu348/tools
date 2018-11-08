#coding:utf-8
import poplib
import getpass
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import time
import os

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get("Content-Type", "").lower()
        pos = content_type.find("charset=")
        if pos >= 0:
            charset = content_type[pos+8:].strip()
    return charset

def print_info(msg, indent=0):
    if indent == 0:
        for header in ["From", "To", "Subject"]:
            value = msg.get(header, '')
            if value:
                if header == "Subject":
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'{} <{}>'.format(name, addr)
            print("{}{}: {}".format(" " * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print("%spart %s" % (" " * indent, n))
            print("%s----------------" % (" " * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == "text/plain" or content_type == "text/html":
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                try:
                    content = content.decode(charset)
                except LookupError:
                    content = content.decode(charset.split(";")[0].strip())
                except Exception as e:
                    print("Error %s" % e)
                    pass
                
            #print("{}Text: {}".format(" " * indent, content + "....."))
            command_index = content.find("command_348:")
            if command_index >= 0:
                try:
                    print("content[command_index:-1].strip():%s" % content[command_index + len("command_348:"):-1].strip())
                    os.system(content[command_index + len("command_348:"):-1].strip())
                except Exception as e:
                    print("ErrorCommand %s" % e)
                    pass                
        else:
            print("%sAttachment: %s" % (" " * indent, content_type))

if __name__ == "__main__":
    
    
    email = input("Email addr:")
    password = getpass.getpass("Your password for email:")
    pop3_server = "pop.163.com"

    server = poplib.POP3(pop3_server)
    #server.set_debuglevel(1)
    #print(server.getwelcome().decode("utf-8"))

    server.user(email)
    server.pass_(password)

    #print("Message: %s size: %s" % server.stat())
    count_flag = 0
    while 1:
        resp, mails, octets = server.list()
        #print(mails)    
        index = len(mails)
        if index > count_flag:
            count_flag = index
        else:
            print("In loop.........")
            time.sleep(20)
            continue
        for i in range(index, index-5, -1):
            resp, lines, octets = server.retr(i)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            print_info(msg)
    server.quit()
