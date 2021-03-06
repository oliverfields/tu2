''' CLI modes '''

from datetime import datetime
import sys
import TaskList
from Utility import usage, report_error
import re
import time


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

	close_tasks_prompt(tl, start[9:13])

	tl.add_task(name, start, end)

	tl.save_tasks_to_file(file)


def close_mode():
	""" Close open tasks """
	end_time_arg=None
	end_time_user_input=None

	if len(sys.argv) == 3:
		file=sys.argv[2]
	elif len(sys.argv) == 4:
		end_time_arg=sys.argv[2]
		file=sys.argv[3]
	else:
		usage('close')
		report_error(1, 'Wrong number of arguments')

	if file=='-':
		file='/dev/stdin'

	tl=TaskList.TaskList(file)

	close_tasks_prompt(tl, end_time_arg)

	tl.save_tasks_to_file(file)


def close_tasks_prompt(tasklist, end_time_arg=None):
	""" Loop over open tasks and offer option to close them """

	today=datetime.now()

	for task in tasklist.tasks:
		current_date=today.strftime('%Y%m%d')

		if end_time_arg != None:
			current_time = end_time_arg
		else:
			current_time=today.strftime('%H%M')

		if task.has_end_time == False:

			stdt=datetime.fromtimestamp(task.start_unixtimestamp).strftime('%Y%m%d')

			# If start date is not today
			if stdt != current_date:
				print("Task '%s' was started on %s at %s\nEnter end date and time as 'YYYYMMDD HHMM' or HHMM for %s HHMM or blank for %s %s, 'i' ignores, Ctrl+C quits:" % (task.name, datetime.fromtimestamp(task.start_unixtimestamp).strftime('%Y%m%d'), datetime.fromtimestamp(task.start_unixtimestamp).strftime('%H%M'), datetime.fromtimestamp(task.start_unixtimestamp).strftime('%Y%m%d'), current_date, current_time))

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
						phours = re.compile('[0-2][0-9][0-6][0-9]$')
						pdatehours = re.compile('^2[0-9][0-9][0-9][0-1][0-9][0-3][0-9] [0-2][0-9][0-6][0-9]$')
						if phours.match(end_time_user_input):
							task.end='%s %s' % (stdt, end_time_user_input)
							break
						elif pdatehours.match(end_time_user_input):
							task.end=end_time_user_input
							break
						else:
							print('Invalid format, must be YYYYMMDD HHMM')

			# If start date is today
			else:

				print("Task '%s' started on %s at %s\nEnter end time as 'HHMM' or blank for %s, 'i' ignores, Ctrl+C quits:" % (task.name, datetime.fromtimestamp(task.start_unixtimestamp).strftime('%Y%m%d'), datetime.fromtimestamp(task.start_unixtimestamp).strftime('%H%M'), current_time))

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
							print('Invalid format, must be HHMM')


def report_mode():
	""" Compile report showing time spent on each task """

	no_end_time='?'
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

	for task in tl.tasks:
		i+=1

		if task.has_end_time:
			no_end_time=''
		else:
			no_end_time='?'

		hours='%sh%s' % (tl.duration_pretty(task.duration), no_end_time)

		report_lines.append({'date': datetime.fromtimestamp(task.start_unixtimestamp).strftime('%Y%m%d'), 'duration': hours, 'name': task.name})

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

	print('\n%sh between %s and %s @ %s' % (tl.duration_pretty(tl.total_duration), first_date, last_date, datetime.now().strftime('%Y%m%d %H:%M')))


def current_mode():
	""" Print tasks that are currently in progress """

	if len(sys.argv) != 3:
		usage('current')
		report_error(1, 'Wrong number of arguments')

	file=sys.argv[2]

	if file=='-':
		file='/dev/stdin'

	tl = TaskList.TaskList(file)

	for task in tl.tasks:
		if task.in_progress:
			if task.has_end_time:
				end_time='%s:%s' % (datetime.fromtimestamp(task.end_unixtimestamp).strftime('%H'), datetime.fromtimestamp(task.end_unixtimestamp).strftime('%M'))
			else:
				end_time=datetime.now().strftime('%H:%M?')

			print('%s (%s:%s-%s, %sh)' % (task.name, datetime.fromtimestamp(task.start_unixtimestamp).strftime('%H'), datetime.fromtimestamp(task.start_unixtimestamp).strftime('%M'), end_time, tl.duration_pretty(task.duration)))