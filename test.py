import unittest 
from libs import *
from libs import Report
from libs import Catalog
from libs import Schedule
from libs import Security
  
class TestReport(unittest.TestCase): 
  
    def test_run(self):    
    		rep = Report.Report('FND','RFND1600','/ISSUITE/','pdf','def','/u01/bashes/','irisa_radani','unit-test-run-report')
        	self.assertTrue(rep.run('{"p3":"v1","p4":"v2"}'))
  

class TestSchedule(unittest.TestCase): 

    def test_run_history(self):
		sch = Schedule.Schedule('irisa_radani')
		self.assertTrue(sch.run('FND','RFND1600','/ISSUITE/','pdf','def','/u01/bashes/','unit-test-run-schedule','{"p3":"v1","p4":"v2"}','','','','','',''))

		self.assertTrue(sch.job_history('1196','/u01/bashes/','unit-test-history'))

if __name__ == '__main__':

	unittest.main()

	# #if sys.argv[1] == 'run-report':
	# rp = ReportTest()
	# rp.run()

	# #elif sys.argv[1] == 'run-schedule':
	# sc = ScheduleTest()
	# sc.run()

	#elif sys.argv[1] == 'schedule-history':
	#sc.history()