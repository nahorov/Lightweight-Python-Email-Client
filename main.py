from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore

import smtplib
from smtplib import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import sys
import imaplib

email_folder = " "
output_directory = "/home/rohan/temp"

class MyGUI(QMainWindow):

	def __init__(self):
		super(MyGUI, self).__init__()
		uic.loadUi("mailgui.ui", self)
		self.show()

		self.login_button.clicked.connect(self.login)
		self.attach_button.clicked.connect(self.attach)
		self.send_button.clicked.connect(self.send_email)
		self.dump_inbox_button.clicked.connect(self.dump_inbox)

	def login(self):
		try:
			self.server = smtplib.SMTP(self.smtp_server_address.text(), self.smtp_port_number.text())
			self.server.ehlo()
			self.server.starttls()
			self.server.ehlo()
			self.server.login(self.email_address.text(), self.password.text())

			self.email_address.setEnabled(False)
			self.password.setEnabled(False)
			self.smtp_server_address.setEnabled(False)
			self.port_number.setEnabled(False)
			self.login_button.setEnabled(False)

			self.recipient_address.setEnabled(True)
			self.email_subject.setEnabled(True)
			self.attach_button.setEnabled(True)
			self.send_button.setEnabled(True)
			self.email_text_body.setEnabled(True)
			self.ToLabel.setEnabled(True)
			self.SubjectLabel.setEnabled(True)
			self.AttachmentsLabel.setEnabled(True)

			self.msg = MIMEMultipart()

		except smtplib.SMTPAuthenticationError:
			message_box = QMessageBox()
			message_box.setText("Invalid Login Information, Authentication Failed.")
			message_box.exec()

		except:
			message_box = QMessageBox()
			message_box.setText("Login Failed. Reason Undiagnosed.")
			message_box.exec()

	def attach(self):
		options = QFileDialog.Option()
		filenames, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "All Files (*.*)", options=options)
		if filenames != []:
			for filename in filenames:
				attachment = open(filename, 'rb')

				filename = filename[filename.rfind("/") + 1:]
				p = MIMEBase('application', 'octet-stream')
				p.set_payload(attachment.read())
				encoders.encode_base64(p)
				p.add_header("Content-Disposition", f"attachment; filename={filename}")
				self.msg.attach(p)
				if not self.AttachmentsLabel.text().endswith(":"):
					self.AttachmentsLabel.setText(self.AttachmentsLabel.text() + ",")
				self.AttachmentsLabel.setText(self.AttachmentsLabel.text() + " " + filename)

	def send_email(self):
		dialog = QMessageBox()
		dialog.setText("Are you sure you want to send this e-mail?")
		dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)  # 0
		dialog.addButton(QPushButton("No"), QMessageBox.NoRole)  # 1

		if dialog.exec_() == 0:
			try:
				self.msg['From'] = self.email_address.text()  # Edit this to your own liking
				self.msg['To'] = self.recipient_address.text()
				self.msg['Subject'] = self.email_subject.text()
				self.msg.attach(MIMEText(self.email_text_body.toPlainText(), 'plain'))
				text = self.msg.as_string()
				self.server.sendmail(self.email_address.text(), self.recipient_address.text(), text)
				message_box = QMessageBox()
				message_box.setText("E-mail Sent!")
				message_box.exec()
			except SMTPResponseException as e:
				error_code = e.smtp_code
				error_message = e.smtp_code
				message_box = QMessageBox()
				message_box.setText("Sending E-mail has failed.")
				message_box.setText("Error Code: " + error_code)
				if (error_code == 422):
					message_box.setText("Recipient Mailbox is full.")
				elif (error_code == 431):
					message_box.setText("Server is out of space.")
				elif (error_code == 447):
					message_box.setText("Timeout. Try reducing the number of recipients.")
				elif (error_code == 510 or error_code == 511):
					message_box.setText(
						"One of the addresses in the recipients doesn't exist, please check again for errors.")
				elif (error_code == 541 or error_code == 554):
					message_box.setText(
						"Your message has been identified as spam. It belongs in a sandwich, not in a server, thank you very much.")
				elif (error_code == 550):
					message_box.setText("Firewall rejected.")
				elif (error_code == 553):
					message_box.setText(
						"Check all the addresses in the recipient field. There should be an error or misspelling somewhere.")
				elif (error_code == 512):
					message_box.setText("Check all the addresses in the recipient field, there should be an error.")
				else:
					message_box.setText(error_code + ": " + error_message)

				message_box.exec()

	def process_inbox(self):
		# Function to dump all emails in the folder to files in the input directory.

		rv, data = self.search(None, "ALL")
		if rv != 'OK':
			message_box.setText("Messages not found. ")
			return

		for num in data[0].split():
			rv, data = self.fetch(num, '(RFC822)')
			if rv != 'OK':
				message_box.setText("Error encountered while retrieving messages, please try again. ", num)
				return
			f = open('%s/%s.eml' %(output_directory, num), 'wb')
			f.write(data[0][1])
			f.close()
			message_box.setText("Done!")

	def dump_inbox(self):
		self.server = imaplib.IMAP4_SSL(self.imap_server_address.text(), self.imap_port_number.text())
		self.server.login(self.email_address.text(), self.password.text())
		rv, data = self.select(email_folder)
		if rv == 'OK':
			message_box.setText("Processing mailbox: ", email_folder)
			process_mailbox(self)
			self.close()
		else:
			message_box.setText("ERROR: Unable to open mailbox ", rv)
			self.logout()
			

app = QApplication([])
window = MyGUI()
app.exec_()
