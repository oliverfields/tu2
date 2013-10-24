from Utility import report_error
from datetime import datetime, timedelta
from time import strftime, mktime

class Task:

	def __init__(self, name, start=datetime.now(), end='-'):
		self.name = name.strip()
		self.start = start
		self.end = end


	@property
	def duration(self):
		""" Calculate time between start and end timestamps """

		if self.end[-1:] == '-':
			end_datetime=datetime.now()
		else:
			try:
				end_datetime=datetime.strptime(self.end, '%Y%m%d %H%M')
			except ValueError:
				raise  ValueError("Invalid end time '%s'" % self.end)

		try:
			start_datetime=datetime.strptime(self.start, '%Y%m%d %H%M')
		except ValueError:
			raise Exception("Invalid start time '%s'" % self.start)


		# Create unix timestamp
		start_ts=mktime(start_datetime.timetuple())
		end_ts=mktime(end_datetime.timetuple())

		#Check start before end
		if start_ts > end_ts:
			report_error(1,'Start date cannot be greater than end date (%s - %s)' % (start_datetime, end_datetime))

		duration=int(end_ts - start_ts)

		return duration


	def serialize(self):
		""" Write task as string """

		return '%s\t%s\t%s' % (self.start, self.end, self.name)