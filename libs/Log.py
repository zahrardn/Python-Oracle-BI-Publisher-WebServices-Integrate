'''
    File name: Log.py
    Description: use python logging with seperate name and path
    Author: z.raddani
    Date created: 06 October 2018
    Python Version: 2.7
'''
import logging
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