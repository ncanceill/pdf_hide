#!/usr/bin/python3
import sys
import select
import argparse

import logger
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
# This is a steganographic tool for hiding data in PDF files
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
	# CLI
	parser = argparse.ArgumentParser(prog="pdf_hide",formatter_class=argparse.RawDescriptionHelpFormatter,
						description=logger.MSG_DESC,epilog=logger.MSG_LICENSE)
	parser.add_argument("action",choices=["embed","extract"],
						help="action to execute")
	parser.add_argument("filename",default="test.pdf",
						help="PDF file (may be compressed) to use as input")
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
	parser.add_argument("-v", "--verbose", action="count", dest="verbose", default=0,
						help="set verbosity level")
	parser.add_argument("-q", "--quiet", action="store_const", dest="verbose", const=-1,
						help="force quiet output")
	parser.add_argument("--version", action="version", version=logger.MSG_VERSION)
	args = parser.parse_args()
	# Log
	rl = logger.rootLogger(args.verbose)
	# Exec
	if args.verbose >= 0:
		rl.print_splash()
	if args.action == "embed":
		if select.select([sys.stdin,],[],[],0.0)[0]:#TODO: use argparse to do that
			inputt = ""
			for line in sys.stdin:
				if inputt.__len__() > 0:
					inputt += "\n"
				inputt += line
			sys.stdin = open("/dev/tty")
			args.msg = inputt
		if args.key == None:
			args.key = input("PDF_HIDE: Please enter stego-key:\n")
		ps = pdf_algo.PDF_stego(args.filename,rl,improve=args.improve,red=args.red,nbits=args.nbits,customrange=args.customrange)
		result = ps.embed(args.msg,args.key,norandom=args.norandom)
		if args.verbose >= 0:
			rl.print_discl()
		if result > 0:
			exit(0)
		exit(result)
	elif args.action == "extract":
		if args.key == None:
			args.key = input("PDF_HIDE: Please enter derived-key:\n")
		ps = pdf_algo.PDF_stego(args.filename,rl,args.improve,args.red,args.nbits,args.customrange)
		result = ps.extract(args.key)
		if args.verbose >= 0:
			rl.print_discl()
		exit(result)

if __name__ == '__main__':
    main()
