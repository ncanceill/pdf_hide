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
NAME=pdf_hide
VERSION=0.0
#
# This is a Makefile for pdf_hide samples v0.0
#
# Written by Nicolas Canceill
# Last updated on Nov 10, 2013
# Hosted at https://github.com/ncanceill/pdf_hide
#

#
#
#
# VARS
#


#
# Exts

TX=.tex
TXT=.txt
PDF=.pdf

#
# Tools

RM_B=rm
RM_F=-rf
RM=$(RM_B) $(RM_F)

PDFL_B=pdflatex
PDFL_F=
PDFL=$(PDFL_B) $(PDFL_F)

#
# Names

LATEX_1=part$(TX).1
LATEX_2=part$(TX).2

TXT_PARAG=lorem$(TXT)

OUT=test
OUT_LONG=test_long
OUT_E=test_e$(PDF)
OUT_MSG=msg

#
#
#
# TARGETS
#

all: $(OUT)$(PDF) $(OUT_LONG)$(PDF)

$(OUT)$(TX): $(LATEX_1) $(LATEX_2) $(TXT_PARAG)
	cat $(LATEX_1) > $(OUT)$(TX)
	cat $(TXT_PARAG) >> $(OUT)$(TX)
	cat $(LATEX_2) >> $(OUT)$(TX)

$(OUT_LONG)$(TX): $(LATEX_1) $(LATEX_2) $(TXT_PARAG)
	cat $(LATEX_1) > $(OUT_LONG)$(TX)
	cat $(TXT_PARAG) >> $(OUT_LONG)$(TX)
	echo >> $(OUT_LONG)$(TX)
	cat $(TXT_PARAG) >> $(OUT_LONG)$(TX)
	echo >> $(OUT_LONG)$(TX)
	cat $(TXT_PARAG) >> $(OUT_LONG)$(TX)
	echo >> $(OUT_LONG)$(TX)
	cat $(TXT_PARAG) >> $(OUT_LONG)$(TX)
	echo >> $(OUT_LONG)$(TX)
	cat $(TXT_PARAG) >> $(OUT_LONG)$(TX)
	echo >> $(OUT_LONG)$(TX)
	cat $(TXT_PARAG) >> $(OUT_LONG)$(TX)
	echo >> $(OUT_LONG)$(TX)
	cat $(TXT_PARAG) >> $(OUT_LONG)$(TX)
	echo >> $(OUT_LONG)$(TX)
	cat $(TXT_PARAG) >> $(OUT_LONG)$(TX)
	echo >> $(OUT_LONG)$(TX)
	cat $(TXT_PARAG) >> $(OUT_LONG)$(TX)
	echo >> $(OUT_LONG)$(TX)
	cat $(TXT_PARAG) >> $(OUT_LONG)$(TX)
	echo >> $(OUT_LONG)$(TX)
	cat $(LATEX_2) >> $(OUT_LONG)$(TX)

%$(PDF): %$(TX)
	$(PDFL) $*

#
# Clean

clean: clean-base clean-long
	$(RM) $(OUT_E)
	$(RM) $(OUT_MSG)

clean-base:
	$(RM) $(OUT).*

clean-long:
	$(RM) $(OUT_LONG).*
