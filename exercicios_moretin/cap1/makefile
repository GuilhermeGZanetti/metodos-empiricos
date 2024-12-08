.ONESHELL:

all: compila executa
compila: 
	python -m venv guilherme_venv
	source guilherme_venv/bin/activate
	pip install numpy matplotlib
executa: 
	python main.py > arquivosaida
clear: 
	rm -r arquivosaida guilherme_venv linear_regression.png