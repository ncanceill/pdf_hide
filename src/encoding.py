#!/usr/bin/python3
import hashlib

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
# encoding.py
__version__ = "0.0a"
#
# This is a collection of utility functions for pdf_hide v0.0a
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

# Handle 015 and 116 numeral integers, and binary strings, and other stuff
class Numerals:

	# The number of bit to use
	n = 4

	def __init__(self,nbits):
		self.n = nbits

	def pad_binstr(self,b,nbits):
		while b.__len__() < nbits:
			b = "0" + b
		return b

	def num_to_binstr(self,num,nbits):
		return self.pad_binstr(bin(num)[2:],nbits)

	# Encodes a string into a binary string based on the ASCII codes (e.g. "a" returns "01100001")
	def str_to_binstr(self,str):
		if str.__len__() < 1:
			return ""
		else:
			result = ""
			for c in str:
				result += self.num_to_binstr(ord(c),8)
			return result

	# Encodes a 4-bit number (passed-in as a binary string, e.g. "0110") into a character
	def binstr_to_ch(self,str):
		return chr(int(str,2) % 256)

	# Encodes an ASCII code (passed-in as an hexadecimal string) into a numeral using mod(2^n)
	def hexstr_to_num(self,h):
		return int(h,16) % (2**self.n)

	# Encodes a n-bit number (passed-in as a binary string, e.g. "0110" if n is 4) into a numeral (a "015" numeral if n is 4)
	def binstr_to_num(self,str):
		return int(str,2) % (2**self.n)

	# Splits a sequence into a list of sequences of specified length (the last one may be shorter)
	def split_len(self,seq,length):
		return [seq[i:i+length] for i in range(0,len(seq),length)]

	# Returns the 20-byte SHA1 digest of a string as an hexadecimal string
	def digest(self,str):
		return hashlib.sha1(str.encode('utf-8')).hexdigest()

	# Encodes a 20-byte SHA1 digest to a list of 20 numerals array according to the algo
	def digest_to_nums(self,d):
		return list(map(self.hexstr_to_num,self.split_len(self.digest(d),2)))

	# Encodes a message to a list of numerals according to the algo
	def msg_to_nums(self,msg):
		return list(map(self.binstr_to_num,[self.pad_binstr(bin,self.n) for bin in self.split_len(self.str_to_binstr(msg),self.n)]))

	# Encodes a message and a stego key according to the algo
	#
	# Returns a list n[]:
	# n[0] is the list of 20 numerals representing "FlagStr1"
	# n[1] is the list of numerals representing the message
	# n[2] is the list of 20 numerals representing "FlagStr2"
	def encode_msg(self,msg,key):
		return [self.digest_to_nums(msg),self.msg_to_nums(msg),self.digest_to_nums(key)]

	# Encodes a derived key according to the algo
	#
	# Returns the list of 20 numerals representing "FlagStr"
	def encode_key(self,key):
		return self.digest_to_nums(key)

	def avg(self,nums):
		n = 0
		for k in nums:
			n += k
		return float(n) / nums.__len__()

	def mean(self,nums,nums_):
		if nums.__len__() < nums_.__len__():
			return 0.
		n = 0
		i = 0
		while i < nums_.__len__():
			n += (nums[i] - nums_[i])
			i += 1
		return float(n) / nums_.__len__()
