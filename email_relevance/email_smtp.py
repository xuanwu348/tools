import smtplib
import socket
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def email_to(sub,content,to_list,file_path = None):
    u"""发送邮件"""
    #解析参数，编辑内容
    content = content.split('\n')
    content = ("<div><a>" + i + "</a></div>" for i in content)
    content = '<html>' + ' '.join(content) + '</html>'
    msg = MIMEMultipart('test')
    msg['Subject'] = sub
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = ';'.join(to_list)
    msg1 = MIMEText(content,'html','utf-8')
    msg.attach(msg1)
    if file_path is None:
        pass
    else:
        for path in file_path:
            filename = path.split('/')[-1]
            att = MIMEText(open(path,'rb').read(),'base64','utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = 'attachment;filename="%s"' % filename
            msg.attach(att)
    s = smtplib.SMTP_SSL(EMAIL_HOST,EMAIL_PORT)
    s.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
    s.sendmail(EMAIL_HOST_USER,to_list,msg.as_string())
    s.quit()
    print('Success!')
    
if __name__== "__main__":
    print("send email")
    EMAIL_HOST = 'smtp.163.com'      #smtp server info, can get from email server page
    EMAIL_PORT = 465
    EMAIL_HOST_USER = input("请输入用户名：")       #Useracount like as "xxxx@163.com"
    EMAIL_HOST_PASSWORD = getpass.getpass("please input password：")       #password or the third persist
    sub = "Sengding a email"    #subject
    content = input("请输入要发送的邮件内容：")   #email content
    to_list = ['xxxxxx@163.com','xxxxxxxxx@qq.com'] #receive address
    #file_path = ["F:/workload/20170501_213138.jpg.JPG"] #attachment file
    try:
        email_to(sub,content,to_list)  #call function
        #email_to(sub,content,to_list)
    except smtplib.SMTPAuthenticationError as e:
        print("Error:" + str(e))
        print("please check you emailacount or pasword")
    except socket.gaierror as e:
        print("Error" + str(e))
        print("please check you network connect! And then try again!")
    
