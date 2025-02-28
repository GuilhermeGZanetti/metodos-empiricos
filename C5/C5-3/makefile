.ONESHELL:

all: compila executa
compila: 
	python -m venv guilherme_venv
	source guilherme_venv/bin/activate
	pip install pystan matplotlib pandas seaborn scipy
executa: 
	python main.py arquivoentrada > arquivosaida 2>&1
clear: 
	rm -r arquivosaida guilherme_venv figs build