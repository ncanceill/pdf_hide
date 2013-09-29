#
#
#
# PDF HIDE
#

#
# DISCLAIMER: This software is provided for free, with full copyrights, and without any warranty.
#
NAME=pdf_hide
VERSION=0.0a
#
# This is a Makefile for pdf_hide samples v0.0a
#
# Written by Nicolas Canceill
# Last updated on Sept 28, 2013
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
OUT_=test_long

#
#
#
# TARGETS
#

all: $(OUT)$(PDF) $(OUT_)$(PDF)

$(OUT)$(TX): $(LATEX_1) $(LATEX_2) $(TXT_PARAG)
	cat $(LATEX_1) > $(OUT)$(TX)
	cat $(TXT_PARAG) >> $(OUT)$(TX)
	cat $(LATEX_2) >> $(OUT)$(TX)

$(OUT_)$(TX): $(LATEX_1) $(LATEX_2) $(TXT_PARAG)
	cat $(LATEX_1) > $(OUT_)$(TX)
	cat $(TXT_PARAG) >> $(OUT_)$(TX)
	echo >> $(OUT_)$(TX)
	cat $(TXT_PARAG) >> $(OUT_)$(TX)
	echo >> $(OUT_)$(TX)
	cat $(TXT_PARAG) >> $(OUT_)$(TX)
	echo >> $(OUT_)$(TX)
	cat $(TXT_PARAG) >> $(OUT_)$(TX)
	echo >> $(OUT_)$(TX)
	cat $(LATEX_2) >> $(OUT_)$(TX)

%$(PDF): %$(TX)
	$(PDFL) $*

#
# Clean

clean: clean-base clean-long

clean-base:
	$(RM) $(OUT).*

clean-long:
	$(RM) $(OUT_).*
