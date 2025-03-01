.ONESHELL:

all: compila executa
compila: 
	python -m venv guilherme_venv
	source guilherme_venv/bin/activate
	pip install pystan matplotlib pandas seaborn
executa: 
	python main.py  > relatorio 2>&1
clear: 
	rm -r arquivosaida guilherme_venv figs intermediario.csv