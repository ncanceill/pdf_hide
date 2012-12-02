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
		# TODO
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
	mu = 3.6
	x = 0.5
	
	def __init__(self,mu,flagstr):
		self.mu = mu
		self.x = self.gen_chaokey(flagstr)
	
	def gen_chaokey(self,flagstr):
		dec = ""
		for i in flagstr:
			dec = dec + str(i)
		return float("0." + dec)
	
	def next(self):
		x_ = self.mu * self.x * (1 - self.x)
		self.x = x_
		return self.x

# Perform the stego algorithm
class PDF_stego:
	redundancy = 0.1
	mu_one = 3.7
	mu_two = 3.8
	passkey = ''
	data = ''
	
	def __init__(self,name,passkey,data):
		self.passkey = passkey
		self.data = data
		self.file_op = PDF_file(name)
		self.file_op.uncompress()
	
	# Returns a list res[]
	# If res[0] == True then num was embedded, move on to next numeral
	# If res[0] == False then try to embed num again in the nex operator
	# res[1] is the new operator value (regardless of res[0])
	# Pass None as num to significate that the IND has been taken to finish
	def embed_op(self,val,ch_one,ch_two,num):
		if abs(val) > 16:
			return [False,val]
		if ch_two < self.redundancy or num == None:
			return [False,ch_one]
		if val < 0:
			return [True, -num]
		return [True, num]

	def embed_line(self,line,ch_one,ch_two,ind,i):
		newline = line
		i_ = i
		k = 0
		while k < newline.__len__():
			# WARNING: use "re.search", DO NOT use "re.match"
			m = re.search(r'\)(\-?[0-9]+)\(',newline[k:])
			if m == None:
				k = newline.__len__()
			else:
				tj = int(m.group(1))
				if i_ < ind.__len__():
					op = self.embed_op(tj,ch_one.next(),ch_two.next(),ind[i_])
				else:
					op = self.embed_op(tj,ch_one.next(),ch_two.next(),None)
				if op[0]:
					i_ += 1
				newline = newline[:k + m.start(1)] + str(op[1]) + newline[k + m.end(1):]
				k = k + m.start(1) + str(op[1]).__len__()
		return [newline,i_]
	
	def embed(self):
		cover_file = open(self.file_op.file_name + ".uncomp.pdf")
		new_file = ""
		nums = Numerals().encode(self.data, self.passkey)
		ch_one = Chaotic(self.mu_one,nums[2])
		ch_two = Chaotic(self.mu_two,nums[2])
		ind = nums[0] + nums[1] + nums[2]
		i = 0
		for line in cover_file:
			# WARNING: use "re.search", DO NOT use "re.match"
			m = re.search(r'\[(.*)\][ ]?TJ',line)
			if m == None:
				new_file += line
			else:
				newline = self.embed_line(m.group(1),ch_one,ch_two,ind,i)
				new_file += line[:m.start(1)] + newline[0] + line[m.end(1):]
				i = newline[1]
		return new_file # TODO create and compress new pdf

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

# Encoding message and key to numerals
#nums = Numerals().encode("lorem ipsum sin dolor amet", "abcd1234")
#print_nums('Flagstr1', nums[0])
#print_nums('Message', nums[1])
#print_nums('Flagstr2', nums[2])

# Running the whole alogorithm
#ps = PDF_stego("test.pdf","lorem ipsum sin dolor amet","abcd1234")
#ps.embed()
