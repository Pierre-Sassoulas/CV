all: CV readme
	git add CV*.pdf
	git add readme.md

CV:
	TEXINPUTS=${TEXINPUTS}:"$(shell pwd)/moderncv/";\
	export TEXINPUTS;\
	xelatex CV*.tex;\
	make clean;\

preinstall:
	sudo apt-get install -y texlive-xetex texlive-bibtex-extra texlive-pstricks texlive-fonts-extra

readme:
	python create_readme.py CV_SASSOULAS_Pierre.tex

clean:
	rm -f *.aux *.cb *.cb2 *.log *.toc *.out
