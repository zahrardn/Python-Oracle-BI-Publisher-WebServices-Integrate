'''
    File name: Report.py
    Description: run BI publisher web services from ReportService and use in main.py
    Author: z.raddani
    Date created: 11 October 2019
    Python Version: 2.7
'''
# import zeep
from libs import *
from libs import Security
from libs import Log
# for call webservices
from suds.client import Client
import datetime
import json

class Report:

	def __init__(self,p_system_app_name,p_report_name,p_reports_path,p_output_type,p_layout,p_stored_report_path,p_user,p_doc_file_name):
		try:
			log_info.info('*****************************************************')		
			# wsdl for report category of BIP services 
			wsdl = '/xmlpserver/services/v2/ReportService?wsdl'
			self.client = Client(server_ip+wsdl)
			self.result = ''

			# authenticate
			sec = Security.Security()
			if sec.impersonate(p_user,server_ip,admin_user,admin_password):
				log_info.info('impersonated for ' + p_user + ' ....')
			else:
				log_error.error('impersonate failed for ' + p_user)
				self.result = self.result + 'impersonate failed for ' + p_user

			self.request_data = {
					'reportRequest' : [{
										'attributeCalendar'			: 'Gregorian',
										'attributeFormat'			: p_output_type,
										'byPassCache'				: 'true',
										'attributeLocale'			: locale,
										'attributeTimezone'			: time_zone,
										'attributeTemplate'			: p_layout,
									    'reportAbsolutePath'		: p_reports_path + p_system_app_name + '/REPORTS/' + p_report_name + '.xdo',
									    'flattenXML'				: 'true',
									    'sizeOfDataChunkDownload'	: '-1',
									    'reportOutputPath'			: p_stored_report_path + p_doc_file_name +'.' + p_output_type
									    }],
					'bipSessionToken' : sec.session_token
					#'userID':user,
					#'password':passwrd
					}
			log_info.info('initialed report ' + p_report_name + ' for ' + p_user + '....')
		except:
			self.result = self.result + 'initial report failed'


	# check parameters from issuite with bi publisher
	def check_params(self,p_param_keys):
		try:
			log_info.info('send for BI server for get params....')
			#client = zeep.Client(wsdl=server_ip+self.wsdl)
			response = self.client.service.getReportParametersInSession(**self.request_data)
			defined_params = list(map(str, [ param['name'] for param in response['listOfParamNameValues']['item']]))

			if defined_params != p_param_keys:
				log_error.error('parameter names that sent are different...')
				self.result = self.result + 'parameter names that sent are different...'
				return False

			log_info.info('parameters are the same so it is ok....')
			return True
		except:
			log_error.error('Error Occured! for check params')
			self.result = self.result + 'Error Occured! for check params'
			return False

	def set_params(self,param_name_vals):
		try:
			# create listOfParamNameValues
			parameters_tmp = []
			for p in param_name_vals.keys():

				parameters_tmp.append({ 'multiValuesAllowed' : True,
									   'name'  : p,
									   'refreshParamOnChange' : True,
									   'selectAll' : True,
									   'templateParam' : False,
									   'useNullForAll' :True,
			 						   'values': [{ 'item' : param_name_vals[p].split(',') }] 
			 						   })
			parameters = { 'listOfParamNameValues':[{ 'item' : parameters_tmp }] }
			self.request_data['reportRequest'][0]['parameterNameValues'] = parameters
			log_info.info('added parameter files....')
			return True
		except:
			log_error.error('Error Occured! for set params')
			self.result = self.result + 'Error Occured! for set params'
			return False

	# add parameters to report request and run report
	def run(self,parameters_nam_val):
		#try:
			parameters_nam_val = json.loads(parameters_nam_val)
			if not self.check_params(parameters_nam_val.keys()):
				self.result = self.result + 'check param failed'
				return False

			log_info.info('start run report ....')

			if not self.set_params(parameters_nam_val):
				self.result = self.result + 'set param failed'
				return False
			
			# run service
			log_info.info('send for BI server....')
			#client = zeep.Client(wsdl=server_ip+self.wsdl)
			response = self.client.service.runReportInSession(**self.request_data)
			#response = client.service.runReport(**request_data)

			# store response to file
			log_info.info('saved output file....')
			self.result = 'success'
			log_info.info('*****************************************************')		
			return True
		# except:
		# 	log_error.error('Error Occured! for run report')
		# 	self.result = self.result + 'Error Occured! for run report'
		# 	return False