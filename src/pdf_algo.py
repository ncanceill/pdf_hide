#!/usr/bin/python3
import re
import random

import chaos
import driver
import encoding
import logger

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
# pdf_algo.py
__version__ = "0.0a"
#
# This is a steganographic algorithm able to hide data in PDF files
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

class PDF_stego:

	# The number of bit to use
	nbits = 4

	# Improvements flag
	improve = False

	# Redundancy parameter, should be in ]0,1[
	redundancy = 0.1

	# Do not replace unchanged values by random values
	norandom = False

	# Only use values in custom range for LaTeX
	customrange = False

	# Chaotic map parameters, should be in ]3.57,4[
	mu_one = 3.7
	mu_two = 3.8

	# Counters for TJ operators
	tj_count = 0
	tj_count_valid = 0

	def __init__(self,input,log,output="a.out",improve=False,red=0.1,nbits=4,customrange=False):
		self.input = input
		self.output = output
		self.improve = improve
		self.l = log
		self.redundancy = red
		self.nbits = nbits
		if self.improve:
			self.customrange = customrange

	def get_tjs(self,line):
		tjs = []
		k = 0
		while k < line.__len__():
			# Parse TJ string from current position
			m = re.search(r'[>)](\-?[0-9]+)[<(]',line[k:])
			if m == None:
				# No more TJ ops
				k = line.__len__()
			else:
				val = int(m.group(1))
				if (self.improve or abs(val) < 2**self.nbits + 1) and val != 0:
					tjs += [abs(val)]
				k += m.end(1)
		return tjs

	def get_tjs_signed(self,line):
		tjs = []
		k = 0
		while k < line.__len__():
			# Parse TJ string from current position
			m = re.search(r'[>)](\-?[0-9]+)[<(]',line[k:])
			if m == None:
				# No more TJ ops
				k = line.__len__()
			else:
				val = int(m.group(1))
				if (self.improve or abs(val) < 2**self.nbits + 1) and val != 0:
					tjs += [val]
				k += m.end(1)
		return tjs

	# Embeds data in a TJ operator
	#
	# val: the original value of the TJ operator
	# ch_one: the next number from chaotic map 1
	# ch_two: the next number from chaotic map 2
	# num: the next numeral to embed, or None if the IND was taken to finish
	#
	# Returns a list res[]
	# If res[0] == True then num was embedded, move on to next numeral
	# If res[0] == False then try to embed num again in the nex operator
	# res[1] is the new operator value (regardless of res[0])
	def embed_op(self,val,ch_one,ch_two,num,jitter):
		if (not self.improve and abs(val) > 2**self.nbits) or val == 0:
			# Do not use TJ op
			return [False,val]
		#if self.improve and self.tj_count == 1:
		# Embed jitter value
		#if jitter < 0:
		#	self.print_debug('Embedded jitter',jitter - 1)
		#	return [False, jitter - 1]
		#self.print_debug('Embedded jitter',jitter + 1)
		#return [False, jitter + 1]
		self.tj_count += 1
		if self.improve:
			if ch_two < self.redundancy or num == None or (self.customrange and (val > -257 or val < -447 or (val < -320 and val > -337))):
				# Use TJ op for a random value
				if self.norandom:
					return [False,val]
				if val < 0:
					return [False,-abs(val) + (abs(val) % (2**self.nbits)) - (int((2**self.nbits - 1) * ch_one) + 1 )]
				return [False,abs(val) - (abs(val) % (2**self.nbits)) + int((2**self.nbits - 1) * ch_one) + 1]
			# Use TJ op for data
			self.tj_count_valid += 1
			if val < 0:
				return [True,-abs(val) + (abs(val) % (2**self.nbits)) - num - 1]
			return [True,abs(val) - (abs(val) % (2**self.nbits)) + num + 1]
		if ch_two < self.redundancy or num == None:
			# Use TJ op for a random value
			if self.norandom:
				return [False,val]
			if val < 0:
				return [False,-(int((2**self.nbits - 1) * ch_one) + 1 )]
			return [False,int((2**self.nbits - 1) * ch_one) + 1]
		# Use TJ op for data
		self.tj_count_valid += 1
		if val < 0:
			return [True, -num - 1]
		return [True, num + 1]

	# Embeds data in TJ operators from a TJ string
	#
	# line: the TJ string to parse
	# ch_one: chaotic map 1
	# ch_two: chaotic map 2
	# ind: the IND to embed
	# i: the current IND index
	#
	# Returns a list res[]
	# res[0] is the modified line
	# res[1] is the new value of the IND index
	def embed_line(self,line,ch_one,ch_two,ind,i,start,ntjs,jitter,j):
		newline = line
		i_ = i
		j_ = j
		k = 0
		while k < newline.__len__():
			# Parse TJ string from current position
			m = re.search(r'[>)](\-?[0-9]+)[<(]',newline[k:])
			if m == None:
				# No more TJ ops
				k = newline.__len__()
			else:
				tj = int(m.group(1))
				if i_ < ind.__len__():
					# Try to embed numeral
					if self.improve:
						ch_one_next = 0
						while ch_one_next == 0:
							ch_one_next = ch_one.random()
						ch_two_next = 0
						while ch_two_next == 0:
							ch_two_next = ch_two.random()
						if self.tj_count < start: #TODO: fix
							if start + ind.__len__() + j_ - ntjs > self.tj_count:
								op = self.embed_op(tj,ch_one_next,ch_two_next,ind[ntjs - start + self.tj_count - j_],jitter)
							else:
								op = self.embed_op(tj,ch_one_next,ch_two_next,None,jitter)
						elif self.tj_count - start < ind.__len__() + j_:
							op = self.embed_op(tj,ch_one_next,ch_two_next,ind[self.tj_count - start - j_],jitter)
						else:
							op = self.embed_op(tj,ch_one_next,ch_two_next,None,jitter)
					else:
						op = self.embed_op(tj,ch_one.next(),ch_two.next(),ind[i_],jitter)
				else:
					# No more numerals to embed
					if self.improve:
						op = self.embed_op(tj,ch_one.random(),ch_two.random(),None,jitter)
					else:
						op = self.embed_op(tj,ch_one.next(),ch_two.next(),None,jitter)
				if op[0]:
					# One numeral was embedded, update IND index
					i_ += 1
				else:
					j_ += 1
				# Insert new value
				newline = newline[:k + m.start(1)] + str(op[1]) + newline[k + m.end(1):]
				# Update current position
				k += m.start(1) + str(op[1]).__len__()
		return [newline,i_,j_]

	# Embeds data with passkey in a PDF file, outputs stego PDF file
	#
	# Returns the number of embedded numerals constituting the data
	def embed(self,data,passkey,norandom=False):
		self.print_conf()
		self.tj_count = 0
		self.tj_count_valid = 0
		self.norandom = norandom
		self.l.info("Embedding data, please wait...")
		driver.uncompress(self.input,self.input+".qdf")
		cover_file = open(self.input + ".qdf",encoding="iso-8859-1")
		new_file = ""
		n = encoding.Numerals(self.nbits)
		# Get the numerals to embed from the key and the message
		nums = n.encode_msg(data,passkey)
		ind = nums[0] + nums[1] + nums[2]
		tjs = []
		if self.improve:
			# Parse file
			for line in cover_file:
				# Parse line for TJ blocks
				m = re.search(r'\[(.*)\][ ]?TJ',line)
				if m != None:
					tjs += self.get_tjs(m.group(1))
			# Jitter data
			jitter = 0#int(n.mean(tjs,ind)) #TODO: improve jitter calculation
			ind = list(map(lambda x: (x + jitter) % (2**self.nbits),ind))
		else:
			jitter = 0
		self.l.debug(self.print_it("FlagStr1 (CheckStr)",nums[0]))
		self.l.debug(self.print_it("FlagStr2",nums[2]))
		self.l.debug(self.print_it("Data",n.msg_to_nums(data)))
		self.l.debug(self.print_it("Jitter",jitter))
		# Initiate chaotic maps
		if self.improve:
			ch_one = random.Random(n.digest(data))
			ch_two = random.Random(passkey)
		else:
			ch_one = chaos.Chaotic(self.mu_one,nums[2])
			ch_two = chaos.Chaotic(self.mu_two,nums[2])
		# Parse file
		if 0:#self.improve: #TODO: fix
			start = int(tjs.__len__() * ch_two.random())
			self.l.debug(self.print_it("Random start position",start))
		else:
			start = 0
		i = 0
		j = 0
		cover_file.seek(0,0)
		for line in cover_file:
			line_ = line
			k = 0
			while k < line_.__len__():
				# Parse line for TJ blocks
				m = re.match(r'\[(.*?)\][ ]?TJ',line_[k:])
				if m == None:
					# No TJ blocks
					k += 1
				else:
					# Try to embed data in TJ block
					block = self.embed_line(m.group(1),ch_one,ch_two,ind,i,start,tjs.__len__(),jitter,j)
					# Insert new block
					line_ = line_[:k + m.start(1)] + block[0] + line_[k + m.end(1):]
					i = block[1]
					j = block[2]
					# Update current position
					k += m.start(1) + block[0].__len__()
			new_file += line_
		tjss_ = []
		if self.l.DEBUG:#TODO: do that better
			cover_file.seek(0,0)
			tjss = []
			# Parse file
			for line in cover_file:
				# Parse line for TJ blocks
				m = re.search(r'\[(.*)\][ ]?TJ',line)
				if m != None:
					tjs += self.get_tjs(m.group(1))
					tjss += self.get_tjs_signed(m.group(1))
			tjss_ = tjss
			if 0:#self.improve:
				self.l.debug(self.print_it("TJ values before",tjss))
				self.l.debug(self.print_it("Low-bits TJ values before",map(lambda x: abs(x) % (2**self.nbits),tjss)))
				self.l.debug(self.print_it("TJ average before",n.avg(tjss)))
				self.l.debug(self.print_it("TJ unsigned average before",n.avg(tjs)))
		cover_file.close()
		if i < ind.__len__():
			self.l.error("Not enough space available (only " + str(self.tj_count_valid) + " available, " + str(ind.__len__()) + " needed)")
			return 0
		else:
			self.l.info("Done embedding.")
			output_file = open(self.output,"w")
			output_file.write(new_file)
			output_file.close()
			driver.fix(self.output,self.output+".fix")
			driver.compress(self.output+".fix",self.output)
			self.l.info("Output file: \"" + self.output + "\"")
			self.l.debug(self.print_it("Embedded data","\"" + data + "\""))
			self.l.debug(self.print_it("Total nb of TJ ops",self.tj_count))
			self.l.debug(self.print_it("Total nb of TJ ops used",ind.__len__()))
			self.l.debug(self.print_it("Total nb of TJ ops used for data",nums[1].__len__()))
			if self.l.DEBUG:#TODO: do that better
				embd_file = open(self.output+".fix",encoding="iso-8859-1")
				tjss = []
				# Parse file
				for line in embd_file:
					# Parse line for TJ blocks
					m = re.search(r'\[(.*)\][ ]?TJ',line)
					if m != None:
						tjs += self.get_tjs(m.group(1))
						tjss += self.get_tjs_signed(m.group(1))
				embd_file.close()
				if 0:#self.improve:
					self.print_debug("TJ values after",tjss)
					self.print_debug("Low-bits TJ values after",map(lambda x: abs(x) % (2**self.nbits),tjss))
					self.print_debug("TJ average after",n.avg(tjss))
					self.print_debug("TJ unsigned average after",n.avg(tjs))
				i = 0
				sbugs = []
				while i < tjss.__len__():
					if tjss[i] * tjss_[i] < 0:
						sbugs += ["@[" + str(i) + "] orig. " + str(tjss_[i]) + " | new " + str(tjss[i])]
					i += 1
				if sbugs.__len__() > 0:
					self.l.debug(self.print_it("Sign bugs",sbugs))
			return nums[1].__len__()

	def extract_op(self,val,ch_two):
		self.tj_count += 1
		if (not self.improve and abs(val) > 2**self.nbits) or val == 0 or ch_two < self.redundancy or (self.customrange and (val > -257 or val < -447 or (val < -320 and val > -337))):
			# Do not use TJ op
			return 0
		self.tj_count_valid += 1
		if 0:#self.improve and self.tj_count == 1:
			return val
		# Extract data from TJ op
		return abs(val)

	def extract_line(self,line,ch_two):
		k = 0
		tjs = []
		while k < line.__len__():
			# Parse TJ string from current position
			m = re.search(r'[>)](\-?[0-9]+)[<(]',line[k:])
			if m == None:
				# No more TJ ops
				k = line.__len__()
			else:
				# Try to extract numeral
				if self.improve:
					ch_two_next = 0
					while ch_two_next == 0:
						ch_two_next = ch_two.random()
				else:
					ch_two_next = ch_two.next()
				tj = self.extract_op(int(m.group(1)),ch_two_next)
				if tj != 0:
					# Get value
					tjs += [tj]
				# Update current position
				k += m.end(1)
		return tjs

	# Extracts data from PDF file using derived_key, outputs extracted data to
	def extract(self,derived_key):
		self.print_conf()
		self.tj_count = 0
		self.tj_count_valid = 0
		self.l.info("Input file: \"" + self.input + "\"")
		self.l.info("Extracting data, please wait...")
		# Only works for valid PDF files
		driver.uncompress(self.input,self.input+".qdf")
		embedding_file = open(self.input+".qdf",encoding="iso-8859-1")
		n = encoding.Numerals(self.nbits)
		# Get the numerals from the key
		nums = n.encode_key(derived_key)
		self.l.debug(self.print_it("FlagStr",nums))
		# Initiate chaotic map
		if self.improve:
			ch_two = random.Random(derived_key)
		else:
			ch_two = chaos.Chaotic(self.mu_two,nums)
		if 0:#self.improve:
			# Parse file
			tjs = []
			for line in embedding_file:
				# Parse line for TJ blocks
				m = re.search(r'\[(.*)\][ ]?TJ',line)
				if m != None:
					tjs += self.get_tjs(m.group(1))
			start = int(tjs.__len__() * ch_two.random())
			self.l.debug(self.print_it("Random start position",start))
			embedding_file.seek(0,0)
		else:
			start = 0
		# Parse file
		tjs = []
		for line in embedding_file:
			# Parse line for TJ blocks
			m = re.search(r'\[(.*)\][ ]?TJ',line)
			if m != None:
				# Try to extract data from TJ block
				tjs += self.extract_line(line,ch_two)
		embedding_file.close()
		if 0:#self.improve:
			# Extract jitter
			if tjs[0] < 0:
				jitter = tjs[0] + 1
			else:
				jitter = tjs[0] - 1
			self.l.debug(self.print_it("Jitter found",jitter))
		else:
			jitter = 0
		# Jitter data
		tjs = list(map(lambda x: (x - jitter - 1) % (2**self.nbits), tjs))
		tjs_ = tjs + tjs
		# Extract data
		k = start + 20
		c = 0
		while c < tjs.__len__():
			# Look for end position
			if nums == tjs_[k:k+20]:
				end = k + 20 - 1
				self.l.debug(self.print_it('End position found',end))
				#length = end - start + 1
				checkstr = tjs_[start:start + 20]
				embedded = tjs_[start + 20:k]
				c = tjs.__len__()
			c += 1
			k += 1
		if c != tjs.__len__() + 1:
			self.l.error("Ending code FlagStr not found")
			return -1
		else:
			# Decode embedded data
			k = 0
			bin_str = ""
			while k < embedded.__len__():
				bin = n.num_to_binstr(embedded[k],self.nbits)
				if k == embedded.__len__() - 1:
					missing = -(bin_str.__len__() % 8) % 8
					if missing > self.nbits:
						self.l.error("...") #TODO: message
						self.l.debug(self.print_it("Raw data (corrupted)",embedded))
						return -1
					bin_str += bin[bin.__len__() - missing:]
				else:
					bin_str += bin
				k += 1
			emb_chars = map(n.binstr_to_ch,n.split_len(bin_str,8))
			emb_str = ""
			for ch in emb_chars:
				emb_str += ch
			if self.l.DEBUG:#TODO: do that better
				self.l.debug(self.print_it('Data Checksum',n.encode_key(emb_str)))
				self.l.debug(self.print_it('CheckStr',checkstr))
				self.l.debug(self.print_it('Data',embedded))
			# Check integrity
			if n.digest_to_nums(emb_str) != checkstr:
				self.l.error("CheckStr does not match embedded data")
				self.l.debug(self.print_it("Raw data (corrupted)",emb_str))
				return -1
			else:
				self.l.info("Done extracting.")
				output_file = open(self.output,"w")
				output_file.write(emb_str)
				output_file.close()
				self.l.info("Output file: \"" + self.output + ".embd\"")
				self.l.debug(self.print_it("Extracted data","\"" + emb_str + "\""))
				self.l.debug(self.print_it("Total nb of TJ ops",self.tj_count))
				self.l.debug(self.print_it("Total nb of valid TJ ops",self.tj_count_valid))
				self.l.debug(self.print_it("Total nb of valid TJ ops used",embedded.__len__() + 40))
				self.l.debug(self.print_it("Total nb of valid TJ ops used for data",embedded.__len__()))
				return 0

	def print_it(self,name,value):
		ret = ""
		if value != None and hasattr(value, '__len__'):
			ret += name + ' (' + str(value.__len__()) + ')'
		else:
			ret += name
		if value == None:
			ret += ""
		else:
			ret += ('\t' + str(value))
		return ret

	def print_conf(self):
		self.l.debug("\n===== CONFIG =====")
		self.l.debug("== input: \"" + self.output + ".qdf\"")
		self.l.debug("== redundancy: " + str(self.redundancy))
		self.l.debug("== bit depth: " + str(self.nbits))
		if self.improve:
			i = "YES"
		else:
			i = "NO"
		self.l.debug("== using improvements: " + i)
