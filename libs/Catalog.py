'''
    File name: Catalog.py
    Description: run BI publisher web services from ReportService and use in main.py
    Author: z.raddani
    Date created: 06 October 2018
    Python Version: 2.7
'''
import zeep
import datetime
from libs import *
import logging

class Catalog:
	def __init__(self,report_model_name,system_app_name):
		self.report_model_name = report_model_name
		self.system_app_name = system_app_name
		self.wsdl = '/xmlpserver/services/v2/CatalogService?wsdl'
		log_info.info('initial Catalog class....')

	def trans(self,typee):
		log_info.info('start trans....')
		if typee == 'model':
			ext = 'xdm'
			dirr = 'DATA_MODEL'
		else:
			ext = 'xdo'
			dirr = 'REPORTS'
		try:
			client = zeep.Client(wsdl=server_ip+self.wsdl)
			request_data = {
				'reportAbsolutePath' : '/' + self.system_app_name + '/' + dirr + '/' + self.report_model_name + '.' + ext,
				'userID'			 : user,
				'password'			 : passwrd
				}
			log_info.info('download report....')
			report_obj = client.service.downloadObject(**request_data)
		except:
			log_error('Error for download report ....')

		try:
			client = zeep.Client(wsdl=server_ip_dest+self.wsdl)
			request_data = {
				# 'reportObjectAbsolutePathURL' : '/' + self.system_app_name + '/REPORTS/' + self.report_model_name + '.xdo',
				'reportObjectAbsolutePathURL' : '/' + self.system_app_name + '/' + dirr + '/' + self.report_model_name + '.' + ext,
				'objectType'				  : ext+'z',
				'objectZippedData'			  : report_obj,
				'userID'					  : user,
				'password'					  : passwrd
				}
			log_info.info('upload report...')
			log_info.info(" file path: " + client.service.uploadObject(**request_data))
			log_info.info('successful trans ' + typee + ' : ' + self.report_model_name)
			log_info.info('\n')
		except:
			log_error('Error for upload report ....')