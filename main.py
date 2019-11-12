
'''
    File name: main.py
    Description: Run scripts that end user run... this use classes exists in libs
    Author: z.raddani
    Date created: 06 October 2018
    Python Version: 2.7
    Example : python /u01/bashes/BIPublisher/main.py report run RFND1600 '{"a":"a"}'
    		  python main.py catalog trans RFND1600 report
    		  python main.py schedule
'''
#import zeep
import sys
import re
import json
import datetime
from libs import *
from libs import Report
from libs import Catalog
from libs import Schedule
from libs import Security

all_services = {'report' : {'run'}, 'catalog' : {'trans'},'schedule' : {}}
if __name__ == '__main__':
	#try:
	if sys.argv[1] == 'report':
		if sys.argv[2] == 'run':

			# 3: FND, 4: RFND1600, 5:/ISSUITE/, 6:pdf, 7:layout-def 8:stored_path, 9:user, 10:doc_file_name , 11:params => '{"p3":"v1","p1":"v2"}', 12:log_file_name
			# report run FND RFND1600 /ISSUITE/ pdf def /u01/bashes/ irisa_radani abc '{"p3":"v1","p1":"v2"}' def.log
			rep = Report.Report(sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10])
			###########run report ################
			if rep.run(json.loads(sys.argv[11])):
				log_info.info(rep.result)
			else:
				log_error.error(rep.result)
			# make result file
			#f = open(stored_report_path + sys.argv[12], "w")
			f = open('/home/zahra/workspace/BI/BIPublisher/' + sys.argv[12], "w")
			f.write(rep.result)
			f.close()

		else:
			log_error.error('''Error:2nd parameter should be in ''' + json.dumps(list(all_services[sys.argv[1]])))
	# elif sys.argv[1] == 'catalog':
	# 	if sys.argv[2] == 'trans':
	# 		data_tmp = re.match(r"""R(\w{3})(\d*)""",sys.argv[3])
	# 		if data_tmp and sys.argv[4] in ['report','model']:
	# 			try:
	# 				cat = Catalog.Catalog(data_tmp.group(0),data_tmp.group(1))
	# 				########### trans ###############
	# 				cat.trans(sys.argv[4])
	# 			except:
	# 				log_error.error('''Script syntax is: python main.py catalog trans RFND3000 report''')
	# 		else:
	# 			log_error.error('''Script syntax is: python main.py catalog trans RFND3000 report''')
	# 	else:
	# 		log_error.error('''Error:2nd parameter should be in ''' + json.dumps(list(all_services[sys.argv[1]])))
	elif sys.argv[1] == 'schedule':
		if sys.argv[2] == 'run':
			data_tmp = re.match(r"""R(\w{3})(\d*)""",sys.argv[3])
			if data_tmp:
				############ schedule #############
				sch = Schedule.Schedule('irisa_radani')
				if sch.run(data_tmp.group(0),data_tmp.group(1),reports_path,'pdf','def',stored_report_path,json.loads(sys.argv[4]),''):
					log_info.info('success :)')
		elif sys.argv[2] == 'history':
			sch = Schedule.Schedule('irisa_radani')
			if sch.job_history(json.loads('1188')):
				log_info.info('success :)')

	else:
		log_error.error('Error to choose type from '+ json.dumps(all_services.keys()))
	# except:
	# 	log_error.error('error')
