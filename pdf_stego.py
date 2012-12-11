#!/usr/bin/python
import os
import re
import hashlib
from optparse import OptionParser

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

	# Generates QDF file "<file>.qdf" from PDF file "<file>", uncompressing streams if needed
	def uncompress(self):
		os.system('qpdf '+self.file_name+' '+self.file_name+'.qdf --qdf --stream-data=uncompress')

	# Generates fixed QDF  file "<file>.fix" from damaged QDF file "<file>", reconstructing XRef and trailer if needed
	def fix(self):
		os.system('fix-qdf <'+self.file_name+' >'+self.file_name+'.fix')

	# Generates PDF file "<file>.pdf" from QDF or PDF file "<file>", compressing streams if needed
	def compress(self):
		os.system('qpdf '+self.file_name+' '+self.file_name+'.pdf --stream-data=compress')

# Handle 015 and 116 numeral integers, and binary strings, and other stuff
class Numerals:
	#nbits = 4

	# Encodes a string into a binary string based on the ASCII codes (e.g. "a" returns "01100001")
	def str_to_binstr(self,str):
		if str.__len__() < 1:
			return ""
		else:
			result = ""
			for c in str:
				b = bin(ord(c))[2:]
				while b.__len__() < 8:
					b = "0" + b
				result += b
			return result

	# Encodes a 4-bit number (passed-in as a binary string, e.g. "0110") into a "015" numeral
	def binstr_to_num(self,str):
		return int(str,2) % 16

	# Encodes an ASCII code (passed-in as an hexadecimal string) into a "015" numeral using mod(16)
	def hexstr_to_num(self,h):
		return int(h,16) % 16

	# Decodes a character from two "015" numerals according to the algo
	def nums_to_ch(self,i,j):
		return chr(16 * i + j)

	# Splits a sequence into a list of sequences of specified length (the last one may be shorter)
	def split_len(self,seq,length):
		return [seq[i:i+length] for i in range(0,len(seq),length)]

	# Returns the 20-byte SHA1 digest of a string as an hexadecimal string
	def digest(self,str):
		return hashlib.sha1(str).hexdigest()

	# Encodes a 20-byte SHA1 digest to a list of 20 "015" numerals array according to the algo
	def digest_to_nums(self,d):
		return map(self.hexstr_to_num,self.split_len(self.digest(d),2))

	# Encodes a message to a list of "015" numerals according to the algo
	def msg_to_nums(self,msg):
		return map(self.binstr_to_num,self.split_len(self.str_to_binstr(msg),4))

	# Encodes a message and a stego key according to the algo
	#
	# Returns a list n[]:
	# n[0] is the list of 20 "015" numerals representing "FlagStr1"
	# n[1] is the list of "015" numerals representing the message
	# n[2] is the list of 20 "015" numerals representing "FlagStr2"
	def encode_msg(self,msg,key):
		return [self.digest_to_nums(msg),self.msg_to_nums(msg),self.digest_to_nums(key)]

	# Encodes a derived key according to the algo
	#
	# Returns the list of 20 "015" numerals representing "FlagStr"
	def encode_key(self,key):
		return self.digest_to_nums(key)

# Generate chaotic maps
class Chaotic:
	mu = 3.6
	x = 0
	
	def __init__(self,mu,flagstr):
		self.mu = mu
		self.x = self.gen_chaokey(flagstr)

	# Generates a chaotic key (seed for the chaotic map) according to the algo
	def gen_chaokey(self,flagstr):
		dec = ""
		for i in flagstr:
			dec = dec + str(i)
		return float("0." + dec)

	# Gets the next real number from the chaotic map
	def next(self):
		x_ = self.mu * self.x * (1 - self.x)
		self.x = x_
		return self.x

# Perform the stego algorithm
class PDF_stego:
	# Debug logging flag
	debug = False

	# Redundancy parameter, should be in ]0,1[
	redundancy = 0.1

	# Chaotic map parameters, should be in ]3.57,4[
	mu_one = 3.7
	mu_two = 3.8

	# Counter for TJ operators
	tj_count = 0
	
	def __init__(self,input,debug):
		self.file_op = PDF_file(input)
		self.debug = debug

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
		if abs(val) > 16 or val == 0:
			# Do not use TJ op
			return [False,val]
		self.tj_count += 1
		if ch_two < self.redundancy or num == None:
			# Use TJ op for a random value
			if val < 0:
				return [False,-(int(15 * ch_one) + 1 )]
			return [False,int(15 * ch_one) + 1]
		# Use TJ op for data
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
	def embed_line(self,line,ch_one,ch_two,ind,i):
		newline = line
		i_ = i
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
					op = self.embed_op(tj,ch_one.next(),ch_two.next(),ind[i_])
				else:
					# No more numerals to embed
					op = self.embed_op(tj,ch_one.next(),ch_two.next(),None)
				if op[0]:
					# One numeral was embedded, update IND index
					i_ += 1
				# Insert new value
				newline = newline[:k + m.start(1)] + str(op[1]) + newline[k + m.end(1):]
				# Update current position
				k += m.start(1) + str(op[1]).__len__()
		return [newline,i_]

	# Embeds data with passkey in a PDF file "<file>", outputs stego PDF file "<file>.out.fix.pdf"
	#
	# Returns the number of embedded "015" numbers constituting the data
	def embed(self,data,passkey):
		self.tj_count = 0
		if self.debug:
			print "\n========== BEGIN EMBED ==========\n"
		print "Embedding with key \"" + passkey + "\" in file \"" + self.file_op.file_name + ".qdf\"..."
		self.file_op.uncompress()
		cover_file = open(self.file_op.file_name + ".qdf")
		new_file = ""
		n = Numerals()
		# Get the numerals to embed from the key and the message
		nums = n.encode_msg(data,passkey)
		if self.debug:
			print_nums('FlagStr1 (CheckStr)',nums[0])
			print_nums('FlagStr2',nums[2])
			print_nums('Data',n.msg_to_nums(data))
		# Initiate chaotic maps
		ch_one = Chaotic(self.mu_one,nums[2])
		ch_two = Chaotic(self.mu_two,nums[2])
		ind = nums[0] + nums[1] + nums[2]
		i = 0
		# Parse file
		for line in cover_file:
			# Parse line for TJ blocks
			m = re.search(r'\[(.*)\][ ]?TJ',line)
			if m == None:
				# No TJ blocks
				new_file += line
			else:
				# Try to embed data in TJ block
				newline = self.embed_line(m.group(1),ch_one,ch_two,ind,i)
				# Insert new block
				new_file += line[:m.start(1)] + newline[0] + line[m.end(1):]
				i = newline[1]
		cover_file.close()
		print "Embedded:\n\"" + data + "\""
		if i < ind.__len__():
			print "Error: not enough space available"
			if self.debug:
				print "\n========== END EMBED ==========\n"
			return 0
		else:
			output_file = open(self.file_op.file_name + ".out","w")
			output_file.write(new_file)
			output_file.close()
			output = PDF_file(self.file_op.file_name + ".out")
			output.fix()
			output_fixed = PDF_file(self.file_op.file_name + ".out.fix")
			output_fixed.compress()
			print "Wrote compressed PDF to \"" + self.file_op.file_name + ".out.fix.pdf\" with " + str(self.tj_count) + " TJ ops (" + str(nums[1].__len__()) + " of them used for data)\n"
			if self.debug:
				print "\n========== END EMBED ==========\n"
			return nums[1].__len__()

	def extract_op(self,val,ch_two):
		self.tj_count += 1
		if abs(val) > 16 or val == 0 or ch_two < self.redundancy:
			# Do not use TJ op
			return 0
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
				tj = self.extract_op(int(m.group(1)),ch_two.next())
				if tj != 0:
					# Get value
					tjs += [tj - 1]
				# Update current position
				k += m.end(1)
		return tjs

	# Extracts data of known length from PDF file "<file>" using derived_key, outputs extracted data to "<file>.embd"
	def extract(self,derived_key,length):
		self.tj_count = 0
		if self.debug:
			print "\n========== BEGIN EXTRACT ==========\n"
		print "Extracting with key \"" + derived_key + "\" from file \"" + self.file_op.file_name + "\"..."
		# Only works for valid PDF files
		self.file_op.uncompress()
		embedding_file = open(self.file_op.file_name + '.qdf')
		n = Numerals()
		# Get the numerals from the key
		nums = n.encode_key(derived_key)
		if self.debug:
			print_nums('FlagStr',nums)
		# Initiate chaotic map
		ch_two = Chaotic(self.mu_two,nums)
		tjs = []
		# Parse file
		for line in embedding_file:
			# Parse line for TJ blocks
			m = re.search(r'\[(.*)\][ ]?TJ',line)
			if m != None:
				# Try to extract data from TJ block
				tjs += self.extract_line(line,ch_two)
		embedding_file.close()
		if tjs.__len__() < 40 + length:
			print "Error: not enough valid data to retrieve message: " + str(40 + length) + " > " + str(tjs.__len__())
		else:
			checkstr = tjs[:20]
			embedded = tjs[20:tjs.__len__() - 20]
			k = 0
			emb_str = ""
			# Decode embedded data
			while k < length - 1:
				emb_str += n.nums_to_ch(embedded[k],embedded[k + 1])
				k += 2
			if self.debug:
				print_nums('Data Checksum',n.encode_key(emb_str))
				print_nums('CheckStr',checkstr)
				print_nums('Data',n.msg_to_nums(emb_str))
			# Check integrity
			if n.digest_to_nums(emb_str) != checkstr:
				print "Error: CheckStr does not match embedded data from " + str(self.tj_count) + " TJ ops (" + str(tjs.__len__() - 40) + " of them used for data)"
				if self.debug:
					print "===== Raw data (corrupted) ====="
					print emb_str
			else:
				print "Extracted:\n\"" + emb_str + "\""
				output_file = open(self.file_op.file_name + ".embd","w")
				output_file.write(emb_str)
				print "Wrote embedded data to \"" + self.file_op.file_name + ".embd\" from " + str(self.tj_count) + " TJ ops (" + str(length) + " of them used for data)\n"
				output_file.close()
		if self.debug:
			print "\n========== END EXTRACT ==========\n"

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
# SCRIPT
#

def main():
	parser = OptionParser(usage="%prog {embed|extract} [options]", version="%prog 0.0b")
	parser.add_option("-f", "--file", dest="filename",
					  help="use PDF file (may be compressed) FILENAME as input [default: \"test.pdf\"]", metavar="FILENAME")
	parser.add_option("-k", "--key", dest="key",
					  help="use KEY as the stego-key", metavar="KEY")
	parser.add_option("-m", "--message", dest="msg",
					  help="use MESSAGE as the data to embed (ignored if extracting)", metavar="MESSAGE")
	parser.add_option("-l", "--message-length", dest="l",
					  help="use LENGTH as the length of the data to extract (ignored if embedding)", metavar="LENGTH")
	parser.add_option("-d", "--debug",
					  action="store_true", dest="debug", default=False,
					  help="print debug messages")
	(options, args) = parser.parse_args()
	if args.__len__() != 1:
		parser.error("Please use command \"embed\" only or command \"extract\" only.")
	if args[0] == "embed":
		if options.filename == None:
			options.filename = raw_input("Please enter input file name: [\"test.pdf\"]")
		if options.filename.__len__() == 0:
			if options.debug:
				print "No file name provided, using default: \"test.pdf\""
			options.filename = "test.pdf"
		if options.key == None:
			options.key = raw_input("Please enter stego-key: ")
		if options.msg == None:
			options.msg = raw_input("Please enter the message to embed: ")
		ps = PDF_stego(options.filename,options.debug)
		l = ps.embed(options.msg,options.key)
	elif args[0] == "extract":
		if options.filename == None:
			options.filename = raw_input("Please enter input file name: [\"test.pdf\"]")
		if options.filename.__len__() == 0:
			if options.debug:
				print "No file name provided, using default: \"test.pdf\""
		if options.key == None:
			options.key = raw_input("Please enter derived-key: ")
		if options.l == None:
			options.l = int(raw_input("Please enter data length: "))
		ps = PDF_stego(options.filename,options.debug)
		ps.extract(options.key,options.l)
	else:
		parser.error("Please use command \"embed\" only or command \"extract\" only.")

if __name__ == '__main__':
    main()
