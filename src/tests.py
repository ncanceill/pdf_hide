#!/usr/bin/python3
import unittest
import os
import pdf_algo

#
#
#
# PDF HIDE
#

#
# DISCLAIMER: This software is provided for free, with full copyrights, and without any warranty.
#

#
# chaos.py
__version__ = "0.0a"
#
# This is a straightforward implementation of chaotic maps
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

class AlgoDefaultTestCase(unittest.TestCase):
	def test_algodef_embed(self):
		ps = pdf_algo.PDF_stego("../sample/test.pdf",False,False,0.1,4,False)
		self.assertTrue(ps.embed("123456ThisIsA=|__TEST__|=","S3cr3|-",False) > 0)

#
#
#
# SCRIPT
#

if __name__ == '__main__':
    unittest.main(verbosity=2,failfast=True)
