import optparse
import os.path
import MySQLdb
from ConfigParser import SafeConfigParser
import sys

def config(sysargv):
	parser = optparse.OptionParser()

	parser.add_option('-c', '--config', help='the configuration file - default name [%default]', default='config.ini', action='store', type='string', dest='config')
	parser.add_option('-f', '--file', help='the corpus file - mandatory option', dest='corpus')

	(opts, args) = parser.parse_args(args = sysargv[1:])

	if opts.corpus is None:
		print 'A corpus file is needed as the input'
		parser.print_help()
		exit(-1)

	if not os.path.isfile(opts.config):
		print 'Coud not find', opts.config
		print 'Please chek your arguments.'
		exit(-1)

	configParser = SafeConfigParser()
	configParser.read(opts.config)

	dbConfig = {}
	dbConfig['dbHost'] = configParser.get('db_connect', 'host')
	dbConfig['dbUser'] = configParser.get('db_connect', 'username')
	dbConfig['dbPass'] = configParser.get('db_connect', 'password')
	dbConfig['dbSchema'] = configParser.get('db_connect', 'schema')
	dbConfig['dbCharset'] = configParser.get('db_connect', 'charset')
	dbConfig['dbUnicode'] = configParser.get('db_connect', 'useUnicode')

	return opts.corpus, dbConfig

config(sys.argv)

version = '0.1'
