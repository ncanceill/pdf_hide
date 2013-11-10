#!/usr/bin/python3
import re
import random

from pdfhide import chaos
from pdfhide import driver
from pdfhide import encoding
from pdfhide import logger

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
__version__ = "0.0"
#
# This is a steganographic algorithm able to hide data in PDF files
#
# Written by Nicolas Canceill
# Last updated on Nov 10, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
#
#
# MAIN CLASS
#

class PDF_stego:

	#
	#
	#
	# VARIABLES
	#

	#
	# Algo settings

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

	#
	# Dynamic variables

	# Counters for TJ operators
	tj_count = 0
	tj_count_valid = 0

	#
	#
	#
	# INITIALIZATION
	#

	# Set algo settings at creation time
	def __init__(self,input,log,output="a.out",improve=False,red=0.1,nbits=4,customrange=False):
		self.input = input
		self.output = output
		self.improve = improve
		self.l = log
		self.redundancy = red
		self.nbits = nbits
		if self.improve:
			self.customrange = customrange
		if self.redundancy > 0.7:
			self.l.warn("You are excluding more than 70% of the available space")
		if not self.improve:
			self.l.warn("You should use the \"-i\" flag for a better result")
			if self.customrange:
				self.l.warn("Improvements are disabled, so I am ignoring the custom-range flag")
		elif self.customrange:
			self.l.warn("The custom range is specifically designed for LaTeX PDF files")
			if self.nbits > 6:
				self.l.warn("Custom range is enabled, so I am forcing NBITS to 6 instead of " + str(self.nbits))
				self.nbits = 6

	#
	#
	#
	# TOOLS
	#

	#
	# Parsing tools for TJ operators

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

	#
	#
	#
	# EMBEDDING
	#

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
	def embed_op(self,val,ch_one,ch_two,num):
		# Check the original TJ value
		if (not self.improve and abs(val) > 2**self.nbits) or val == 0:
			# Value is invalid
			# -> Do not use TJ op
			return [False,val]
		# Original TJ value is valid
		# -> Use TJ op
		self.tj_count += 1
		# -> Check improvement flag
		if self.improve:
			# Improvements are enabled
			# -> Check redundancy and custom range settings
			if ch_two < self.redundancy or num == None or (self.customrange and not encoding.is_in_crange(val,self.nbits)):
				# NB: Custom range values work because of the hack normalrange/customrange
				# TODO: update docs!!!
				#
				# Value is either out of range
				# or ruled out by redundancy
				# or all data is already embedded
				# -> Check no-random flag
				if self.norandom:
					# No-random is set
					# -> Do not use TJ op
					return [False,val]
				# Use TJ op for a random value
				# -> Check sign
				if val < 0:
					return [False,-abs(val) + (abs(val) % (2**self.nbits)) - (int((2**self.nbits - 1) * ch_one) + 1 )]
				return [False,abs(val) - (abs(val) % (2**self.nbits)) + int((2**self.nbits - 1) * ch_one) + 1]
			# Value is in range
			# -> Use TJ op for data
			self.tj_count_valid += 1
			normalrange = 1
			# NB: Hack for custom range (do not shift by 1)
			# TODO: do that better and include in docs
			if self.customrange:
				normalrange = 0
			# Compute new TJ value
			# -> Check sign
			if val < 0:
				return [True,-abs(val) + (abs(val) % (2**self.nbits)) - num - normalrange]
			return [True,abs(val) - (abs(val) % (2**self.nbits)) + num + normalrange]
		# Improvements are disabled
		# -> Check redundancy setting
		if ch_two < self.redundancy or num == None:
			# Value is either ruled out by redundancy
			# or all data is already embedded
			# -> Check no-random flag
			if self.norandom:
				# No-random is set
				# -> Do not use TJ op
				return [False,val]
			# Use TJ op for a random value
			# -> Check sign
			if val < 0:
				return [False,-(int((2**self.nbits - 1) * ch_one) + 1 )]
			return [False,int((2**self.nbits - 1) * ch_one) + 1]
		# Value is in range
		# -> Use TJ op for data
		self.tj_count_valid += 1
		# -> Check sign
		if val < 0:
			return [True, -num - 1]
		return [True, num + 1]

	# Embeds data in TJ operators from a TJ string
	#
	# line: the TJ string to parse
	# ch_one: chaotic map 1
	# ch_two: chaotic map 2
	# ind: the list of nums to embed
	# i: the number of TJ ops already used
	# start: the TJ op where data starts
	# ntjs: the number of TJ ops available
	# j: the number of TJ ops already discarded
	#
	# Returns a list res[]
	# res[0] is the modified line
	# res[1] is the new value of the IND index
	def embed_line(self,line,ch_one,ch_two,ind,i,start,ntjs,j):
		# Copy parameters to return
		newline = line
		i_ = i
		j_ = j
		# Go through the line
		k = 0
		while k < newline.__len__():
			# Look for a TJ op, starting at current position
			m = re.search(r'[>)](\-?[0-9]+)[<(]',newline[k:])
			if m == None:
				# No more TJ ops
				# -> Break the loop
				k = newline.__len__()
			else:
				# A TJ op is found
				tj = int(m.group(1))
				# -> Check if there still is data to embed
				if i_ < ind.__len__():
					# Try to embed numeral
					# -> Check improvements flag
					if self.improve:
						# Using Python's randomness
						# -> Eliminate zeros
						#
						# TODO: check that
						ch_one_next = 0
						while ch_one_next == 0:
							ch_one_next = ch_one.random()
						ch_two_next = 0
						while ch_two_next == 0:
							ch_two_next = ch_two.random()
						# Check the position of the TJ op in the file
						# and embed accordingly
						if self.tj_count < start: #TODO: fix -> TODO: remember what i meant by "fix"
							# TJ op is before the start position
							# -> Check the end position
							if start + ind.__len__() + j_ - ntjs > self.tj_count:
								# TJ op is before the end position
								# -> Shift the list of nums accordingly
								#    and embed num
								op = self.embed_op(tj,ch_one_next,ch_two_next,ind[ntjs - start + self.tj_count - j_])
							else:
								# TJ op is after the end position
								# -> Do not embed num
								op = self.embed_op(tj,ch_one_next,ch_two_next,None)
						# TJ op is after the start position
						# -> Check if there is still data to embed
						elif self.tj_count - start < ind.__len__() + j_:
							# Embed num
							op = self.embed_op(tj,ch_one_next,ch_two_next,ind[self.tj_count - start - j_])
						else:
							# Do not embed num
							op = self.embed_op(tj,ch_one_next,ch_two_next,None)
					else:
						# Improvements are disabled
						# -> Embed next num
						op = self.embed_op(tj,ch_one.next(),ch_two.next(),ind[i_])
				else:
					# No more numerals to embed
					if self.improve:
						op = self.embed_op(tj,ch_one.random(),ch_two.random(),None)
					else:
						op = self.embed_op(tj,ch_one.next(),ch_two.next(),None)
				if op[0]:
					# One numeral was embedded, update valid index
					i_ += 1
				else:
					# Numeral was not embedded, update discarded index
					j_ += 1
				# Finished analizing TJ op
				# -> Insert new value
				newline = newline[:k + m.start(1)] + str(op[1]) + newline[k + m.end(1):]
				# Update current position
				# -> Jump after the current TJ op
				k += m.start(1) + str(op[1]).__len__()
				# -> Keep parsing the line
		return [newline,i_,j_]

	# Embeds data with passkey in a PDF file, outputs stego PDF file
	#
	# Returns the number of embedded numerals constituting the data
	def embed(self,data,passkey,norandom=False):
		# Initialize state
		self.norandom = norandom
		if self.customrange:
			if norandom:
				self.l.warn("Custom range is enabled, so I am forcing the no-random flag")
			self.norandom = True
		self.tj_count = 0
		self.tj_count_valid = 0
		self.tjs = []
		i = 0
		j = 0
		new_file = b""
		# Get the numerals to embed from the key and the message
		nums = encoding.encode_msg(data,passkey,self.nbits)
		ind = nums[0] + nums[1] + nums[2]
		# Initialize chaotic maps
		if self.improve:
			ch_one = random.Random(encoding.digest(data))
			ch_two = random.Random(passkey)
		else:
			ch_one = chaos.Chaotic(self.mu_one,nums[2])
			ch_two = chaos.Chaotic(self.mu_two,nums[2])
		# Open input file
		#
		# NB: Only works for valid PDF files
		self.l.info("Input file: \"" + self.input + "\"")
		driver.uncompress(self.input,self.input+".qdf")
		cover_file = open(self.input + ".qdf","rb")
		cover_file.seek(0,0)
		# Determine start position
		if 0:#self.improve: #TODO: fix
			start = int(self.tjs.__len__() * ch_two.random())
			self.l.debug("Random start position",start)
		else:
			start = 0
		# Parse file
		self.l.info("Embedding data, please wait...")
		self.print_conf_embed(data,nums)
		for line__ in cover_file:
			line = line__.decode("latin-1")
			line_ = line
			# Parse line for TJ blocks
			k = 0
			while k < line_.__len__():
				# Look for a TJ block, starting at current position
				m = re.match(r'\[(.*?)\][ ]?TJ',line_[k:])
				if m == None:
					# No TJ blocks
					# -> Look further
					#
					# TODO: check that
					k += 1
				else:
					# A TJ block is found
					# -> Try to embed data in TJ block
					block = self.embed_line(m.group(1),ch_one,ch_two,ind,i,start,self.tjs.__len__(),j)
					# Insert new block in the line
					line_ = line_[:k + m.start(1)] + block[0] + line_[k + m.end(1):]
					# Update state
					i = block[1]
					j = block[2]
					# Update current position
					k += m.start(1) + block[0].__len__()
			# Encode new line
			new_file += line_.encode("latin-1")
		self.debug_embed_check_tj(cover_file)
		# Close file and clean up
		cover_file.close()
		driver.delete(self.input+".qdf")
		# Check if all data was embedded
		if i < ind.__len__():
			# All data was not embedded
			# -> Fail
			self.l.error("Not enough space available (only " + str(self.tj_count_valid) + " available, " + str(ind.__len__()) + " needed)")
			return -ind.__len__()
		# All data was embedded
		self.l.info("Done embedding.")
		# -> Produce output file
		output_file = open(self.output+".raw","wb")
		output_file.write(new_file)
		output_file.close()
		# Fix Compress Clean
		driver.fcc(self.output+".raw",self.output)
		self.debug_embed_print_sum()
		driver.delete(self.output+".raw.fix")
		# All finished
		self.l.info("Output file: \"" + self.output + "\"")
		return nums[1].__len__()

	#
	#
	#
	# EXTRACTING
	#

	# Extracts data from a TJ operator
	#
	# val: the value of the TJ operator
	# ch_two: the next number from chaotic map 2
	#
	# Returns an integer
	# If it is 0, the TJ op is not valid
	# Otherwise, the abolute value of the TJ op is returned
	def extract_op(self,val,ch_two):
		# Update state
		self.tj_count += 1
		# Check value against settings
		if (not self.improve and abs(val) > 2**self.nbits) or val == 0 or ch_two < self.redundancy or (self.customrange and not encoding.is_in_crange(val,self.nbits)):
			# Value is either out of range
			# or ruled out by redundancy
			# or invalid
			# -> Do not use TJ op
			return 0
		# Value is in range
		# -> Update state
		self.tj_count_valid += 1
		if 0:#self.improve and self.tj_count == 1:
			return val
		# Extract data from TJ op
		return abs(val)

	# Extracts data from all operators in a TJ string
	#
	# line: the TJ string to parse
	# ch_two: chaotic map 2
	#
	# Returns a list tjs[]
	# tjs[n] is the value of the n-th valid TJ op
	def extract_line(self,line,ch_two):
		# Initialize list to return
		tjs = []
		# Go through the line
		k = 0
		while k < line.__len__():
			# Look for a TJ op, starting at current position
			m = re.search(r'[>)](\-?[0-9]+)[<(]',line[k:])
			if m == None:
				# No more TJ ops
				# -> Break the loop
				k = line.__len__()
			else:
				# A TJ op is found
				# -> Check improvements flag
				if self.improve:
					# Using Python's randomness
					# -> Eliminate zeros
					#
					# TODO: check that
					ch_two_next = 0
					while ch_two_next == 0:
						ch_two_next = ch_two.random()
				else:
					# Improvements are disabled
					ch_two_next = ch_two.next()
				# Finished checking chaotic map
				# -> Try to extract numeral
				tj = self.extract_op(int(m.group(1)),ch_two_next)
				# -> Check result
				if tj != 0:
					# A valid value was found
					# -> Prepare to return value
					tjs += [tj]
				# Update current position
				# -> Jump after the current TJ op
				k += m.end(1)
				# -> Keep parsing the line
		return tjs

	# Extracts data from PDF file using derived_key, outputs extracted data to
	def extract(self,derived_key):
		# Initialize state
		self.tj_count = 0
		self.tj_count_valid = 0
		tjs = []
		# Get the numerals from the key
		nums = encoding.encode_key(derived_key,self.nbits)
		# Initiate chaotic map
		if self.improve:
			ch_two = random.Random(derived_key)
		else:
			ch_two = chaos.Chaotic(self.mu_two,nums)
		# Open input file
		#
		# NB: Only works for valid PDF files
		self.l.info("Input file: \"" + self.input + "\"")
		driver.uncompress(self.input,self.input+".qdf")
		embedding_file = open(self.input+".qdf",encoding="iso-8859-1")
		# Determine start position
		if 0:#self.improve:#TODO: fix
			# Parse file
			for line in embedding_file:
				# Parse line for TJ blocks
				m = re.search(r'\[(.*)\][ ]?TJ',line)
				if m != None:
					tjs += self.get_tjs(m.group(1))
			start = int(tjs.__len__() * ch_two.random())
			embedding_file.seek(0,0)
			tjs = []
		else:
			start = 0
		# Parse file
		self.l.info("Extracting data, please wait...")
		self.print_conf_extract(start,nums)
		for line in embedding_file:
			# Parse line for TJ blocks
			# -> Look for a TJ block, starting at current position
			m = re.search(r'\[(.*)\][ ]?TJ',line)
			if m != None:
				# A TJ block is found
				# -> Try to extract data from TJ block
				tjs += self.extract_line(line,ch_two)
		# Close file and clean up
		embedding_file.close()
		driver.delete(self.input+".qdf")
		# Extract data from TJ ops
		normalrange = 1
		# NB: Hack for custom range (do not shift by 1)
		# TODO: do that better and include in docs
		if self.customrange:
			normalrange = 0
		# Normalize values
		#
		# TODO: check if really necessary
		tjs = list(map(lambda x: (x - normalrange) % (2**self.nbits), tjs))
		# Wrap values around in order
		# to move easily inside
		#
		# TODO: use modulo calculation instead
		tjs_ = tjs + tjs
		# Start extracting after CheckStr
		#
		# NB: CheckStr is 20 numerals long
		k = start + 20
		# Go through the list of numerals
		c = 0
		while c < tjs.__len__():
			# Look for end position FlagStr
			# at current position
			#
			# NB: FlagStr is 20 numerals long
			if nums == tjs_[k:k+20]:
				# End position is found, register it
				end = k + 20 - 1
				self.l.debug("End position found",end)
				# NB: length = end - start + 1
				# Extract CheckStr
				checkstr = tjs_[start:start + 20]
				# Extract data
				embedded = tjs_[start + 20:k]
				# Break the loop
				c = tjs.__len__()
			# FlagStr not found
			# -> Look further
			c += 1
			k += 1
		# Check is FlagStr was found
		#
		# TODO: check that
		if c != tjs.__len__() + 1:
			# FlagStr not found
			# -> Fail
			self.l.error("Ending code FlagStr not found")
			return -1
		# FlagStr was found
		# -> Decode embedded data
		self.l.info("Done extracting.")
		self.l.info("Decoding data, please wait...")
		# Go through the list of numerals
		# containing the data
		k = 0
		bin_str = ""
		while k < embedded.__len__():
			# Decode the next numeral into a binary string
			bin = encoding.num_to_binstr(embedded[k],self.nbits)
			# Check if it was the last numeral
			if k == embedded.__len__() - 1:
				# Processing the last numeral
				# -> Only take the bits needed
				bin_str += bin[bin.__len__() - self.nbits:]
			else:
				# Not processing the last numeral
				# -> Take all bits
				bin_str += bin
			# -> Keep decoding
			k += 1
		# Decode the full binary string into bytes
		emb_chars = encoding.decode(bin_str)
		emb_str = b""
		for ch in emb_chars:
			emb_str += ch
		self.debug_extract_print_sum(encoding.encode_key(emb_str,self.nbits),bin_str,checkstr,embedded,emb_str)
		# Check integrity
		if encoding.digest_to_nums(emb_str, self.nbits) != checkstr:
			# Data coes not match embedded checksum
			# -> Fail
			self.l.error("CheckStr does not match embedded data")
			return -1
		# Data matches checksum
		self.l.info("Done decoding.")
		# -> Produce output file
		output_file = open(self.output,"wb")
		output_file.write(emb_str)
		output_file.close()
		# All finished
		self.l.info("Output file: \"" + self.output + "\"")
		return 0

	#
	#
	#
	# DEBUG CHECKS
	#

	#
	# Printing tools for debug

	def print_conf(self):
		self.l.debug("===== BEGIN CONFIG =====")
		self.l.debugs({
					  "input":"\"" + self.output + ".qdf\"",
					  "redundancy":self.redundancy,
					  "bit depth":self.nbits,
					  "improvements":self.improve
					  })

	def print_conf_embed(self,data,nums):
		self.print_conf()
		self.l.debugs({
					  "Data to embed":data,
					  "Data to embed (binary)":encoding.str_to_binstr(data,self.nbits),
					  "FlagStr1 (CheckStr)":nums[0],
					  "FlagStr2":nums[2],
					  "Data":encoding.msg_to_nums(data,self.nbits)
					  })
		self.l.debug("===== END CONFIG =====")

	def print_conf_extract(self,start,nums):
		self.print_conf()
		self.l.debugs({
					  "Random start position":start,
					  "FlagStr":nums
					  })
		self.l.debug("===== END CONFIG =====")

	def debug_embed_check_tj(self,cover_file):
		if self.l.DEBUG:#TODO: do that better
			self.tjss_ = []
			cover_file.seek(0,0)
			tjss = []
			# Parse file
			for line__ in cover_file:
				line = line__.decode("latin-1")
				# Parse line for TJ blocks
				m = re.search(r'\[(.*)\][ ]?TJ',line)
				if m != None:
					self.tjs += self.get_tjs(m.group(1))
					tjss += self.get_tjs_signed(m.group(1))
			self.tjss_ = tjss
			#if self.improve:
			#	self.l.debug(self.print_it("TJ values before",tjss))
			#	self.l.debug(self.print_it("Low-bits TJ values before",map(lambda x: abs(x) % (2**self.nbits),tjss)))
			#	self.l.debug(self.print_it("TJ average before",n.avg(tjss)))
			#	self.l.debug(self.print_it("TJ unsigned average before",n.avg(tjs)))

	def debug_embed_print_sum(self):
		if self.l.DEBUG:#TODO: do that better
			embd_file = open(self.output+".raw.fix",encoding="iso-8859-1")
			tjss = []
			# Parse file
			for line in embd_file:
				# Parse line for TJ blocks
				m = re.search(r'\[(.*)\][ ]?TJ',line)
				if m != None:
					self.tjs += self.get_tjs(m.group(1))
					tjss += self.get_tjs_signed(m.group(1))
			embd_file.close()
			#if 0:#self.improve:
			#	self.print_debug("TJ values after",tjss)
			#	self.print_debug("Low-bits TJ values after",map(lambda x: abs(x) % (2**self.nbits),tjss))
			#	self.print_debug("TJ average after",n.avg(tjss))
			#	self.print_debug("TJ unsigned average after",n.avg(tjs))
			i = 0
			sbugs = []
			while i < tjss.__len__():
				if tjss[i] * self.tjss_[i] < 0:
					sbugs += ["@[" + str(i) + "] orig. " + str(self.tjss_[i]) + " | new " + str(tjss[i])]
				i += 1
			if sbugs.__len__() > 0:
				self.l.debug("Sign bugs",sbugs)
				self.l.debug("Embedded data","\"" + data + "\"")
				self.l.debug("Total nb of TJ ops",self.tj_count)
				self.l.debug("Total nb of TJ ops used",ind.__len__())
				self.l.debug("Total nb of TJ ops used for data",nums[1].__len__())

	def debug_extract_print_sum(self,checksum,bin_str,checkstr,embedded,emb_str):
		self.l.debug("Raw binary data",bin_str)
		self.l.debug("Raw data",embedded)
		self.l.debug("Data Checksum",checksum)
		self.l.debug("CheckStr",checkstr)
		self.l.debug("Extracted data","\"" + str(emb_str) + "\"")
		self.l.debug("Total nb of TJ ops",self.tj_count)
		self.l.debug("Total nb of valid TJ ops",self.tj_count_valid)
		self.l.debug("Total nb of valid TJ ops used",embedded.__len__() + 40)
		self.l.debug("Total nb of valid TJ ops used for data",embedded.__len__())
