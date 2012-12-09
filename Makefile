LATEX_TJ="./latex_tj.sh"
FILENAME=test

pdf: $(FILENAME)
	$(LATEX_TJ) $(FILENAME)

clean:
	rm -rf $(FILENAME).*
