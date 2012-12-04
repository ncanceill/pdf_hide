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
		os.system('qpdf '+self.file_name+' '+self.file_name+'.comp.pdf --stream-data=compress')

# Handle 015 and 116 numeral integers, and binary strings, and other stuff
class Numerals:
	#nbits = 4
	
	def str_to_binstr(self,str):
		return bin(int(binascii.hexlify(str), 16))

	def binstr_to_num(self,str):
		return int(str,2) % 16
	
	def hexstr_to_num(self,h):
		return int(h,16) % 16

	def nums_to_ch(self,i,j):
		return chr(16 * i + j)
	
	def split_len(self,seq,length):
		return [seq[i:i+length] for i in range(0,len(seq),length)]
	
	def digest(self,str):
		h = hashlib.sha1()
		h.update(str)
		return h.hexdigest()
	
	def digest_to_nums(self,d):
		return map(self.hexstr_to_num,self.split_len(self.digest(d),2))
	
	def msg_to_nums(self,msg):
		return map(self.binstr_to_num,self.split_len(self.str_to_binstr(msg),4))
	
	def encode_msg(self,msg,key):
		return [self.digest_to_nums(msg),self.msg_to_nums(msg),self.digest_to_nums(key)]
	
	def encode_key(self,key):
		return map(lambda x: x + 1,self.digest_to_nums(key))

#def bin_to_binstr(self,bin):
#	return str(bin) if bin<=1 else bin(bin>>1) + str(bin&1)

#def bin_to_str(self,bin):
#	return binascii.unhexlify('%x' % int(bin,2))

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
	mu_two = 3.9
	
	def __init__(self,input):
		self.file_op = PDF_file(input)
	
	# Returns a list res[]
	# If res[0] == True then num was embedded, move on to next numeral
	# If res[0] == False then try to embed num again in the nex operator
	# res[1] is the new operator value (regardless of res[0])
	# Pass None as num to significate that the IND has been taken to finish
	def embed_op(self,val,ch_one,ch_two,num):
		if abs(val) > 16 or val == 0:
			return [False,val]
		if ch_two < self.redundancy or num == None:
			return [False,int(15*ch_one)+1]
		if val < 0:
			return [True, -num - 1]
		return [True, num + 1]

	def embed_line(self,line,ch_one,ch_two,ind,i):
		newline = line
		i_ = i
		k = 0
		while k < newline.__len__():
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
				k += m.start(1) + str(op[1]).__len__()
		return [newline,i_]
	
	def embed(self,data,passkey):
		print "Embedding \"" + data + "\" with key \"" + passkey + "\" in file \"" + self.file_op.file_name + ".uncomp.pdf\"..."
		self.file_op.uncompress()
		cover_file = open(self.file_op.file_name + ".uncomp.pdf")
		new_file = ""
		nums = Numerals().encode_msg(data,passkey)
		ch_one = Chaotic(self.mu_one,nums[2])
		ch_two = Chaotic(self.mu_two,nums[2])
		ind = nums[0] + nums[1] + nums[2]
		i = 0
		for line in cover_file:
			m = re.search(r'\[(.*)\][ ]?TJ',line)
			if m == None:
				new_file += line
			else:
				newline = self.embed_line(m.group(1),ch_one,ch_two,ind,i)
				new_file += line[:m.start(1)] + newline[0] + line[m.end(1):]
				i = newline[1]
		if i < ind.__len__():
			print "Error: not enough space available"
		else:
			output_file = open(self.file_op.file_name + ".out.pdf","w")
			output_file.write(new_file)
			print "Wrote uncompressed PDF to \"" + self.file_op.file_name + ".out.pdf\""
			#output = PDF_file(self.file_op.file_name + ".out.pdf")
			#output.compress() # TODO: update checksum

	def extract_op(self,val,ch_two):
		if abs(val) > 16 or val == 0 or ch_two < self.redundancy:
			return 0
		return abs(val)

	def extract_line(self,line,ch_two):
		k = 0
		tjs = []
		while k < line.__len__():
			m = re.search(r'\)(\-?[0-9]+)\(',line[k:])
			if m == None:
				k = line.__len__()
			else:
				tj = self.extract_op(int(m.group(1)),ch_two.next)
				if tj != 0:
					tjs += [tj - 1]
				k += m.end(1)
		return tjs

	def extract(self,derived_key):
		print "Extracting with key \"" + derived_key + "\" from file \"" + self.file_op.file_name + "\"..."
		# Only works for valid PDF files
		#self.file_op.uncompress()
		#embedding_file = open(self.file_op.file_name + ".uncomp.pdf")
		embedding_file = open(self.file_op.file_name)
		n = Numerals()
		nums = n.encode_key(derived_key)
		ch_two = Chaotic(self.mu_two,nums)
		tjs = []
		for line in embedding_file:
			m = re.search(r'\[(.*)\][ ]?TJ',line)
			if m != None:
				tjs += self.extract_line(line,ch_two)
		if tjs.__len__() < 42:
			print "Error: not enough valid data to retrieve message: 42 > " + str(tjs.__len__())
		else:
			checkstr = tjs[:20]
			embedded = tjs[20:tjs.__len__() - 20]
			k = 0
			emb_str = ""
			while k < embedded.__len__() - 1:
				emb_str += n.nums_to_ch(embedded[k],embedded[k + 1])
				k += 1
			if n.digest_to_nums(emb_str) != checkstr:
				print "Error: CheckStr does not match embedded data:"
				print_nums('Data Checksum',n.encode_key(emb_str))
				print_nums('CheckStr',checkstr)
				print "Raw data (corrupted): " + emb_str
			else:
				output_file = open(self.file_op.file_name + ".embd","w")
				output_file.write(emb_str)
				print "Wrote embedded data to \"" + self.file_op.file_name + ".embd\""

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
#nums = Numerals().encode_msg("lorem ipsum sin dolor amet","abcd1234")
#print_nums('FlagStr1',nums[0])
#print_nums('Message',nums[1])
#print_nums('FlagStr2',nums[2])

# Encoding derived key to numerals
#nums = Numerals().encode_key("abcd1234")
#print_nums('FlagStr',nums)

# Running the embedding alogorithm
ps = PDF_stego("test.pdf")
ps.embed("lorem ipsum","abcd1234")

# Running the extracting alogorithm
ps = PDF_stego("test.pdf.out.pdf")
ps.extract("abcd1234")
