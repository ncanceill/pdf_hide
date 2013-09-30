#!/usr/bin/python3
import unittest
import os
import random

import logger
import pdf_algo

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
# chaos.py
__version__ = "0.0a"
#
# This is a test suite for pdf_hide v0.0a
#
# Written by Nicolas Canceill
# Last updated on Sept 29, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
#
#
# CONFIG
#

# Random seed: use a specific number to reproduce tests
RANDOM_SEED=123456#None

# Log level: use logger.DEBUG to debug
LOG_LEVEL=logger.DEBUG#CRITICAL

#
#
#
# STATIC
#

s_base = "../sample/test"
s_long = "../sample/test_long"

# Log
rl = logger.rootLogger(LOG_LEVEL)

def print_begin(case):
	print("========== BEGIN TEST " + case.upper() + " ==========")

def print_end(case):
	print("========== END TEST " + case.upper() + " ==========")

#
#
#
# CLASSES
#

class AllDependenciesTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		print_begin('dependencies')
	def test_dep_pdflatex(self):
		self.assertEqual(os.system('which pdflatex > /dev/null'),0)
	def test_dep_qpdf(self):
		self.assertEqual(os.system('which qpdf > /dev/null'),0)
	@classmethod
	def tearDownClass(cls):
		print_end('dependencies')

class DefaultAlgoTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		print_begin('algorithm (default)')
		cls.defaultMessage = "123456ThisIsA\n=|__TEST__|="
		cls.defaultKey = "S3cr3|-"
	def test_algodef_embed(self):
		ps = pdf_algo.PDF_stego(s_base + ".pdf",rl)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algodef_extract(self):
		ps = pdf_algo.PDF_stego(s_base + ".pdf.out.fix.pdf",rl)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algodef_resultchk(self):
		output_file = open(s_base + ".pdf.out.fix.pdf.embd")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	@classmethod
	def tearDownClass(cls):
		print_end('algorithm (default)')

class SpecialAlgoTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		random.seed(RANDOM_SEED)
		print_begin('algorithm (special)')
		cls.defaultMessage = "123456ThisIsA\n=|__TEST__|="
		cls.defaultKey = "S3cr3|-"
		cls.redundancy = 0
		while cls.redundancy == 0:
			cls.redundancy = random.random()
		cls.nbits = random.randrange(5,8)
	def test_algo_customred_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,red=self.redundancy)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algo_customred_extract(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf.out.fix.pdf",rl,red=self.redundancy)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algo_customred_resultchk(self):
		output_file = open(s_long + ".pdf.out.fix.pdf.embd")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algo_customnbit_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,nbits=self.nbits)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algo_customnbit_extract(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf.out.fix.pdf",rl,nbits=self.nbits)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algo_customnbit_resultchk(self):
		output_file = open(s_long + ".pdf.out.fix.pdf.embd")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algo_customrange_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,customrange=True)
		result = ps.embed(self.defaultMessage,self.defaultKey,norandom=True)
		self.assertTrue(result > 0)
	def test_algo_customrange_extract(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf.out.fix.pdf",rl,customrange=True)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algo_customrange_resultchk(self):
		output_file = open(s_long + ".pdf.out.fix.pdf.embd")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algo_full_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,red=self.redundancy,nbits=self.nbits,customrange=True)
		result = ps.embed(self.defaultMessage,self.defaultKey,norandom=True)
		self.assertTrue(result > 0)
	def test_algo_full_extract(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf.out.fix.pdf",rl,red=self.redundancy,nbits=self.nbits,customrange=True)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algo_full_resultchk(self):
		output_file = open(s_long + ".pdf.out.fix.pdf.embd")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	@classmethod
	def tearDownClass(cls):
		print_end('algorithm (special)')

class DefaultAlgoImprovedTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		print_begin('algorithm improved (default)')
		cls.defaultMessage = "123456ThisIsA\n=|__TEST__|="
		cls.defaultKey = "S3cr3|-"
	def test_algoidef_embed(self):
		ps = pdf_algo.PDF_stego(s_base + ".pdf",rl,improve=True)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algoidef_extract(self):
		ps = pdf_algo.PDF_stego(s_base + ".pdf.out.fix.pdf",rl,improve=True)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algoidef_resultchk(self):
		output_file = open(s_base + ".pdf.out.fix.pdf.embd")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	@classmethod
	def tearDownClass(cls):
		print_end('algorithm improved (default)')

class SpecialAlgoImprovedTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		random.seed(RANDOM_SEED)
		print_begin('algorithm improved (special)')
		cls.defaultMessage = "123456ThisIsA\n=|__TEST__|="
		cls.defaultKey = "S3cr3|-"
		cls.redundancy = 0
		while cls.redundancy == 0:
			cls.redundancy = random.random()
		cls.nbits = random.randrange(5,8)
	def test_algoi_customred_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,improve=True,red=self.redundancy)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algoi_customred_extract(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf.out.fix.pdf",rl,improve=True,red=self.redundancy)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algoi_customred_resultchk(self):
		output_file = open(s_long + ".pdf.out.fix.pdf.embd")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algoi_customnbit_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,improve=True,nbits=self.nbits)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algoi_customnbit_extract(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf.out.fix.pdf",rl,improve=True,nbits=self.nbits)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algoi_customnbit_resultchk(self):
		output_file = open(s_long + ".pdf.out.fix.pdf.embd")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algo_customrange_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,improve=True,customrange=True)
		result = ps.embed(self.defaultMessage,self.defaultKey,norandom=True)
		self.assertTrue(result > 0)
	def test_algo_customrange_extract(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf.out.fix.pdf",rl,improve=True,customrange=True)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algo_customrange_resultchk(self):
		output_file = open(s_long + ".pdf.out.fix.pdf.embd")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algoi_full_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,improve=True,red=self.redundancy,nbits=self.nbits,customrange=True)
		result = ps.embed(self.defaultMessage,self.defaultKey,norandom=True)
		self.assertTrue(result > 0)
	def test_algoi_full_extract(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf.out.fix.pdf",rl,improve=True,red=self.redundancy,nbits=self.nbits,customrange=True)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algoi_full_resultchk(self):
		output_file = open(s_long + ".pdf.out.fix.pdf.embd")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	@classmethod
	def tearDownClass(cls):
		print_end('algorithm improved (special)')

#
#
#
# SCRIPT
#

if __name__ == '__main__':
    unittest.main(verbosity=2,failfast=True)
