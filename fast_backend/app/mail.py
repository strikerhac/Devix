from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import APIRouter
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email import encoders
import traceback
import sys
from app.utils.db_utils import *
from app.core.config import *
from app.models.monitoring_models import *


def send_email(
        send_from,
        send_to,
        subject,
        message,
        files = [],
        server='smtp.office365.com',
        port = 587,
        username = '',
        password = '',
        use_tls = True
):
    """
    compose and send email with the given parameters and with the provided info and attachments.

    Args:
        send_from (str):from name
        send_to (list[str]): to name(s)
        subject (str):message title
        message (str):message body
        files(list[str]): files(s) list of file paths to be attached to email
        server(str): mail server smtp server
        port (int): port number
        username (str):server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    Args:
        send_from:
        send_to:
        subject:
        message:
        port:
        username:
        password:
        use_tls:
        files:

    Returns:

    """
    COMMASPACE = ', '
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))
    for path in files:
        part = MIMEBase('application', 'octet-stream')
        with open(path,'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment;filename={}'.format(Path(path).name))
        msg.attach(part)

    smtp = smtplib.SMTP(server,port)
    if use_tls:
        smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from,send_to,msg.as_string())



def GenerateMailForCloudAlert(alert):
    try:
        print("\n### Generating Mail for Cloud Alerts ###\n",file=sys.stderr)
        mailQuery = "select * from mail_credentials where status='active';"
        mail_cred = configs.db.execute(mailQuery)
        if mail_cred is None:
            return JSONResponse(content="Mail Credentails Not Found", status_code=404)
        mail_cred = dict(mail_cred)
        print("\n---> Active Mail Credentials <---\n", file=sys.stderr)
        print(mail_cred, file=sys.stderr)
        receipents = []
        msg = f"""
                SERVEICE NAME  : {alert['service_name']}
                SERVICE KEY    : {alert['service_key']}
                ACCOUNT LABEL  : {alert['account_label']}

                Alert Level    : {alert['level']}
                Alert Type     : {alert['type']}
                Description    : {alert['description']}
                Date/Time      : {alert['time']}
                """
        try:
            query = "select * from alert"

            try:
                result = configs.db.execute(query)
                for row in result:
                    receipents.append(row[1])
            except Exception as e:
                traceback.print_exc()
            subject = f"MonetX - NEW Cloud Alert | {alert['service_name']} | {alert['level']}"
            if alert['status'] == 'Clear':
                subject = f"MonetX - Cloud Alert CLEARED | {alert['service_name']} | {alert['level']}"

            send_email(
                send_from=mail_cred['MAIL'],
                send_to=receipents,
                subject=subject,
                message=msg,
                username=mail_cred['MAIL'],
                password=mail_cred['PASSWORD'],
                server=mail_cred['SERVER']
            )
        except Exception as e:
            traceback.print_exc()

    except Exception as e:
        traceback.print_exc()