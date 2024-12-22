.ONESHELL:

all: compila executa
compila: 
	python -m venv guilherme_venv
	source guilherme_venv/bin/activate
	pip install pystan matplotlib pandas
executa: 
	python main.py > arquivosaida
clear: 
	rm -r arquivosaida guilherme_venv figs