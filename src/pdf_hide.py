#!/usr/bin/python3
import sys
import select
import argparse

import pdf_drive
import chaos
import pdf_algo

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
# pdf_hide.py
__version__ = "0.0a"
#
# This is a tool for hiding data in PDF files
#
# Written by Nicolas Canceill
# Last updated on May 6, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
#
#
# SCRIPT
#

def main():
	parser = argparse.ArgumentParser(prog="pdf_hide",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("action",
						help="action to execute: embed|extract")
	parser.add_argument("-f", "--file", dest="filename",
						help="use PDF file (may be compressed) FILENAME as input", metavar="FILENAME")
	parser.add_argument("-k", "--key", dest="key",
					  help="use KEY as the stego-key", metavar="KEY")
	parser.add_argument("-m", "--message", dest="msg",
					  help="use MESSAGE as the data to embed (ignored if extracting)", metavar="MESSAGE")
	parser.add_argument("-n", "--nbits", dest="nbits", action="store", type=int, default=4,
					  help="use NBITS as the number of bits to use for numerals", metavar="NBITS")
	parser.add_argument("-r", "--redundancy", dest="red", action="store", type=float, default=0.1,
						help="use RED as the redundancy parameter (strictly between 0 and 1)", metavar="RED")
	parser.add_argument("-i", "--improve", action="store_true", dest="improve", default=False,
						help="use algo improvements")
	parser.add_argument("--no-random", action="store_true", dest="norandom", default=False,
						help="do not embed random values, keep original ones (ignored if extracting)")
	parser.add_argument("--custom-range", action="store_true", dest="customrange", default=False,
						help="use data in [-450,-250] without -333 and -334 (ignored with original algo, should always be used in combination with --no-random when embedding)")
	parser.add_argument("-d", "--debug", action="store_true", dest="debug", default=False,
						help="print debug messages")
	parser.add_argument("-q", "--quiet", action="store_true", dest="debug", default=False,
						help="do not print info messages")
	args = parser.parse_args()
	if args.action == "embed":
		if select.select([sys.stdin,],[],[],0.0)[0]:
			input = ""
			for line in sys.stdin:
				if input.__len__() > 0:
					input += "\n"
				input += line
			sys.stdin = open("/dev/tty")
			args.msg = input
		if args.msg == None:
			args.msg = raw_input("Please enter the message to embed:\n")
		if args.filename == None:
			args.filename = raw_input("Please enter input file name: [\"test.pdf\"]\n")
		if args.filename.__len__() == 0:
			if args.debug:
				print("No file name provided, using default: \"test.pdf\"")
			args.filename = "test.pdf"
		if args.key == None:
			args.key = raw_input("Please enter stego-key:\n")
		if args.red == None:
			args.red = "0.1"
		ps = PDF_stego(args.filename,args.debug,args.quiet,args.improve,args.red,args.nbits,args.customrange)
		exit(ps.embed(args.msg,args.key,args.norandom))
	elif args[0] == "extract":
		if args.filename == None:
			args.filename = raw_input("Please enter input file name: [\"test.pdf.out.fix.pdf\"]\n")
		if args.filename.__len__() == 0:
			if args.debug:
				print("No file name provided, using default: \"test.pdf.out.fix.pdf\"")
			args.filename = "test.pdf.out.fix.pdf"
		if args.key == None:
			args.key = raw_input("Please enter derived-key:\n")
		ps = PDF_stego(args.filename,args.debug,args.quiet,args.improve,args.red,args.nbits,args.customrange)
		exit(ps.extract(args.key))
	else:
		parser.error("Please use command \"embed\" only or command \"extract\" only.")

if __name__ == '__main__':
    main()
