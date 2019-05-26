ctype.png : ctype.pdf
	pdftoppm -png -singlefile -scale-to-x 850 -scale-to-y -1 $< $(basename $@)

ctype.pdf : ctype.bh ../binheat.py
	python3 -m pip-run -q .. -- -m binheat $< $@
