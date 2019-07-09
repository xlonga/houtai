


import os
from config import readConfig
import logging
from datetime import datetime
import threading

localReadConfig = readConfig.ReadConfig()


class Log:
	""" pass """
	def __init__(self):
		""" pass """
		self.proDir = readConfig.proDir[0:-6]
		self.resultPath = os.path.join(self.proDir, 'result')
		if not os.path.exists(self.resultPath):
			os.mkdir(self.resultPath)
		self.logPath = os.path.join(self.resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
		if not os.path.exists(self.logPath):
			os.mkdir(self.logPath)
			
		self.logger = logging.getLogger()   #返回日志器名称标识，不填则为root
		self.logger.setLevel(logging.INFO)  #设置日志器处理的日志消息的最低严重级别INFO

		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levename)s - %(message)s')  #设置日志格式
		handler = logging.FileHandler(os.path.join(self.logPath, 'output.log'))  #将日志消息发送到磁盘文件
		handler.setFormatter(formatter)     
		self.logger.addHandler(handler)    #为该logger对象添加一个handler对象

	def get_logger(self):
		""" pass """
		return self.logger

	def build_start_line(self, case_no):
		""" pass """
		self.logger.info("--------" + case_no + "START--------")

	def build_end_line(self, case_no):
		""" pass """
		self.logger.info("--------" + case_no + "END--------")

	def build_case_line(self, case_name, code, msg):
		""" pass """
		self.logger.info(case_name + " - Code:" + code + " - msg" + msg)

	def get_report_path(self):
		""" pass """
		report_path = os.path.join(self.logPath, "report.html")
		return report_path

	def get_result_path(self):
		""" pass """
		return self.logPath

	def write_result(self, result):
		""" pass """
		result_path = os.path.join(self.logPath, "report.txt")
		fb = open(result_path, 'wb')
		try:
			fb.write(result)
		except FileNotFoundError as ex:
			logger.error(str(ex))


class MyLog:
	""" pass """
	log = None
	mutex = threading.Lock()

	def __int__(self):
		""" pass """
		pass

	@staticmethod
	def get_log():
		""" pass """
		if MyLog.log is None:
			MyLog.mutex.acquire()
			MyLog.log = Log()
			MyLog.mutex.release()

		return MyLog.log


if __name__ == '__main__':
	log = MyLog.get_log()
	logger = log.get_logger()
	logger.debug("test debug")
	logger.info("test info")