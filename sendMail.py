import smtplib

def send(text='nothing', mail=None):
    #mail =  ('host', 'from-to', 'pass') 
    HOST = mail[0]
    SUBJECT = "Weekly backup report"
    FROM = mail[1]
    TO = mail[1]
 
    BODY = "\r\n".join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        text
    ))
 
    server = smtplib.SMTP(HOST, 587)
    server.starttls()

    server.login(mail[1], mail[2])
    server.sendmail(FROM, [TO], BODY)
    server.quit()


