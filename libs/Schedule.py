'''
    File name: Schedule.py
    Description: schedule BI publisher web services from ScheduleService and use in main.py
    Author: z.raddani
    Date created: 06 October 2018
    Python Version: 2.7
'''
# import zeep
from libs import *

from libs import Log
from libs import Report
# for call webservices
from suds.client import Client
import datetime

class Schedule:

	def __init__(self,p_report_name,p_system_app_name,p_reports_path,p_output_type,p_layout,p_stored_report_path,p_user):

		log_info.info('initial schedule ' + p_report_name + ' for ' + p_user + '....')
		# wsdl for report category of BIP services 
		wsdl = '/xmlpserver/services/v2/ScheduleService?wsdl'
		self.client = Client(server_ip+wsdl)

		self.sec = Security.Security()
		self.sec.impersonate(p_user,server_ip,admin_user,admin_password)
		log_info.info('impersonated for ' + p_user + ' ....')

		self.out_stored_path_name = p_stored_report_path + p_report_name + '_' + datetime.datetime.now().strftime ("%Y%m%d%H%M%S") + p_user +'.' + p_output_type
		self.user = p_user
		
		self.report = Report.Report(p_report_name,p_system_app_name,p_reports_path,p_output_type,p_layout,p_stored_report_path,p_user)


	def run(self,parameters_nam_val,p_start_date):

		if not self.report.check_params(parameters_nam_val.keys()):
				return False

		log_info.info('start run report ....')

		if not self.report.set_params(parameters_nam_val):
			return False

		# set schedule request
		request_schedule = {
				'scheduleRequest' : [{ 
						'deliveryChannels' : [{
											"localOptions": [{'item' : { 'destination' : self.out_stored_path_name }}]
											}],
						#'notificationTo' : 'a@gmail.com',
						'saveDataOption' 			: True,
						'saveOutputOption' 			: True,
						'scheduleBurstringOption' 	: False,
						'schedulePublicOption' 		: True,
						'jobTZ'						: "Asia/Tehran",
						'startDate'					: p_start_date,
						'jobLocale'					: "fa-IR",
						'repeatCount'				: 0,
						'useUTF8Option'				: True,
						'userJobName'				: self.user,
						'reportRequest' 			: self.report.request_data['reportRequest']

					}],
				'bipSessionToken' : self.sec.session_token 
				}

		log_info.info('send for BI server for schedule report....')
		self.client.service.scheduleReportInSession(**request_schedule)
		return True