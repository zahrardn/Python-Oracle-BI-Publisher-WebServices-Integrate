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
import pytz

class Schedule:

	def __init__(self,p_user):

		log_info.info('initial schedule ....')
		# wsdl for report category of BIP services 
		wsdl = '/xmlpserver/services/v2/ScheduleService?wsdl'
		self.client = Client(server_ip+wsdl)

		self.sec = Security.Security()
		self.sec.impersonate(p_user,server_ip,admin_user,admin_password)
		log_info.info('impersonated for ' + p_user + ' ....')

		self.user = p_user


	def run(self,p_report_name,p_system_app_name,p_reports_path,p_output_type,p_layout,p_stored_report_path,parameters_nam_val,p_start_date):

		out_stored_path_name = p_stored_report_path + p_report_name + '_' + datetime.datetime.now().strftime ("%Y%m%d%H%M%S") + self.user +'.' + p_output_type

		report = Report.Report(p_report_name,p_system_app_name,p_reports_path,p_output_type,p_layout,p_stored_report_path,self.user)

		if not report.check_params(parameters_nam_val.keys()):
				return False

		log_info.info('start run schedule report ' + p_report_name + ' for ' + self.user + '....')

		if not report.set_params(parameters_nam_val):
			return False

		# set schedule request
		request_schedule = {
				'scheduleRequest' : [{ 
						'deliveryChannels' : [{
											"localOptions": [{'item' : { 'destination' : out_stored_path_name }}]
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
						'reportRequest' 			: report.request_data['reportRequest']

					}],
				'bipSessionToken' : self.sec.session_token 
				}

		log_info.info('send for BI server for schedule report....')
		response = self.client.service.scheduleReportInSession(**request_schedule)
		return True


	def job_history(self,p_job_id):

		request_history = {
			'filter' : {
				'jobName' 	: self.user ,
				'owner'		: self.user,
				'jobId'		: p_job_id
			},
			'beginIdx'		: 1,
			'bipSessionToken' : self.sec.session_token 
		}
		log_info.info('send for BI server for get schedule history....')
		response = self.client.service.getAllScheduledReportHistoryInSession(**request_history)

		start_date = response['jobInfoList']['item'][0]['startDate'].replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Tehran')).strftime('%Y-%m-%d %H:%M:%S')
		end_date = response['jobInfoList']['item'][0]['endDate'].replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Tehran')).strftime('%Y-%m-%d %H:%M:%S')

		report_name = response['jobInfoList']['item'][0]['reportUrl'].rsplit('/', 1)[1][:-4]

		out = response['jobInfoList']['item'][0]['status'] + ',' + str(response['jobInfoList']['item'][0]['jobId']) + ',' + start_date + ',' + end_date + ',' + report_name + ', 0'
		print out
		
		return True