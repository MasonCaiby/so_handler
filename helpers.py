import os
import errno
import glob
from emailer import build_message


def safe_folder(folder_name):
    ''' DOCSTRING
        Safely makes a new folder, useful if you will be saving to a possibly
        new folder
        ---------
        INPUTS:
        folder_name: the name of the *new* folder you want to *make*
        ---------
        RETURNS:
        NONE
    '''
    try:
        os.makedirs(folder_name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def newest_file(folder):
    ''' DOCSTRING
        Gets the most recently saved file from a folder
        ---------
        INPUTS:
        folder: the name of the folder whose files you want to check
        ---------
        RETURNS:
        latest_file: the absolute pathname of the latest file saved to a folder
    '''
    list_of_files = glob.glob(folder+'/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    latest_file = os.path.abspath(latest_file)
    return latest_file


def remote_verbose_emailer(epoch_number, remote_verbose_email, body):
    ''' DOCSTRING
        Sends an email to a specified email address, with a specified body and
        epoch number. I hard coded the rest in as this is really an extension of
        a function I already made.
        ---------
        INPUTS:
        epoch_number: The number epoch this poem's weights are from
        remote_verbose_email: the email you will be sending the poem to
        body: the body of the email
        --------
        RETURNS
        NONE
    '''
    subject = 'Epoch number {} finished training, \
                poem enclosed'.format(epoch_number)
    with open('gmail.csv') as gmail:
        creds = gmail.read().split(', ')
        from_email = creds[0]
        from_password = creds[1]
    build_message(subject=subject,
                  name='RNN Trainer',
                  name_from='Your model in training',
                  from_email=from_email,
                  password=from_password,
                  to_email=remote_verbose_email,
                  poem=body)
    print('email to {} sent\n'.format(remote_verbose_email))
