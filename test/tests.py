#!/usr/bin/python3
import unittest
import os
import random
import string

from pdfhide import logger
from pdfhide import pdf_algo

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
__version__ = "0.0"
#
# This is a test suite for pdf_hide v0.0
#
# Written by Nicolas Canceill
# Last updated on Nov 10, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
#
#
# CONFIG
#

# Random seeds: use specific numbers to reproduce tests
RANDOM_SEED=os.urandom(16) #TODO: check compatibility
DATA_LEN=random.randrange(1,64) #TODO: include size in docs
msg=os.urandom(DATA_LEN)
KEY_LEN=random.randrange(64) #TODO: include size and input type in docs
key=''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for x in range(KEY_LEN))
# TODO: test key with all unicode chars except linebreaks

# Log level: use logger.DEBUG to debug
LOG_LEVEL=logger.CRITICAL

#
#
#
# STATIC
#

s_base = "sample/test"
s_long = "sample/test_long"
s_embed = "sample/test_e.pdf"
s_msg = "sample/msg"


# Log
rl = logger.rootLogger(LOG_LEVEL)

def print_begin(case):
	print("========== BEGIN TEST " + case.upper() + " ==========")
	print("========== SEED TEST = " + str(RANDOM_SEED))
	print("========== DATA TEST = " + str(msg))
	print("========== KEY TEST = " + str(key))

def print_end(case):
	print("========== END TEST " + case.upper() + " ==========")

#
#
#
# TEST CASES
#

# Dependencies
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

# Algorithm, no custom settings, no improvements
class DefaultAlgoTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		print_begin('algorithm (default)')
		cls.defaultMessage = msg
		cls.defaultKey = key
	def test_algodef_embed(self):
		ps = pdf_algo.PDF_stego(s_base + ".pdf",rl,output=s_embed)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algodef_extract(self):
		ps = pdf_algo.PDF_stego(s_embed,rl,output=s_msg)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algodef_resultchk(self):
		output_file = open(s_msg,"rb")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	@classmethod
	def tearDownClass(cls):
		print_end('algorithm (default)')

# Algorithm, custom settings, no improvements
class SpecialAlgoTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		random.seed(RANDOM_SEED)
		print_begin('algorithm (special)')
		cls.defaultMessage = msg
		cls.defaultKey = key
		cls.redundancy = 0
		while cls.redundancy == 0:
			#0.85 as a margin to be sure there is enough space
			#TODO: check nb of TJ ops and do that dynamically
			cls.redundancy = round(random.random()*0.85,2)
		cls.nbits = random.randrange(5,8)
	def test_algo_customred_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,output=s_embed,red=self.redundancy)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algo_customred_extract(self):
		ps = pdf_algo.PDF_stego(s_embed,rl,output=s_msg,red=self.redundancy)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algo_customred_resultchk(self):
		output_file = open(s_msg,"rb")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algo_customnbit_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,output=s_embed,nbits=self.nbits)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algo_customnbit_extract(self):
		ps = pdf_algo.PDF_stego(s_embed,rl,output=s_msg,nbits=self.nbits)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algo_customnbit_resultchk(self):
		output_file = open(s_msg,"rb")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algo_customnorandom_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,output=s_embed)
		result = ps.embed(self.defaultMessage,self.defaultKey,norandom=True)
		self.assertTrue(result > 0)
	def test_algo_customnorandom_extract(self):
		ps = pdf_algo.PDF_stego(s_embed,rl,output=s_msg)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algo_customnorandom_resultchk(self):
		output_file = open(s_msg,"rb")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algo_full_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,output=s_embed,red=self.redundancy,nbits=self.nbits)
		result = ps.embed(self.defaultMessage,self.defaultKey,norandom=True)
		self.assertTrue(result > 0)
	def test_algo_full_extract(self):
		ps = pdf_algo.PDF_stego(s_embed,rl,output=s_msg,red=self.redundancy,nbits=self.nbits)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algo_full_resultchk(self):
		output_file = open(s_msg,"rb")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	@classmethod
	def tearDownClass(cls):
		print_end('algorithm (special)')

# Algorithm, no custom settings, improvements
class DefaultIAlgoTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		print_begin('algorithm improved (default)')
		cls.defaultMessage = msg
		cls.defaultKey = key
	def test_algoidef_embed(self):
		ps = pdf_algo.PDF_stego(s_base + ".pdf",rl,output=s_embed,improve=True)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algoidef_extract(self):
		ps = pdf_algo.PDF_stego(s_embed,rl,output=s_msg,improve=True)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algoidef_resultchk(self):
		output_file = open(s_msg,"rb")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	@classmethod
	def tearDownClass(cls):
		print_end('algorithm improved (default)')

# Algorithm, custom settings, improvements
class SpecialIAlgoTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		random.seed(RANDOM_SEED)
		print_begin('algorithm improved (special)')
		cls.defaultMessage = msg
		cls.defaultKey = key
		cls.redundancy = 0
		while cls.redundancy == 0:
			#0.85 as a margin to be sure there is enough space
			#TODO: check nb of TJ ops and do that dynamically
			cls.redundancy = round(random.random()*0.85,2)
		cls.nbits = random.randrange(5,8)
	def test_algoi_customred_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,output=s_embed,improve=True,red=self.redundancy)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algoi_customred_extract(self):
		ps = pdf_algo.PDF_stego(s_embed,rl,output=s_msg,improve=True,red=self.redundancy)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algoi_customred_resultchk(self):
		output_file = open(s_msg,"rb")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algoi_customnbit_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,output=s_embed,improve=True,nbits=self.nbits)
		result = ps.embed(self.defaultMessage,self.defaultKey)
		self.assertTrue(result > 0)
	def test_algoi_customnbit_extract(self):
		ps = pdf_algo.PDF_stego(s_embed,rl,output=s_msg,improve=True,nbits=self.nbits)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algoi_customnbit_resultchk(self):
		output_file = open(s_msg,"rb")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algoi_customrange_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,output=s_embed,improve=True,customrange=True)
		result = ps.embed(self.defaultMessage,self.defaultKey,norandom=True)
		self.assertTrue(result > 0)
	def test_algoi_customrange_extract(self):
		ps = pdf_algo.PDF_stego(s_embed,rl,output=s_msg,improve=True,customrange=True)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algoi_customrange_resultchk(self):
		output_file = open(s_msg,"rb")
		output = output_file.read()
		output_file.close()
		self.assertEqual(self.defaultMessage,output)
	def test_algoi_full_embed(self):
		ps = pdf_algo.PDF_stego(s_long + ".pdf",rl,output=s_embed,improve=True,red=self.redundancy,nbits=self.nbits,customrange=True)
		result = ps.embed(self.defaultMessage,self.defaultKey,norandom=True)
		self.assertTrue(result > 0)
	def test_algoi_full_extract(self):
		ps = pdf_algo.PDF_stego(s_embed,rl,output=s_msg,improve=True,red=self.redundancy,nbits=self.nbits,customrange=True)
		result = ps.extract(self.defaultKey)
		self.assertEqual(result, 0)
	def test_algoi_full_resultchk(self):
		output_file = open(s_msg,"rb")
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
