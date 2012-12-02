#!/usr/bin/python
import os
import re
import binascii
import hashlib

#
#
#
# CLASSES
#

# Handle PDF files
class PDF_file:
	
	file_name = ''
	
	def __init__(self,file_name):
		self.file_name = file_name
	
	def uncompress(self):
		os.system('qpdf '+self.file_name+' '+self.file_name+'.uncomp.pdf --stream-data=uncompress')
	
	def compress(self):
		return 0

# Handle 015 numeral integers
class Numerals:
	#nbits = 4
	
	def str_to_binstr(self,str):
		return bin(int(binascii.hexlify(str), 16))

	def binstr_to_num(self,str):
		return int(str,2) % 16
	
	#def bin_to_binstr(self,bin):
	#	return str(bin) if bin<=1 else bin(bin>>1) + str(bin&1)
	
	#def bin_to_str(self,bin):
	#	return binascii.unhexlify('%x' % int(bin,2))
	
	def hexstr_to_num(self,h):
		return int(h,16) % 16
	
	def split_len(self,seq,length):
		return [seq[i:i+length] for i in range(0,len(seq),length)]
	
	def digest(self,str):
		h = hashlib.sha1()
		h.update(str)
		return h.hexdigest()
	
	def digest_to_nums(self,d):
		return map(self.hexstr_to_num,self.split_len(d,2))
	
	def msg_to_nums(self,msg):
		return map(self.binstr_to_num,self.split_len(self.str_to_binstr(msg),4))
	
	def encode(self,msg,key):
		return [self.digest_to_nums(self.digest(msg)),self.msg_to_nums(msg),self.digest_to_nums(self.digest(key))]

# Generate chaotic maps
class Chaotic:
	passkey = ''
	mu = 0
	
	def __init__(self,passkey,mu):
		self.passkey = passkey
		self.mu = mu
	
	def next(self,x):
		return self.mu * x * (1 - x)

# Perform the stego algorithm
class PDF_stego:
	passkey = ''
	
	def __init__(self,name,passkey):
		self.passkey = passkey
		self.file_op = PDF_file(name)
		self.file_op.uncompress()
	
	def embed(self):
		cover_file = open(self.file_op.file_name + ".uncomp.pdf")
		for line in cover_file:
			m = re.search(r'\[.*\][ ]?TJ',line) #WARNING: use "search", DO NOT use "match"
			if m != None:
				print(line+ "\n") 
			
	
	def sub_embed(self,line):
		return 0

#
#
#
# UTILITIES
#

def print_nums(name, nums):
	print '===== ' + name + ' ====='
	print nums

#
#
#
# TESTS & EXAMPLES
#
		
#ps = PDF_stego("test.pdf","abcd")
#ps.embed()

#nums = Numerals().encode("lorem ipsum sin dolor amet", "abcd1234")
#print_nums('Flagstr1', nums[0])
#print_nums('Message', nums[1])
#print_nums('Flagstr2', nums[2])
