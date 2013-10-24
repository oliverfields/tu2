''' CLI modes '''

from datetime import datetime
from time import strptime
import sys
import TaskList
from Utility import usage, report_error
import re

def make_time(argument):
	""" Convert command line argument string to datetime object """

	today= datetime.now()

	if argument == 'now':
		hour=today.hour
		min=today.minute
	else:
		hour=int(argument[:2])
		min=int(argument[2:])

	try:
		timestamp=datetime(today.year, today.month, today.day, hour, min, 0)
		return timestamp.strftime("%Y%m%d %H%M")
	except Exception, e:
		usage('add')
		report_error(1,'Time argument has wrong format')


def add_mode():
	""" Add new task to task list """

	period=None
	file=None
	start=make_time('now')
	end='-'

	if len(sys.argv) == 4:
		name=sys.argv[2]
		file=sys.argv[3]
	elif len(sys.argv) == 5:
		name=sys.argv[2]
		period=sys.argv[3]
		file=sys.argv[4]
	else:
		usage('add')
		report_error(1, 'Wrong number of arguments')

	if file=='-':
		file='/dev/stdin'

	if period != None:
		period_split=period.split('-')

		start=make_time(period_split[0])

		if len(period_split) == 2:
			end=make_time(period_split[1])

	tl = TaskList.TaskList(file)
	tl.add_task(name, start, end)

	tl.save_tasks_to_file(file)


def close_mode():
	""" Loop over open tasks and offer option to close them """

	current_date=datetime.now().strftime('%Y%m%d')
	end_time_user_input=None

	if len(sys.argv) != 3:
		usage('close')
		report_error(1, 'Wrong number of arguments')

	file=sys.argv[2]

	if file=='-':
		file='/dev/stdin'

	tl = TaskList.TaskList(file)

	for task in tl.tasks:
		current_time=datetime.now().strftime('%H%M')
		if task.end[-1:]=='-':

			print("Task '%s' started on %s at %s\nEnter end time as 'HHMM' or blank for %s, 'i' ignores, Ctrl+C quits:" % (task.name, task.start[:8], task.start[9:13], current_time))

			while True:
				try:
					end_time_user_input=raw_input('-> ')
				except KeyboardInterrupt:
					print('\n')
					sys.exit(0)

				if end_time_user_input=='':
					task.end='%s %s' % (current_date, current_time)
					break
				elif end_time_user_input == 'i':
					break
				else:
					p = re.compile('^[0-2][0-9][0-6][0-9]$')
					if p.match(end_time_user_input):
						task.end='%s %s' % (current_date, end_time_user_input)
						break
					else:
						print('Invalid time format, must be HHMM')

	tl.save_tasks_to_file(file)


def duration_pretty(seconds):
	""" Pretty print duration """

	hours, remainder=divmod(seconds, 3600)
	mins, secs=divmod(remainder, 60)

	rounded_mins=str(round(float(mins) / float(60),1))[2:]

	#pretty_string='%s.%s\t%s:%s' % (hours, rounded_mins, hours, mins)
	pretty_string='%s.%s' % (hours, rounded_mins)

	return pretty_string


def report_mode():
	""" Compile report showing time spent on each task """

	no_end_time='?'
	total_secs=0
	report_lines=[]
	max_length=5
	first_date=None
	last_date=None
	i=0

	if len(sys.argv) != 3:
		usage('report')
		report_error(1, 'Wrong number of arguments')

	file=sys.argv[2]

	if file=='-':
		file='/dev/stdin'

	tl = TaskList.TaskList(file)

	#print('Date      Hours    Name\n----      -----    ----')

	for task in tl.tasks:
		i+=1
		try:
			total_secs+=task.duration
		except ValueError as e:
			report_error(1, "%s in '%s' on line %s " % (e, file, i))

		if task.end[-1:] == '-':
			no_end_time='?'
		else:
			no_end_time=' '

		hours='%sh%s' % (duration_pretty(task.duration), no_end_time)

		report_lines.append({'date': task.start[:8], 'duration': hours, 'name': task.name})

		if max_length < len(hours):
			max_length=len(hours)

	for line in report_lines:
		if first_date>line['date'] or first_date==None:
			first_date=line['date']

		if last_date<line['date'] or last_date==None:
			last_date=line['date']

		line['duration']=line['duration'].rjust(max_length)

	for line in report_lines:
		print('%s   %s   %s' % (line['date'], line['duration'], line['name']))

	print('\nTotal %sh, period %s - %s @ %s' % (duration_pretty(total_secs), first_date, last_date, datetime.now().strftime('%Y%m%d %H%M')))


def current_mode():
	""" Print tasks not closed (no end time) """

	if len(sys.argv) != 3:
		usage('current')
		report_error(1, 'Wrong number of arguments')

	file=sys.argv[2]

	if file=='-':
		file='/dev/stdin'

	tl = TaskList.TaskList(file)

	for task in tl.tasks:
		if task.end[-1:]=='-':
			print('%s (started %s:%s, %sh ago)' % (task.name, task.start[8:11], task.start[11:13], duration_pretty(task.duration)))
