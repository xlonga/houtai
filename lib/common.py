


import requests
from config import readConfig as readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from lib import configHttp
from lib import Log
import json

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir[0:-6]
localConfigHttp = configHttp.ConfigHttp()
log = Log.MyLog().get_log()
logger = log.get_logger()

caseNo = 0

def show_return_msg(response):
	""" 显示返回的数据 """
	url = response.url
	msg = response.text
	print("\n请求地址:"+url)
	print("\n请求返回值："+'\n'+json.dumps(json.loads(msg), ensure_ascii=False, sort_key=True, indent=4))


#***************************************读取用例excel****************************************
def get_xls(xls_name, api_id, sheet_name='sheet'):
	""" 读取testcase excel """
	cls = []
	xlsPath = os.path.join(proDir, 'testFile', 'case', xls_name)
	print(xlsPath)
	file = open_workbook(xlsPath)
	sheet = file.sheet_by_name(sheet_name)
	nrows = sheet.nrows
	for i in range(nrows):
		if sheet.row_values(i)[0] != u'ApiID' and i == api_id:
			cls.append(sheet.row_values(i))
	return cls


#***************************************读取sql xml****************************************
database = {}

def set_xml():
	""" 设置sql xml"""
	if len(database) ==0:
		sql_path = os.path.join(proDir, 'testFile', 'SQL.xml')
		tree = ElementTree.parse(sql_path)
		for db in tree.findall('database'):
			db_name = db.get("name")
			table = {}
			for tb in db.getchildren():
				table_name = tb.get("name")
				sql = {}
				for data in tb.getchildren():
					sql_id = data.text
				table[table_name] = sql
			database[db_name] = table

def get_xml_dict(database_name, table_name):
	""" pass """
	set_xml()
	database_dict = database.get(database_name).get(table_name)
	return database_dict

def get_sql(database_name, table_name, sql_id):
	""" pass """
	db = get_xml_dict(database_name, table_name)
	sql = db.get(sql_id)
	return sql


#***************************************读取接口地址 xml****************************************
def get_url_from_xml(name):
	""" pass """
	url_list = []
	url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
	tree = ElementTree.parse(url_path)
	for u in tree.finall('url'):
		url_name = u.get('name')
		if url_name == name:
			for c in u.getchildren():
				url_list.append(c.text)
	url = '/v2/' + '/'.jion(url_list)
	return url


#***************************************获取接口返回数据的指定参数****************************************
def get_value(my_dict, key):
	""" 递归函数，取返回的字典中的值 """
	if isinstance(my_dict, dict):
		if my_dict.get(key) or my_dict.get(key) == 0 or my_dict.get(key) == ''\
				and my_dict.get(key) is False:
			return my_dict.get(key)

		for my_dict_key in my_dict:
			if get_value(my_dict.get(my_dict_key), key) or\
							get_value(my_dict.get(my_dict_key), key) is False:
				return get_value(my_dict.get(my_dict_key), key)

	if isinstance(my_dict, list):
		for my_dict_arr in my_dict:
			if get_value(my_dict_arr, key)\
					or get_value(my_dict_arr, key) is False:
				return get_value(my_dict_arr, key)

def list_for_key_to_dict(*args, my_dict):
	""" 接收需要解析的dict和包含要解析的my_dict的key的list"""
	result = {}
	if len(args) > 0:
		for key in args:
			result.update({key: get_value(my_dict, key)})
	return result


#**********************************************同参数取不同值显示***********************************************
def compare_json_data(A, B, xpath='.'):
    if isinstance(A, list) and isinstance(B, list):
        for i in range(len(A)):
            try:
                compare_json_data(A[i], B[i], xpath + '[%s]'%str(i))
            except:
                print ('▇▇▇▇▇ A中的%s[%s]未在B中找到'%(xpath,i))
    if isinstance(A, dict) and isinstance(B, dict):
        for i in A:
            try:
                B[i]
            except:
                print ('▇▇▇▇▇ A中的%s/%s 未在B中找到'%(xpath,i))
                continue
            if not (isinstance(A.get(i), (list, dict)) or isinstance(B.get(i), (list, dict))):
                if type(A.get(i)) != type(B.get(i)):
                    print ('▇▇▇▇▇ 类型不同参数在[A]中的绝对路径:  %s/%s  ►►► A is %s, B is %s '%(xpath,i,type(A.get(i)),type(B.get(i))))
                elif A.get(i) != B.get(i):
                    print ('▇▇▇▇▇ 仅内容不同参数在[A]中的绝对路径:  %s/%s  ►►► A is %s, B is %s ' % (xpath, i, A.get(i), B.get(i)))
                continue
            compare_json_data(A.get(i), B.get(i), xpath + '/' + str(i))
        return
    if type(A) != type(B):
        print ('▇▇▇▇▇ 类型不同参数在[A]中的绝对路径:  %s  ►►► A is %s, B is %s ' % (xpath, type(A), type(B)))
    elif A != B and type(A) is not list:
        print ('▇▇▇▇▇ 仅内容不同参数在[A]中的绝对路径:  %s  ►►► A is %s, B is %s ' % (xpath, A, B))


if __name__ == '__main__':
	print(get_xls("login"))
	