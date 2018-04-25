from flickr_scraper import main
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


def build_message(name, name_from, from_email, password, to_email, poem, img):
    ''' DOCSTRING
        This builds and sends an email. The from email address must be a gmail
        address and have its security set to less trustyworth apps, or whatever
        google calls them
        ---------
        INPUTS
        name: the name of the person the email is for
        name_from: the sender's name
        from_email: the email address you will be sending the email from
        password: the password for the email address you will be sending from
        to_email: the email you want to send to
        poem: the poem you are sending (or just some other body text)
        img: the image you would like to attach to the email
        ---------
        RETURNS
        NONE
    '''
    now = datetime.datetime.now()
    date = now.strftime("%m-%d-%Y")
    subject = "I love you, {} ({})".format(name, date)

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Create the body of the message.
    html = """\
        <p>""" + str(poem) + """<br><br>
            <img src="cid:image1"><br><br>
            Love, <br>
            """ + str(name_from)


    # Record the MIME types.
    msgHtml = MIMEText(html, 'html')

    with open(img, 'rb') as img_open:
        img_email = img_open.read()
        msgImg = MIMEImage(img_email, 'jpg')
        msgImg.add_header('Content-ID', '<image1>')
        msgImg.add_header('Content-Disposition', 'inline', filename=img)

    msg.attach(msgHtml)
    msg.attach(msgImg)

    server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_email, password)
    #server.send_message(msg)
    server.sendmail(from_email, to_email, msg.as_string())
    server.close()

if __name__ == "__main__":
    with open('gmail.csv') as gmail:
        creds = gmail.read().split(', ')
        from_email = creds[0]
        from_password = creds[1]
    build_message('Marissa', 'Max', from_email, from_password,
                  'custome.love.poems@gmail.com', 'poem',
                  'flickr/27209935818_26bc8f7476_b.jpg')
