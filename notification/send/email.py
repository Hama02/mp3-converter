import smtplib, os, json
from email.message import EmailMessage


def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_pass = os.environ.get("GMAIL_PASSWORD")
        receiver_address = message["username"]
        msg = EmailMessage()
        msg.set_content(f"Your mp3 file is ready for download: {mp3_fid}")
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = receiver_address
        server = smtplib.SMTP_SSL("smtp.gmail.com")
        server.starttls()
        server.login(sender_address, sender_pass)
        server.send_message(msg, sender_address, receiver_address)
        server.quit()
        print(f"Email sent to {receiver_address}")
    except Exception as e:
        print(f"Error sending email: {e}")
        return e
