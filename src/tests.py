#!/usr/bin/python3

import unittest
import pdf_hide
import os

#
#
#
# PDF HIDE
#

#
# DISCLAIMER: This software is provided for free, with full copyrights, and without any warranty.
#

#
# pdf_hide.py
__version__ = "0.0a"
#
# This is a collection of tests for the tool
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

class DependenciesTestCase(unittest.TestCase):
	def test_dep_pdflatex(self):
		self.assertEqual(os.system('which pdflatex > /dev/null'),0)

	def test_dep_qpdf(self):
		self.assertEqual(os.system('which qpdf > /dev/null'),0)

class GenericTestCase(unittest.TestCase):
	def test_gen_proghelp(self):
		self.assertEqual(os.system('./pdf_hide.py -h > /dev/null'),0)

#
#
#
# SCRIPT
#

if __name__ == '__main__':
    unittest.main(verbosity=2)
