from Utility import report_error
from datetime import datetime, timedelta
from time import strftime, mktime

class Task:

	def __init__(self, name, start=datetime.now(), end='-'):
		self.name = name.strip()
		self.start = start
		self.end = end


	@property
	def has_end_time(self):
		""" Boolean if task has end time or not """
		if self.end[-1:]=='-':
			return True
		else:
			return False


	@property
	def in_progress(self):
		""" Boolean if current time within task start and end time """
		now=mktime(datetime.now().timetuple())

		if now >= self.start_unixtimestamp and now <= self.end_unixtimestamp:
			return True
		else:
			return False


	@property
	def start_unixtimestamp(self):
		try:
			dt=datetime.strptime(self.start, '%Y%m%d %H%M')
			return mktime(dt.timetuple())
		except ValueError:
			raise Exception("Invalid start time '%s'" % self.start)


	@property
	def end_unixtimestamp(self):
		if self.has_end_time:
			dt=datetime.now()
		else:
			try:
				dt=datetime.strptime(self.end, '%Y%m%d %H%M')
				return mktime(dt.timetuple())
			except ValueError:
				raise  ValueError("Invalid end time '%s'" % self.end)


	@property
	def duration(self):
		""" Calculate time between start and end timestamps """

		start_ts=self.start_unixtimestamp
		end_ts=self.end_unixtimestamp

		# If start time in future and no end time cannot compute
		# duration, else assume end is now
		if self.has_end_time and start_ts >= end_ts:
			duration=0
		elif start_ts > end_ts:
			report_error(1,'Start date cannot be greater than end date (%s - %s)' % (start_datetime, end_datetime))
		else:
			duration=int(end_ts - start_ts)

		return duration


	def serialize(self):
		""" Write task as string """

		return '%s\t%s\t%s' % (self.start, self.end, self.name)