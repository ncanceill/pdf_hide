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

#
# Clean

clean:
	make -C $(SAMPLE_D) clean

clean-pkg:
	$(RM) $(NAME)-$(VERSION)$(TGZ)
