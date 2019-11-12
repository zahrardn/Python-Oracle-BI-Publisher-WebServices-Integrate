
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
			#f = open(sys.argv[8] + sys.argv[12], "w")
			f = open('/home/zahra/workspace/BI/BIPublisher/' + sys.argv[12], "w")
			f.write(rep.result)
			f.close()

		else:
			log_error.error('''Error:2nd parameter should be in ''' + json.dumps(list(all_services[sys.argv[1]])))

	elif sys.argv[1] == 'schedule':
		if sys.argv[2] == 'run':
			# 3: FND, 4: RFND1600, 5:/ISSUITE/, 6:pdf, 7:layout-def 8:stored_path, 9:user, 10:doc_file_name , 11:params => '{"p3":"v1","p1":"v2"}', 12:start_date 13:log_file_name
			# report run FND RFND1600 /ISSUITE/ pdf def /u01/bashes/ irisa_radani abc '{"p3":"v1","p1":"v2"}' '' def.log
			############ schedule #############
			sch = Schedule.Schedule(sys.argv[9])
			if sch.run(sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[10],json.loads(sys.argv[11]),sys.argv[12]):
				log_info.info(sch.result)
			else:
				log_error.error(sch.result)

			# make result file
			#f = open(sys.argv[8] + sys.argv[13], "w")
			f = open('/home/zahra/workspace/BI/BIPublisher/' + sys.argv[13], "w")
			f.write(sch.result)
			f.close()

		elif sys.argv[2] == 'history':
			# 3: irisa_radani, 4:job_id, 5:out_path, 6: out_name, 7:log_name
			sch = Schedule.Schedule(sys.argv[3])
			if sch.job_history(sys.argv[4],sys.argv[5],sys.argv[6]):
				log_info.info(sch.result)
			else:
				log_error.error(sch.result)

			# make result file
			#f = open(sys.argv[5] + sys.argv[7], "w")
			f = open('/home/zahra/workspace/BI/BIPublisher/' + sys.argv[7], "w")
			f.write(sch.result)
			f.close()

	else:
		log_error.error('Error to choose type from '+ json.dumps(all_services.keys()))
	# except:
	# 	log_error.error('error')
