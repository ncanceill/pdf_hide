#!/usr/bin/python
import os
import re

class PDF_file:
	file_name = ''
	def __init__(self, file_name):
		self.file_name = file_name
	def uncompress(self):
		os.system('qpdf '+self.file_name+' '+self.file_name+'.uncomp.pdf --stream-data=uncompress')
	def compress(self):
		return 0;
class PDF_stego:
	passkey = ''
	
	def __init__(self, name, passkey):
		self.passkey = passkey
		self.file_op = PDF_file(name)
		self.file_op.uncompress()
	
	def embed(self):
		cover_file = open(self.file_op.file_name + ".uncomp.pdf")
		for line in cover_file:
			m = re.match(r'\[.*\][ ]?TJ',line)
			if m != None:
				print(line+ "\n") 
			
	
	def sub_embed(self,line):
		return 0;
		
class Chaotic:
	passkey = ''
	
	def __init__(self,passkey):
		self.passkey = passkey
		
ps = PDF_stego("test.pdf","abcd") 	
ps.embed()		
