'''
    File name: Security.py
    Description: run BI publisher web services from SecurityService and use in main.py
    Author: z.raddani
    Date created: 11 October 2019
    Python Version: 2.7
'''
from libs import *
# for call webservices
from suds.client import Client
# for logging
import logging

class Security:
	def __init__(self):
		self.wsdl = '/xmlpserver/services/v2/SecurityService?wsdl'
		self.session_token = ''
		#log_info.info('initial security class....')

	# impersonate is like login so return session token, but with admin user access and user named p_user
	def impersonate(self,p_user,p_server_ip,p_admin_user,p_admin_password):
		try:
			#log_info.info('send for BI server....')
			client = Client(p_server_ip+self.wsdl)
			#client = zeep.Client(wsdl=server_ip+self.wsdl)
			self.session_token = client.service.impersonate(p_admin_user,p_admin_password,p_user)
			return True
		except:
			return False