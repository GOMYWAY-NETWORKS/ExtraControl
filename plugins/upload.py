#!/usr/bin/env python
# encoding: utf-8
#
# ExtraControl - Aruba Cloud Computing ExtraControl
# Copyright (C) 2012 Aruba S.p.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import argparse
from tools import *
import os

def main():
	parser = argparse.ArgumentParser(add_help=True, prog='upload')
	subparsers = parser.add_subparsers(title='subcommands', help='valid subcommands', dest="sub_command")
	
	usermodule = subparsers.add_parser('usermodule')
	usermodule.add_argument("module", help="module name")
	usermodule.add_argument("new_module", help="path to module", nargs="+")
	
	help = subparsers.add_parser('help')
	args = parser.parse_args()
	
	if args.sub_command == 'help':
		usermodule.print_help()
		return 0

	m = moduleFromNameAndType(args.module, MODULE_CUSTOMS)
	
	if m != None:
		print "Module already exists"
		return 1
		
	new_module = args.new_module[0]
	
	if new_module.lower().startswith('http'):
		def logTransfer(count, block, size):
			pass
		print "Downloading:", new_module
		try:
			filename, headers = urllib.urlretrieve(new_module, reporthook=logTransfer)
			new_module = filename
		except IOError, msg:
			print "Error: %s" % msg
			return 1
		except:
			print "File too short"
			return 1
		print '\nDownloaded:', filename
		print 'Headers:\n', headers
	else:
		if not os.path.exists(new_module):
			print "Update file not found"
			return 1
	
	custom_dir = getCustomDirectory()

	beforeFileUpdate()
		
	try:
		os.mkdir(custom_dir)
	except OSError, msg:
		pass

	update_path = os.path.join(custom_dir, args.module)
	copyModule(new_module, update_path)

	afterFileUpdate()

	print 'Done'
	return 0
	
if __name__ == "__main__":
	sys.exit(main())
