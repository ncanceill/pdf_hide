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
__version__ = "0.0b"
#
# This is a collection of utility functions for pdf_hide v0.0b
#
# Written by Nicolas Canceill
# Last updated on Oct 12, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

# TODO: doc

#
#
# FUNCTIONS
#
# Handle 015 and 116 numeral integers, and binary strings, and other stuff
#

#
# Binary strings

def pad_binstr(b,nbits):
	while b.__len__() < nbits:
		b = "0" + b
	return b

def pad_binstr_bige(b,nbits):
	while b.__len__() % nbits > 0:
		b = "0" + b
	return b

def pad_binstr_littlee(b,nbits):
	while b.__len__() % nbits > 0:
		b = b + "0"
	return b

def pad_str(msg,nbits):
	return [pad_binstr(bin,nbits) for bin in split_len(str_to_binstr(msg,nbits),nbits)]

def tail_bige(b):
	if b[:b.__len__()%8].__len__() > 0 and int(b[:b.__len__()%8],2) > 0:
		return pad_binstr_bige(b,8)
	return b[b.__len__()%8:]

def tail_littlee(b):
	if b[b.__len__()-(b.__len__()%8):].__len__() > 0 and int(b[b.__len__()-(b.__len__()%8):],2) > 0:
		return pad_binstr_littlee(b,8)
	return b[:b.__len__()-(b.__len__()%8)-1]

def num_to_binstr(num,nbits):
	return pad_binstr(bin(num)[2:],nbits)

# Encodes a string into a binary string based on the ASCII codes
# (e.g. "a" returns "01100001")
def str_to_binstr(str,nbits):
	# Hack for bytes instead of string
	#TODO: do that better and include little endian
	if isinstance(str,type(b'')):
		return bstr_to_binstr_bige(str,nbits)
	if str.__len__() < 1:
		return ""
	else:
		result = ""
		for c in str:
			result += num_to_binstr(ord(c),8)
		return result

# Encodes bytes into a big-endian binary string codes
# (e.g. b"\xac" returns "0010101100" if n is 5)
def bstr_to_binstr_bige(bstr,nbits):
	if bstr.__len__() < 1:
		return ""
	else:
		return pad_binstr_bige(bin(int.from_bytes(bstr,"big"))[2:],nbits)

# Encodes bytes into a little-endian binary string codes
# (e.g. b"\xac" returns "0011010100" if n is 5)
def bstr_to_binstr_littlee(bstr,nbits):
	if bstr.__len__() < 1:
		return ""
	else:
		return pad_binstr_littlee(bin(int.from_bytes(bstr,"little"))[2:],nbits)

# Encodes an 8-bit number (passed-in as a binary string, e.g. "01100001" for a)
# into a character
def binstr_to_ch(str):
	return chr(int(str,2) % 256)

# Encodes an 8-bit number (passed-in as a binary string, e.g. "01000110")
# into a big endian byte
def binstr_to_byte_bige(str):
	return int(str,2).to_bytes(1,"big")

# Encodes an ASCII code (passed-in as an hexadecimal string)
# into a numeral using mod(2^n)
def hexstr_to_num(h,nbits):
	return int(h,16) % (2**nbits)

# Encodes a n-bit number (passed-in as a binary string, e.g. "0110" if n is 4)
# into a numeral (a "015" numeral if n is 4)
def binstr_to_num(str,nbits):
	return int(str,2) % (2**nbits)

# Returns the 20-byte SHA1 digest of a string as an hexadecimal string
def digest(str):
	# Hack for bytes instead of string
	#TODO: do that better
	if isinstance(str,type(b'')):
		return hashlib.sha1(str).hexdigest()
	return hashlib.sha1(str.encode('utf-8')).hexdigest()

#
# Sequences of numerals

# Splits a sequence into a list of sequences of specified length (the last one may be shorter)
def split_len(seq,length):
	return [seq[i:i+length] for i in range(0,len(seq),length)]

#
# Encoding

# Encodes a 20-byte SHA1 digest to a list of 20 numerals array according to the algo
def digest_to_nums(d,nbits):
	return [hexstr_to_num(dig,nbits) for dig in split_len(digest(d),2)]

# Encodes a message to a list of numerals according to the algo
def msg_to_nums(msg,nbits):
	return [binstr_to_num(str,nbits) for str in pad_str(msg,nbits)]

# Encodes a message and a stego key according to the algo
#
# Returns a list n[]:
# n[0] is the list of 20 numerals representing "FlagStr1"
# n[1] is the list of numerals representing the message
# n[2] is the list of 20 numerals representing "FlagStr2"
def encode_msg(msg,key,nbits):
	return [digest_to_nums(msg,nbits),msg_to_nums(msg,nbits),digest_to_nums(key,nbits)]

# Encodes a derived key according to the algo
#
# Returns the list of 20 numerals representing "FlagStr"
def encode_key(key,nbits):
	return digest_to_nums(key,nbits)

def decode(bin_str):
	return [binstr_to_byte_bige(num) for num in split_len(tail_bige(bin_str),8)]

#
# Math

def avg(nums):
	n = 0
	for k in nums:
		n += k
	return float(n) / nums.__len__()

def mean(nums,nums_):
	if nums.__len__() < nums_.__len__():
		return 0.
	n = 0
	i = 0
	while i < nums_.__len__():
		n += (nums[i] - nums_[i])
		i += 1
	return float(n) / nums_.__len__()
