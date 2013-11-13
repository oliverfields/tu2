''' General utility library '''
import sys
import os


def report_error(code, message):
	sys.stderr.write('Error: %s\n' % message)
	sys.exit(code)


def report_warning(message):
	print 'Warning: %s' % message


def report_notice(message):
	print 'Notice: %s' % message


def usage(mode='default'):
	""" Print usage message """
	executable_name = os.path.basename(sys.argv[0])

	usage_message = {
		'add': ' <task> [HHMM|now][-HHMM|-now] <file|stdin>',
		'close': ' [HHMM] <file|stdin>',
		'report': ' <file|stdin>',
		'current': ' <file|stdin>',
	}

	if mode == 'default':
		modes = ''
		for key, message in usage_message.items():
			modes = '%s|%s' % (key, modes)

		modes = modes.lstrip('|')
		modes = modes.rstrip('|')
		print 'Usage: %s [%s] <arguments>' % (executable_name, modes)
	else:
		print 'Usage: %s %s%s' % (executable_name, mode, usage_message[mode])


