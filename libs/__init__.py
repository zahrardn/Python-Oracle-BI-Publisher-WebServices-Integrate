'''
    File name: __init__.py
    Description: Set python global variables
    Author: z.raddani
    Date created: 06 October 2018
    Python Version: 2.7
'''
from Log import *
from libs import Security
import random

admin_user = 'adminuser'
admin_password = 'adminpassword'

server_ip = 'http://[ip:port]'

info_log_path_name = '/home/zahra/workspace/BI/BIPublisher/logs/info.log'
error_log_path_name = '/home/zahra/workspace/BI/BIPublisher/logs/error.log'

log_path = '/home/zahra/workspace/BI/BIPublisher/'

time_zone = "Asia/Tehran"
locale	  = "fa-IR"
# logging
log_obj = Log.LOG()
log_info = log_obj.use_logging('BI_LOG_INFO',info_log_path_name,logging.INFO)
log_error =log_obj.use_logging('BI_LOG_ERROR',error_log_path_name,logging.ERROR)

log_id = str(random.randint(1000,9999))+'	'
