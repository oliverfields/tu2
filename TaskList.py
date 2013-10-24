from os.path import exists
from os import unlink, close, write, rename
from tempfile import mkstemp
from Utility import report_error
from time import strptime
import Task
import re

class TaskList():

	def __init__(self, file):
		self.tasks = []
		self.file = None

		self.load_tasks_from_file(file)


	def load_tasks_from_file(self, file):
		""" Read tasks from file, format 'YYYY-MM-DD HH:MM\t[YYYY-MM-DD HH:MM|-]\tName """

		field_sep="\t"

		try:
			task_file = open(file, 'r')

			try:
				lines = task_file.readlines()
				i=-1
				print_line=i+2
				max_lines=len(lines) - 1

				while True:
					i += 1

					# Break if no lines left
					if i > max_lines:
						break
					# Skip lines that only contain whitespace
					elif lines[i].strip() == '':
						i += 1
						continue

					line=lines[i]
					l=line.split(field_sep)

					if len(l) != 3:
						report_error(1,"Line %s in '%s' is malformed -> %s" % (print_line, file,line))
					else:
						name=l[2]
						start=l[0]
						end=l[1]

					try:
						self.add_task(name, start, end)
					except Exception, e:
						print(e)
						report_error(1,"Unable to load task from line %s in '%s' -> %s" % (print_line, file,line))

			finally:
				task_file.close()

		except IOError:
			report_error(1,"Unable to open file '%s'" % file)

	def add_task(self, name, start, end):
		""" Add task to list """

		task=Task.Task(name, start, end)
		self.tasks.append(task)


	def save_tasks_to_file(self, file):
		""" Write tasks to file securely. Write to tmp file first, once ok rename original file to .bak, rename temp file to orginal file name and finally delete .bak if all swell """

		if file=='/dev/stdin':
			for task in self.tasks:
				print(task.serialize())
		else:
			tmp_file=file+'.tmp'
			backup_file=file+'.bak'

			f=open(tmp_file, 'w')

			for task in self.tasks:
				f.write('%s\n' % task.serialize())
			f.close()

			# Load temporary file to check ok
			try:
				tl=TaskList(tmp_file)
			except Exception, e:
				report_error(1,"Failure creating temporary file")

			rename(file, backup_file)
			rename(tmp_file, file)
			unlink(backup_file)