.ONESHELL:

all: compila executa
compila: 
	python3 -m venv guilherme_venv
	source guilherme_venv/bin/activate
	pip install pystan
executa: 
	python main.py > arquivosaida
clear: 
	source deactivate
	rm -r arquivosaida guilherme_venv