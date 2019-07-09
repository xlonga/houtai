


import requests
from config import readConfig
from lib import Log
import json


loacalReadConfig = readConfig.ReadConfig()


class ConfigHttp:
	""" pass """

	

	def __init__(self):
		""" pass """
		global scheme, host, port, timeout
		scheme = loacalReadConfig.get_http('scheme')
		host = loacalReadConfig.get_http('baseurl')
		port = loacalReadConfig.get_http('port')
		timeout = loacalReadConfig.get_http('timeout')
		self.log = Log.MyLog().get_log()
		self.logger = self.log.get_logger()
		self.headers = {}
		self.params = {}
		self.data = {}
		self.url = None
		self.files = {}
		self.state = 0
		self.session = requests.Session()

	def set_url(self, url):
		""" 生成完整的基本url """
		self.url = scheme+'://'+host+':'+port+url
		print(self.url)

	def set_headers(self, header):
		""" pass """
		self.headers = header

	def set_params(self, param):
		""" pass """
		self.params = param

	def set_data(self, data):
		""" pass """
		self.data = data

	def set_files(self, filename):
		""" pass """
		if filename != '':
			file_path = 'D:/python/image/' + filename

		if filename == '' or filename is None:
			self.state = 1

	def get(self):
		""" pass """
		try:
			response = self.session.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
			return response
		except TimeoutError:
			self.logger.error("Time out!")
			return None

	def post(self):
		""" pass """
		try:
			response = self.session.post(self.url, headers=self.headers, data=self.data, timeout=float(timeout))
			return response
		except TimeoutError:
			self.logger.error("Time out!")
			return None

	def postWithFile(self):
		""" pass """
		try:
			response = self.session.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
			return response
		except TimeoutError:
			self.logger.error("Time out!")
			return None

	def postWithJson(self):
		""" pass """
		try:
			response = self.session.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
			return response
		except TimeoutError:
			self.logger.error("Time out!")
			return None



if __name__ == '__main__':
	print('ConfigHttp')
