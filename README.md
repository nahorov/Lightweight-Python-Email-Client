# Lightweight-Python-Email-Client
A lightweight GUI Email Client in Python 3 and PyQt5

Software prerequisites required:
1. Python 3.8
2. Qt5, PyQt5 5.14

The script is simple enough to run. On Linux terminal, a simple "python3 main.py" should work. 

The first four fields to be filled are the login credentials for the email account you want to send email from. The last four fields at the bottom of the GUI application are for the login credentials for the email account whose inbox contents you want downloaded into the folder. Effectively you can send email out of one email account, and check the inbox of another email account at the same time, hence the seemingly-redundant functionality. 
Future update might contain an extention to access and read the emails having been downloaded, and then delete them if will need be. 

Emails can be accessed in the /tmp/Email/ folder, in a subdirectory created dynamically at the time at which the "Dump Inbox" button was clicked, bearing the said email address from which the contents were fetched, and date and time at which the "Dump Inbox" button was clicked. Emails will be downloaded in reverse chronological order, as in, the first email to be downloaded would be the latest one which was received. 
