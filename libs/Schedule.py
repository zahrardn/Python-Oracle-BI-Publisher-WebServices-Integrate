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
		try:			
			# wsdl for report category of BIP services 
			wsdl = '/xmlpserver/services/v2/ScheduleService?wsdl'
			self.client = Client(server_ip+wsdl)
			self.result = ''

			# authenticate
			self.sec = Security.Security()
			if self.sec.impersonate(p_user,server_ip,admin_user,admin_password):
				log_info.info('impersonated for ' + p_user + ' ....')
			else:
				log_error.error('impersonate failed for ' + p_user)
				self.result = self.result + 'impersonate failed for ' + p_user

			self.user = p_user
			log_info.info('initialed schedule ....')
		except:
			self.result = self.result + 'initial schedule failed'


	def run(self,p_system_app_name,p_report_name,p_reports_path,p_output_type,p_layout,p_stored_report_path,p_doc_file_name,p_parameters_nam_val,p_start_date):

		try:
			out_stored_path_name = p_stored_report_path + p_doc_file_name +'.' + p_output_type

			report = Report.Report(p_system_app_name,p_report_name,p_reports_path,p_output_type,p_layout,p_stored_report_path,self.user,p_doc_file_name)

			if not report.check_params(p_parameters_nam_val.keys()):
				self.result = self.result + report.result
				return False

			log_info.info('start run schedule report ' + p_report_name + ' for ' + self.user + '....')

			if not report.set_params(p_parameters_nam_val):
				self.result = self.result + report.result
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
							'jobTZ'						: time_zone,
							'startDate'					: p_start_date,
							'jobLocale'					: locale,
							'repeatCount'				: 0,
							'useUTF8Option'				: True,
							'userJobName'				: self.user,
							'reportRequest' 			: report.request_data['reportRequest']

						}],
					'bipSessionToken' : self.sec.session_token 
					}

			log_info.info('send for BI server for schedule report....')
			self.result = self.client.service.scheduleReportInSession(**request_schedule)
			#self.result = 'success'
			return True
		except:
			log_error.error('Error Occured! for schedule report')
			self.result = self.result + 'Error Occured! for schedule report'


	def job_history(self,p_job_id,p_out_path,p_out_file_name):

		#try:
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

			start_date = response['jobInfoList']['item'][0]['startDate'].replace(tzinfo=pytz.utc).astimezone(pytz.timezone(time_zone)).strftime('%Y-%m-%d %H:%M:%S')
			end_date = response['jobInfoList']['item'][0]['endDate'].replace(tzinfo=pytz.utc).astimezone(pytz.timezone(time_zone)).strftime('%Y-%m-%d %H:%M:%S')

			report_name = response['jobInfoList']['item'][0]['reportUrl'].rsplit('/', 1)[1][:-4]

			out = response['jobInfoList']['item'][0]['status'] + ',' + str(response['jobInfoList']['item'][0]['jobId']) + ',' + start_date + ',' + end_date + ',' + report_name + ', 0'
			
			#f = open(p_out_path + p_out_file_name, "w")
			f = open('/home/zahra/workspace/BI/BIPublisher/' + p_out_file_name, "w")
			f.write(out)
			f.close()

			self.result = 'success'
			return True
		# except:
		# 	log_error.error('Error Occured! for schedule history report')
		# 	self.result = self.result + 'Error Occured! for schedule history report'