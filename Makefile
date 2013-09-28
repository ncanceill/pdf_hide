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
# This is a Makefile for pdf_hide v0.0a
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

PY=.py
PYC=.pyc
TGZ=.tgz

#
# Tools

RM_B=rm
RM_F=-rf
RM=$(RM_B) $(RM_F)

TAR_B=tar
TAR_F=-acvzf
TAR=$(TAR_B) $(TAR_F)

PYTH_B=python3
PYTH_F=
PYTH=$(PYTH_B) $(PYTH_F)

#
# Names

SRC_D=src
SRC=$(SRC_D)/*$(PY)

SAMPLE_D=sample
ADD=$(SAMPLE_D)/*

UTL=Makefile README.md

TEST_D=$(SRC_D)
TEST=tests$(PY)

#
#
#
# TARGETS
#

all:

#
# Package

pkg: $(SRC) clean
	$(TAR) $(NAME)-$(VERSION)$(TGZ) $(SRC) $(UTL) $(ADD)

#
# Tests

samples:
	make -C $(SAMPLE_D) all

test: samples
	cd $(TEST_D) && $(PYTH) $(TEST)
	make -C $(SAMPLE_D) clean

#
# Clean

clean:
	make -C $(SAMPLE_D) clean

clean-pkg:
	$(RM) $(NAME)-$(VERSION)$(TGZ)
