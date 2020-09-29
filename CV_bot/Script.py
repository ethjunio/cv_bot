import numpy as np 
import pandas as pd
import os
import subprocess

df = pd.read_csv("CSV.csv")


## CREATE A DICTIONARE OUT OF THE CSV DATA
dict_template = dict()
for elem in df.columns:
	dict_template[elem] = df.iloc[0][elem]


## REPLACE & SYMBOL WITH AND, OTHERWISE LATEX CODE DOES NOT COMPILE
## REPLACE 6.0 WITH 6 (ORIGINAL DF COLUMNS FOR GRADES ARE FLOAT)
for key, value in dict_template.items():
	if(str(value).find('&')>=0):
		dict_template[key] = str(value).replace('&','and')
	if(str(value).find('6.0')>=0):
		dict_template[key] = str(value).replace('6.0','6')


## REPLACE PLACEHOLDERS IN LATEX TEMPLATE WITH VALUES EXCTRACTED FROM THE CSV FILE, THEN CREATE THE FINAL LATEX TEMPLATE
with open('Latex_template.tex','r') as file:
	text = file.read()

	for key, value in dict_template.items():
		text = text.replace('$'+key+'$', str(value))

	with open('Latex_template_modified.tex', 'w') as output:
		output.write(text)



subprocess.run(["pdflatex","Latex_template_modified.tex"])