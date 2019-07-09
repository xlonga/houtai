


import unittest
import paramunittest 
from config import readConfig
from lib import Log
from lib import common
from lib import configHttp


case_xls = common.get_xls("case_xlsx")
localReadConfig = readConfig.ReadConfig()
configHttp = configHttp.ConfigHttp()


@paramunittest.parametrized(*case_xls)
class FileUpload_api(unittest.TestCase):
	""" pass """
	


