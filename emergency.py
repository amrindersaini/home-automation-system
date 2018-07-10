import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
from datetime import datetime

class Emergency():
    def email():
        mail = MIMEMultipart()
        fromaddr = "asingh437@myseneca.ca"
        toaddr = "asingh437@myseneca.ca"
        mail['From'] = fromaddr
        mail['To'] =  toaddr
        mail['Subject'] = "Emergency At Home"
        timestamp = datetime.now()
        body = "Emergency button was pressed at home : " + str(timestamp)
        mail.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.live.com', 587)
        server.starttls()
        server.login(fromaddr, "Saini@7676")
        text = mail.as_string()
        server.sendmail(fromaddr,toaddr, text)
        server.quit()