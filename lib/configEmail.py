


import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import threading
import config.readConfig as readConfig
from lib.Log import MyLog
import zipfile
import glob

localReadConfig = readConfig.ReadConfig()


class Email:
	""" pass """
	def __init__(self):
		""" pass """
		self.host = localReadConfig.get_email('mail_host')
		self.user = localReadConfig.get_email('mail_user')
		self.password = localReadConfig.get_email('mail_pass')
		self.port = localReadConfig.get_email('mail_port')
		self.sender = localReadConfig.get_email('mail_send')
		self.title = localReadConfig.get_email('mail_title')
		self.value = localReadConfig.get_email('receiver')
		
		self.receiver = []
		for n in str(self.value).split("/"):
			self.receiver.append(n)
		date = datetime.now().strftime("%Y-%m-%d %H:%M-%S")
		self.subject = '接口测试报告' + ' ' + date

		self.log = MyLog.get_log()
		self.logger = self.log.get_logger()
		self.msg = MIMEMultipart('related')

	def config_header(self):
		""" pass """
		f = open(os.path.join(ReadConfig.proDir, 'testFile', 'emailStyle.txt')) 
		content = f.read()
		f.close()
		content_plain = MIMEText(content, 'html', 'UTF-8')
		self.msg.attach(content_plain)
		self.config_image()

	def config_image(self):
		""" pass """
		image1_path = os.path.join(readConfig.proDir, 'testFile', 'img', '1.png')
		fp1 = open(image1_path, 'rb')
		msgImage1 = MIMEImage(fp1.read())
		fp1.close()
		msgImage1.add_header('Content-ID', '<image1>')
		self.msg.attach(msgImage1)

		image2_path = os.path.join(readConfig.proDir, 'testFile', 'img', 'log.jpg')
		fp2 = open(image2_path, 'rb')
		msgImage2 = MIMEImage(fp2.read())
		fp2.close()
		msgImage2.add_header('Content-ID', '<image2>')
		self.msg.attach(msgImage2)

	def config_file(self):
		""" pass """
		if self.check_file():
			reportpath = self.log.get_result_path()
			zippath = os.path.join(readConfig.proDir, 'result', 'test.zip')
			files = glob.glob(reportpath + '\*')
			f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
			for file in files:
				#修改压缩文件的目录结构
				f.write(file, '/report/'+os.path.basename(file))
			f.close()

			reportfile = open(zippath, 'rb').read()
			filehtml = MIMEText(reportfile, 'base64', 'utf-8')
			filehtml['Content-Type'] = 'application/octet-stream'
			filehtml['Content-Disposition'] = 'attachment; filename="test.zip"'
			self.msg.attach(filehtml)

		def check_file(self):
			""" pass """
			reportpath = self.log.get_report_path()
			if os.path.isfile(reportpath) and not os.stat(reportpath) == 0:
				return True
			else:
				return False

		def send_email(self):
			""" pass """
			self.config_header()
			self.config_content()
			self.config_file()
			try:
				smtp = smtplib.SMTP()
				smtp.connect(host)
				smtp.login(self.user, self.password)
				smtp.sendemail(self.sender, self.receiver, self.msg.as_string())
				smtp.quit()
				self.logger.info('The test report has send to developer by email.')
			except Exception as ex:
				self.logger.error(str(ex))

class MyEmail:
	""" pass """
	email = None
	mutex = threading.lock()

	def __init__(self):
		""" pass """
		pass

	@staticmethod
	def get_email():
		""" pass """
		if MyEmail.email is None:
			MyEmail.mutex.acquire()
			MyEmail.email = Email()
			MyEmail.mutex.release()
		return MyEmail.email


if __name__ == '__main__':
	email = MyEmail.get_email()