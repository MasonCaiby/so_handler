import os, errno, glob
from emailer import build_message

def safe_folder(folder_name):
    try:
        os.makedirs(folder_name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def newest_file(folder):
    list_of_files = glob.glob(folder+'/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def remote_verbose_emailer(epoch_number, remote_verbose_email, poem):
    subject = 'Epoch number {} finished training, poem enclosed'.format(epoch_number)
    with open('gmail.csv') as gmail:
        creds = gmail.read().split(', ')
        from_email = creds[0]
        from_password = creds[1]
    build_message(subject=subject,
                  name='RNN Trainer',
                  name_from='Your model in training',
                  from_email=from_email, password=from_password,
                  to_email=remote_verbose_email, poem=poem)
    print('email to {} sent\n'.format(remote_verbose_email))
