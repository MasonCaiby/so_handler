from flickr_scraper import main
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime


def build_message(name, from_email, to_email, poem, img):

    now = datetime.datetime.now()
    date = now.strftime("%m-%d-%Y")
    subject = "I love you, {} ({})".format(name, date)

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    msg.attach(poem)
    msg.attach(img)
