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
__version__ = "0.0"
#
# This is a collection of utility functions for pdf_hide v0.0
#
# Written by Nicolas Canceill
# Last updated on Nov 10, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
# This modules provides useful functions to the pdf_hide algorithm.
#
# Basically, it exposes an API to juggle with binary strings (implemented
# as the `bytes` type in Python), binary representations (implemented as
# UTF-8 strings of "0"s and "1"s), and n-bits integers called 'numerals'.
#

#
#
# PUBLIC API
#
#

#
# Encoding

# Returns the 20-byte SHA1 digest of a string as an hexadecimal string
def digest(str):
	if isinstance(str,type(b'')):
		return hashlib.sha1(str).hexdigest()
	return hashlib.sha1(str.encode('utf-8')).hexdigest()

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
	return [digest_to_nums(msg,nbits),msg_to_nums(msg,nbits),digest_to_nums(key.encode('utf-8'),nbits)]

# Encodes a derived key according to the algo
#
# Returns the list of 20 numerals representing "FlagStr"
def encode_key(key,nbits):
	return digest_to_nums(key,nbits)

#
# Decoding

# Decodes extracted data into bytes
#
# Returns a list of bytes
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

def lmgt(nbits,limit):
	m = 0
	n = 2**nbits
	l = abs(limit)
	while m * n < l:
		m = m + 1
	if limit < 0:
		return -(m * n)
	return m * n

def gmlt(nbits,limit):
	m = 0
	n = 2**nbits
	l = abs(limit)
	while m * n < l:
		m = m + 1
	if limit < 0:
		return -(m - 1) * n
	return (m - 1) * n

def is_in_crange(tj,nbits):
	return ((tj <= lmgt(nbits,-250) and tj > gmlt(nbits,-333)) or (tj <= lmgt(nbits,-334) and tj > gmlt(nbits,-450)))

#
# Sequences

# Splits a sequence into a list of sequences of specified length
# (the last one may be shorter)
def split_len(seq,length):
	return [seq[i:i+length] for i in range(0,len(seq),length)]

#
#
# INTERNALS
#
#

#
# Padding strings

def pad_binstr(b,nbits):
	while b.__len__() < nbits:
		b = "0" + b
	return b

def pad_binstr_bige(b,nbits):
	while b.__len__() % nbits > 0:
		b = "0" + b
	return b

def pad_str(msg,nbits):
	return [pad_binstr(bin,nbits) for bin in split_len(str_to_binstr(msg,nbits),nbits)]

def num_to_binstr(num,nbits):
	return pad_binstr(bin(num)[2:],nbits)

#
# Troncating strings

def tail_bige(b):
	if b[:b.__len__()%8].__len__() > 0 and int(b[:b.__len__()%8],2) > 0:
		return pad_binstr_bige(b,8)
	return b[b.__len__()%8:]

#
# Conversions

# --- Bytes to binary strings

# Encodes bytes into a big-endian binary string
# (e.g. b"\xac" returns "0010101100" if n is 5)
def str_to_binstr(bstr,nbits):
	if bstr.__len__() < 1:
		return ""
	if isinstance(bstr,type(b'')):
		return pad_binstr_bige(bin(int.from_bytes(bstr,"big"))[2:],nbits)
	return pad_binstr_bige(bin(int.from_bytes(bstr.encode('utf-8'),"big"))[2:],nbits)

# --- Binary strings to bytes

# Encodes an 8-bit number (passed-in as a binary string, e.g. "01000110")
# into a big endian byte
def binstr_to_byte_bige(str):
	return int(str,2).to_bytes(1,"big")

# --- Binary strings to strings

# Encodes an 8-bit number (passed-in as a binary string, e.g. "01100001" for a)
# into a character
def binstr_to_ch(str):
	return chr(int(str,2) % 256)

# --- Strings to numerals

# Encodes an ASCII code (passed-in as an hexadecimal string)
# into a numeral using mod(2^n)
def hexstr_to_num(h,nbits):
	return int(h,16) % (2**nbits)

# Encodes a n-bit number (passed-in as a binary string, e.g. "0110" if n is 4)
# into a numeral (a "015" numeral if n is 4)
def binstr_to_num(str,nbits):
	return int(str,2) % (2**nbits)
