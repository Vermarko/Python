# per mandare mail da pytho
from email.message import EmailMessage

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "tua_email@gmail.com"
    msg['To'] = "destinatario@gmail.com"

    # Connessione al server Gmail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("tua_email@gmail.com", "LA_TUA_APP_PASSWORD")
        smtp.send_message(msg)