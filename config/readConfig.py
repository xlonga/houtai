


import os
import codecs
import configparser


proDir = os.path.split(os.path.realpath(__file__))[0]
# print(proDir)
configPath = os.path.join(proDir, 'config.ini')
# print(configPath)

class ReadConfig:
	""" pass """
	def __init__(self):
		""" pass """
		fd = open(configPath)
		data = fd.read()
		# remove BOM
		if data[:3] == codecs.BOM_UTF8:
			data = data[3:]
			file = codecs.open(configPath, 'w')
			file.write(data)
			file.close()
		fd.close()

		self.cf = configparser.ConfigParser()
		self.cf.read(configPath)

	def get_email(self, name):
		""" pass """
		value = self.cf.get('EMAIL', name)
		return value

	def get_http(self, name):
		""" pass """
		value = self.cf.get('HTTP', name)
		return value

	def get_headers(self, name):
		""" pass """
		value = self.cf.get('HEADERS', name)
		return value

	def set_headers(self, name, value):
		""" pass """
		self.cf.set('HEADERS', name, value)
		with open(configPath, 'w+') as f:
			self.cf.write(f)

	def get_url(self, name):
		""" pass """
		value = self.cf.get('URL', name)
		return value

	def get_db(self, name):
		""" pass """
		value = self.cf.get('DATABASE', name)
		return value