#
#
#
# PDF HIDE
#

#
# DISCLAIMER: This software is provided for free, with full copyrights, and without any warranty.
#

#
# Makefile
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

NAME=pdf_hide
VERSION=0.0a

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

UTL=Makefile README.md

TEST=$(SRC_D)/tests$(PY)

#
#
#
# TARGETS
#

#
# Package

pkg: $(SRC) clean
	$(TAR) $(NAME)-$(VERSION)$(TGZ) $(SRC) $(UTL)

#
# Tests

test: $(SRC)
	$(PYTH) $(TEST)

#
# Clean

clean:

clean-pkg:
	$(RM) $(NAME)-$(VERSION)$(TGZ)
