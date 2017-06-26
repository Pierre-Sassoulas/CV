CV:
	TEXINPUTS=${TEXINPUTS}:"$(shell pwd)/moderncv/";\
	export TEXINPUTS;\
	pdflatex CV*.tex;\
	pdflatex CV*.tex;\
	make clean;\

clean:
	rm -f *.aux *.cb *.cb2 *.log *.toc *.out
