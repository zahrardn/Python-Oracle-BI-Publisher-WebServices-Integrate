'''
    File name: __init__.py
    Description: Set python global variables
    Author: z.raddani
    Date created: 06 October 2018
    Python Version: 2.7
'''
from Log import *
from libs import Security

admin_user = 'weblogic'
admin_password = 'OBIadmin46726'

server_ip = 'http://172.27.3.15:9502'
server_ip_dest = 'http://172.27.3.15:9502'

info_log_path_name = '/home/zahra/workspace/BI/BIPublisher/logs/info.log'
error_log_path_name = '/home/zahra/workspace/BI/BIPublisher/logs/error.log'
# report
stored_report_path = '/u01/bashes/'
reports_path='/ISSUITE/'

# logging
log_obj = Log.LOG()
log_info = log_obj.use_logging('BI_LOG_INFO',info_log_path_name,logging.INFO)
log_error =log_obj.use_logging('BI_LOG_ERROR',error_log_path_name,logging.ERROR)
