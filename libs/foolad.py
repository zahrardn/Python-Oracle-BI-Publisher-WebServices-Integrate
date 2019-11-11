'''me: Report.py
    Description: run BI publisher web services from ReportService and use in main.py
    Author: z.raddani
    Date created: 06 October 2018
    Python Version: 2.7
'''
#import zeep
import datetime
#from libs import *
import logging 
from suds.client import Client
import sys
import re
import json
import datetime
#from Log import *

user = 'weblogic'
passwrd = 'OBIadmin46726'
server_ip = 'http://172.25.67.64:9502'
server_ip_dest = 'http://172.25.67.64:9502'
info_log_path_name = '/u01/bashes/test-py/info.log'
error_log_path_name = '/u01/bashes/test-py/error.log'
 # report
stored_report_path = '/u01/bashes/test-py/'
logging.basicConfig(filename=info_log_path_name)

class LOG:
	def use_logging(self,log_name,log_path_name,level):
		log           = logging.getLogger(log_name)
		log_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

		# comment this to suppress console output
		stream_handler = logging.StreamHandler()
		stream_handler.setFormatter(log_formatter)
		log.addHandler(stream_handler)

		file_handler_info = logging.FileHandler(log_path_name)
		file_handler_info.setFormatter(log_formatter)
		log.addHandler(file_handler_info)
		log.setLevel(level)
		return log

log_obj = LOG()
log_info = log_obj.use_logging('BI_LOG_INFO',info_log_path_name,logging.INFO)
log_error =log_obj.use_logging('BI_LOG_ERROR',error_log_path_name,logging.ERROR)

class Security:
	def __init__(self):
		self.wsdl = '/xmlpserver/services/v2/SecurityService?wsdl'
		self.session_token = ''
		log_info.info('initial security class....')

	def impersonate(self):
		log_info.info('send for BI server....')
		client = Client(server_ip+self.wsdl)
		#client = zeep.Client(wsdl=server_ip+self.wsdl)
		self.session_token = client.service.impersonate("biptrans","biptrans@123","irisa_radani")

class Report:
	def __init__(self,report_name,system_app_name):
		print datetime.datetime.now()
		self.report_name = report_name
		self.system_app_name = system_app_name
		self.wsdl = '/xmlpserver/services/v2/ReportService?wsdl'
		sec = Security()
		sec.impersonate()
		self.session_token = sec.session_token
		log_info.info('initial report class....')

	def get_params(self):
		request_data = {
				'reportRequest' : [{
									'attributeCalendar'			: 'Gregorian',
									'attributeFormat'			: 'pdf',
									'byPassCache'				: 'true',
									'attributeLocale'			: 'fa-IR',
								    'reportAbsolutePath'		: '/ISSUITE/' + self.system_app_name + '/REPORTS/' + self.report_name + '.xdo',
								    'flattenXML'				: 'false',
								    'sizeOfDataChunkDownload'	: '-1'
								    }],
				'bipSessionToken' : self.session_token
				#'userID':user,
				#'password':passwrd
				}
		log_info.info('send for BI server for params....')
		client = Client(server_ip+self.wsdl)
		#client = zeep.Client(wsdl=server_ip+self.wsdl)
		response = client.service.getReportParametersInSession(**request_data)


	def run(self,parameters_nam_val,stored_report_path):
		#try:
			log_info.info('start run report for ' + self.report_name + '....')
			stored_report_path_name = stored_report_path + self.report_name + '_' + datetime.datetime.now().strftime ("%Y%m%d%H%M%S") +'.pdf'
			# create listOfParamNameValues
			parameters_tmp = []
			for p in parameters_nam_val.keys():
				parameters_tmp.append({ 'multiValuesAllowed' : False,
									   'name'  : 'p1',
									   'refreshParamOnChange' : True,
									   'selectAll' : False,
									   'templateParam' : False,
									   'useNullForAll' :False,
			 						   'values': [{ 'item' : parameters_nam_val[p] }] 
			 						   })
			parameters = { 'listOfParamNameValues':[{ 'item' : parameters_tmp }] }
			#print(parameters)
			# create request data
			request_data = {
				'reportRequest' : [{
									'attributeCalendar'			: 'Gregorian',
									'attributeFormat'			: 'pdf',
									'byPassCache'				: 'true',
									'attributeLocale'			: 'fa-IR',
									'parameterNameValues'		: parameters,
								    'reportAbsolutePath'		: '/ISSUITE/' + self.system_app_name + '/REPORTS/' + self.report_name + '.xdo',
								    'flattenXML'				: 'false',
								    'sizeOfDataChunkDownload'	: '-1',
								    'reportOutputPath'			:  stored_report_path + 'a.pdf'
								    }],
				'bipSessionToken' : self.session_token
				#'userID':user,
				#'password':passwrd
				}

			self.get_params()
			# run service
			log_info.info('send for BI server....')
			client = Client(server_ip+self.wsdl)
			#client = zeep.Client(wsdl=server_ip+self.wsdl)
			response = client.service.runReportInSession(**request_data)
			#response = client.service.runReport(**request_data)

			# store response to file
			log_info.info('crete output file....')

			# if response['reportBytes'] != None:
			# 	file = open('222.pdf','w+b')#stored_report_path_name, 'w+b')
			# 	file.write(response['reportBytes'])
			# 	file.close()
			# 	log_info.info('Successful run report ' + self.report_name + ' :)')
			# 	log_info.info('\n')
			# 	print datetime.datetime.now()
			# else:
			# 	log_error.error('None response error ')
		
		#except:
			#log_error.error('Error Occured! for run report')

all_services = {'report' : {'run'}, 'catalog' : {'trans'},'schedule' : {}}
# if __name__ == '__main__':
if 1==1:
     #try:
     if sys.argv[1] == 'report':
         if sys.argv[2] == 'run':
             data_tmp = re.match(r"""R(\w{3})(\d*)""",sys.argv[3])
             if data_tmp:
                 #try:
                 rep = Report(data_tmp.group(0),data_tmp.group(1))
                 ###########run report ################
                 rep.run(json.loads(sys.argv[4]),stored_report_path)
                 # except:
                 #       log_error.error('''Error: 4th param should be report parameters like => '{"param1":"value1","param2":"value2"}' ''')
                 #       log_error.error('''Script syntax is: python main.py report run RFND3000 '{"p1":"S","p2":""}' ''')
             else:
                 log_error.error('Error: 3nd parameter should be report name.')
         else:
             log_error.error('''Error:2nd parameter should be in ''' + json.dumps(list(all_services[sys.argv[1]])))

