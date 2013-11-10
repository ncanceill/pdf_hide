#!/usr/bin/python3
import logging

#
#
#
# PDF HIDE
#

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
# along with this program.  If not, see [http://www.gnu.org/licenses/].
#
# Copyright (C) 2013 Nicolas Canceill
#

#
# logger.py
__version__ = "0.0"
#
# This is a logging engine for pdf_hide v0.0
#
# Written by Nicolas Canceill
# Last updated on Nov 10, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
#
#
# STATIC
#

LOG_FORMAT = "%(levelname)s:	%(message)s"

CRITICAL=-1
ERROR=0
INFO=1
DEBUG=2

MSG_VERSION = "This is PDF_HIDE v" + __version__
MSG_DESC = """A steganographic tool for hiding data inside PDF files
Hosted at https://github.com/ncanceill/pdf_hide"""
MSG_END = """My job is done!"""
MSG_LICENSE = """PDF_HIDE  Copyright (C) 2013  Nicolas Canceill
Distributed under GNU General Public License v3
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to
redistribute it under certain conditions.
Please see LICENSE.md or http://www.gnu.org/licenses/ for details."""
MSG_BUG = """Maintained by Nicolas Canceill
Please report bugs at https://github.com/ncanceill/pdf_hide
or at nicolas.canceill@ens-cachan.org"""

#
#
# BASIC MESSAGES
#
#

# Print splash screen
def print_splash():
	print("====================")
	print(MSG_VERSION)
	print("====================")

# Print end message
def print_end():
	print(MSG_END)

# Print disclaimer
def print_discl():
	print("")
	print(MSG_LICENSE)
	print("")

# Print maintenance info
def print_maint():
	print("====================")
	print(MSG_BUG)
	print("====================")

# Print a value
def print_val(v):
	if v == None:
		return ""
	m = "\n\t" + v.__class__.__qualname__
	if hasattr(v,'__len__'):
		m = m + "\t[" + str(v.__len__()) + "]"
	return m + "\n\t" + str(v)

#
#
# ROOT LOGGER
#
#

class rootLogger:
	# Set verbosity level at creation time
	def __init__(self,verbose=0):
		logging.basicConfig(format=LOG_FORMAT)
		if verbose == CRITICAL:
			logging.getLogger().setLevel(logging.CRITICAL)
		elif verbose == ERROR:
			logging.getLogger().setLevel(logging.ERROR)
		elif verbose == INFO:
			logging.getLogger().setLevel(logging.INFO)
		self.DEBUG = False
		if verbose >= DEBUG:
			logging.getLogger().setLevel(logging.DEBUG)
			self.DEBUG=True

	def critical(self,msg,val=None):
		logging.critical(msg + print_val(val))
		print_maint()

	def error(self,msg,val=None):
		logging.error(msg + print_val(val))

	def warn(self,msg,val=None):
		logging.warning(msg + print_val(val))

	def info(self,msg,val=None):
		logging.info(msg + print_val(val))

	def debug(self,msg,val=None):
		logging.debug(msg + print_val(val))

	def criticals(self,dict):
		for (m,v) in dict.items():
			self.critical(m,v)

	def errors(self,dict):
		for (m,v) in dict.items():
			self.error(m,v)

	def warns(self,dict):
		for (m,v) in dict.items():
			self.warn(m,v)

	def infos(self,dict):
		for (m,v) in dict.items():
			self.info(m,v)

	def debugs(self,dict):
		for (m,v) in dict.items():
			self.debug(m,v)
