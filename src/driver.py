#!/usr/bin/python3
import os

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
# pdf_drive.py
__version__ = "0.0a"
#
# This is a simple API for handling PDF files based on qpdf
#
# Written by Nicolas Canceill
# Last updated on Sept 28, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
#
#
# CLASSES
#

class PDF_file:

	file_name = ''

	def __init__(self,file_name):
		self.file_name = file_name

	# Generates QDF file "<file>.qdf" from PDF file "<file>", uncompressing streams if needed
	def uncompress(self):
		os.system('qpdf '+self.file_name+' '+self.file_name+'.qdf --qdf --stream-data=uncompress')

	# Generates fixed QDF  file "<file>.fix" from damaged QDF file "<file>", reconstructing XRef and trailer if needed
	def fix(self):
		os.system('fix-qdf <'+self.file_name+' >'+self.file_name+'.fix')

	# Generates PDF file "<file>.pdf" from QDF or PDF file "<file>", compressing streams if needed
	def compress(self):
		os.system('qpdf '+self.file_name+' '+self.file_name+'.pdf --stream-data=compress')
