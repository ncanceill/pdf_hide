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
# This is a Makefile for pdf_hide v0.0
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
PYTEST_F=-m
PYTEST=$(PYTH_B) $(PYTEST_F)

#
# Names

SETUP=setup$(PY)

MK=Makefile $(SAMPLE_D)/Makefile
UTL=README.md LICENSE.md DISCLAIMER.md

SRC_D=src
SRC=$(SRC_D)/*$(PY)

BUILD_D=build
DIST_D=dist

SAMPLE_D=sample
SAMPLE=$(SAMPLE_D)/*.txt $(SAMPLE_D)/*.tex*

TEST_D=test
TEST=tests
TESTS=$(TEST_D)/$(TEST)$(PY)

#
#
#
# TARGETS
#

all: builds

#
# Main

builds:
	$(PYTH) $(SETUP) build

install:
	$(PYTH) $(SETUP) install

#
# Package

pkg: $(SRC) $(SAMPLE) $(TESTS) $(MK) $(UTL) clean
	$(PYTH) $(SETUP) sdist

#
# Tests

samples:
	make -C $(SAMPLE_D) all

tests: samples
	$(PYTEST) $(TEST_D).$(TEST)

#
# Clean

clean: clean-sample clean-build clean-pkg

clean-sample:
	make -C $(SAMPLE_D) clean

clean-build:
	$(RM) $(BUILD_D)/*

clean-pkg:
	$(RM) $(DIST_D)/*
