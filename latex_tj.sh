#!/bin/bash

#
#
#
# latex_tj.sh
NAME=latex_tj.sh
#
# Version 0.0
VERSION=0.0
#
# This script generates a LaTeX files from a texte, and compiles it.
# Then it examines the TJ operators in the generated PDF.
#
# Created by Nicolas Canceill for the SSN project.
#

#
#
#
# Global variables
#
# SHOULD NOT be modified
#

#
# Files
#

# The first part of the LaTeX file
LATEX_F="part.tex.1"

# The first part of the LaTeX file
LATEX_S="part.tex.2"

#
# Parameters
#

# The file name to use
TXT_PARAG=

#
# Messages: English
#

# The opening message
MSG_OPENING_EN="This is $NAME v$VERSION - Created by Nicolas Canceill for the SSN project"

#
#
#
# Functions
#
# SHOULD NOT be modified
#

# Generates the LaTeX file
gen_latex()
{
	cat $LATEX_F > $TXT_PARAG".tex"
	cat $TXT_PARAG >> $TXT_PARAG".tex"
	cat $LATEX_S >> $TXT_PARAG".tex"
}

# Generates the QPDF
gen_qpdf()
{
	pdflatex $TXT_PARAG".tex"
	qpdf $TXT_PARAG".pdf" $TXT_PARAG".q.pdf" --stream-data=uncompress
}

get_tj()
{
	grep -aoE '\[.*\]TJ' $TXT_PARAG".q.pdf" | grep -aoE '\)[-]?[0-9]+\(' | tr -d '()' | sort -n | uniq -c
}

#
#
#
# Script
#
# MUST NOT be modified
#

echo $MSG_OPENING_EN
for i in $@
do
	TXT_PARAG=$i
	gen_latex
	gen_qpdf
	get_tj > $TXT_PARAG".tj"
done



