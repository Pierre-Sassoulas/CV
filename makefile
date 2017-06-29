all: CV readme
	git add CV*.pdf
	git add readme.md

CV:
	TEXINPUTS=${TEXINPUTS}:"$(shell pwd)/moderncv/";\
	export TEXINPUTS;\
	xelatex CV*.tex;\
	make clean;\

readme:
	python create_readme.py CV_SASSOULAS_Pierre.tex

clean:
	rm -f *.aux *.cb *.cb2 *.log *.toc *.out
