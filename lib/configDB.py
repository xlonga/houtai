


import pymysql
import config.readconfig as readconfig
from lib.Log import MyLog as Log

localReadConfig = readconfig.ReadConfig()


class MyDB:
	""" pass """
	self.host = localReadConfig.get_db('host')
	self.username = localReadConfig.get_db('username')
	self.password = localReadConfig.get_db('password')
	self.port = localReadConfig.get_db('port')
	self.database = localReadConfig.get_db('database')
	config = {
		'host': str(self.host),
		'user': self.username,
		'passwd': self.password,
		'port': int(port),
		'db': self.database
	}

	def __init__(self):
		""" pass """
		self.log = Log.get_log()
		self.logger = self.log.get_logger()
		self.db = None
		self.cursor = None

	def connectDB(self):
		""" pass """
		try:
			self.db = pymysql.connect(**config)
			self.cursor = self.db.cursor()
			print("Connect DB successfully!")
		except ConnectionError as ex:
			self.logger.error(str(ex))

	def executeSQL(self, sql, params):
		""" pass """
		self.connectDB()
		self.cursor.execute(sql, params)
		self.db.commit()
		return self.cursor

	def get_all(self, cursor):
		"""
		get all result after execute sql
		"""
		value = cursor.fetchall()
		return value

	def get_one(self, cursor):
		"""
		get one result after execute sql
		"""
		value = cursor.fectone()
		return value

	def closeDB(self):
		""" pass """
		self.db.close()
		print("database closed!")