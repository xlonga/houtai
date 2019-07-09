


from lib import common
from lib import configHttp
from config import readConfig

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogin_xls = common.get_xls('Case.xlsx')


def login():
	""" pass """
	url = '/ManagementPlatform/Account/Admin/v1.0/PhoneLogin'
	localConfigHttp.set_url(url)
	data = {'ACB501': '13522352342',
			'UCC003': 'E10ADC3949BA59ABBE56E057F20F883E'}
	localConfigHttp.set_data(data)
	response = localConfigHttp.post().json()
	UCE309 = common.get_value(response, 'UCE309')
	UCE385 = common.get_value(response, 'UCE385')
	return UCE309, UCE385



if __name__ == '__main__':
	print(login())

