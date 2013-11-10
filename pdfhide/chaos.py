#!/usr/bin/python3

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
# chaos.py
__version__ = "0.0"
#
# This is a straightforward implementation of chaotic maps for pdf_hide v0.0
#
# Written by Nicolas Canceill
# Last updated on Nov 10, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
# This module implements chaotic maps for the pdf_hide algo.
#
# It implements logistic recursive map of the following type:
# ##### x -> mu * x * (1 - x) #####
# This map presents a chaotic behavior for most values of 'mu'
# strictly comprised between 3.57 and 4.
#
# A chaotic map is initiated with the 'mu' parameter in ]3.57,4[
# and with an initial value of 'x' generated from the 'flagstr'
# parameter according to the pdf_hide algo.
#
# After that, the 'next()' method can be used to simultaneously
# generate and retrieve the next value from the chaotic map.
#

class Chaotic:

	mu = 3.9
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
