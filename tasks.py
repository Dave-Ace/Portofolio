from celery import shared_task
from David import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

 

#celery -A David.celery worker --pool=solo -l info
@shared_task(bind=True)
def fetch(self, messages_to, messages_from):
    result = []
    x = messages_to.count()
    y = messages_from.count()
    
    me_to = []
    me_from = []
    for message in messages_to:
        me_to.append(message)
    for message in messages_from:
        me_from.append(message)
        

    messages_from = []
    messages_to  = []
        
    for i in me_to:
        messages_to.append(me_to[x-1])
        x -= 1
    
    for i in me_from:
        messages_from.append(me_from[y-1])
        y -= 1
            
    while len(messages_from) > 0:
        for message in messages_to:    
            if message.timestamp == "appended":
                continue
            else:
                for message2 in messages_from:
                    if message.timestamp < message2.timestamp and message.timestamp:
                        if message in result:
                            break
                        else:
                            result.append(self.message_to_json(message))
                            message.timestamp = "appended"
                            break
                    elif message.timestamp == message2.timestamp:
                        break
                    else:
                        if message2 in result:
                            break
                        else:
                            result.append(self.message_to_json(message2))
                            messages_from.remove(message2)
                            continue
    if len(messages_to) != 0:
        for message in messages_to:
            if message.timestamp != "appended":
                result.append(self.message_to_json(message))
    return result
@shared_task(bind=True)
def send_mail(self, name, email, subject, message):
    SMTP_SERVER = settings.SMTP_SERVER
    SMTP_PORT = settings.SMTP_PORT
    SMTP_USERNAME = settings.SMTP_USERNAME
    SMTP_PASSWORD = settings.SMTP_PASSWORD
    EMAIL_FROM = settings.EMAIL_FROM 
    EMAIL_TO = settings.EMAIL_TO
    EMAIL_SUBJECT = settings.EMAIL_SUBJECT

    name = name
    email = email
    subject = subject
    message = message

    co_msg = """ 
    Name: """ + name + """

    email: """ + email + """

    Message: """ + message + """
    
    """
    msg = MIMEText(co_msg)
    msg['Subject'] = EMAIL_SUBJECT + "|" + subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    debuglevel = True
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()
    return 'Message successfully sent'

