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
__version__ = "0.0a"
#
# This is a logging engine for pdf_hide v0.0a
#
# Written by Nicolas Canceill
# Last updated on Sept 29, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
#
#
# STATIC
#

MSG_VERSION = "This is PDF_HIDE v" + __version__
MSG_DESC = "A steganographic tool for hiding data inside PDF files"
MSG_LICENSE = """PDF_HIDE  Copyright (C) 2013  Nicolas Canceill
Distributed under GNU General Public License v3
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
Please see LICENSE.md or http://www.gnu.org/licenses/"""

#
#
#
# CLASSES
#

class rootLogger:
	DEBUG = False
	VERBOSE = 0

	def print_splash(parser):
		if VERBOSE >= 0 : print("====================")
		print MSG_VERSION
		if VERBOSE >= 0 : print("====================")

	def print_discl(parser):
		if VERBOSE >= 0 : print("====================")
		print MSG_LICENSE
		if VERBOSE >= 0 : print("====================")
