import numpy as np 
import pandas as pd
import os
import subprocess
import json	

f = open('Schedule.json',) 
dict_interviews = json.load(f)



set_users = set()
set_companies = set()
for elem in dict_interviews['interviews']:
	set_users.add(elem['candidateId'])
	set_companies.add(elem['companyId'])





for user in set_users:
	user_interviews = []
	for elem in dict_interviews['interviews']:
		if(elem['candidateId'] == user):
			user_interviews.append(elem)

	user_interviews = sorted(user_interviews, key=lambda elem: elem['timeSlot']['id']) 
	string = ''
	for index,elem in enumerate(user_interviews):
		if(index%2==0):
			string += '\\IS{' + elem['timeSlot']['timeRange'] + '}' + '{' + elem['companyId'] + '}' + '{' + elem['interviewRoom']['name'] + '}' + '{' + str(index + 1) + '}' + '\n'
		else:
			string += '\\CT{' + elem['timeSlot']['timeRange'] + '}' + '{' + elem['companyId'] + '}' + '{' + elem['interviewRoom']['name'] + '}' + '{' + str(index + 1) + '}' + '\n'


	file = open('Latex_template.tex','r')
	text = file.read()
	text = text.replace('$Interviews$', string)
	text = text.replace('$Name$', user)
	file.close()

	user = str(user).replace(' ','_')
	with open('users/' + user + '_schedule.tex', 'w') as output:
		output.write(text)
		output.close()

			
	os.system('pdflatex -interaction=batchmode -output-directory=Users/ Users/'+ str(user).replace(' ','_') + '_schedule.tex' + '>/dev/null')




for company in set_companies:
	company_interviews = []
	for elem in dict_interviews['interviews']:
		if(elem['companyId'] == company):
			company_interviews.append(elem)

	company_interviews = sorted(company_interviews, key=lambda elem: elem['timeSlot']['id']) 
	string = ''
	for index,elem in enumerate(company_interviews):
		if(index%2==0):
			string += '\\IS{' + elem['timeSlot']['timeRange'] + '}' + '{' + elem['candidateId'] + '}' + '{' + elem['interviewRoom']['name'] + '}' + '{' + str(index + 1) + '}' + '\n'
		else:
			string += '\\CT{' + elem['timeSlot']['timeRange'] + '}' + '{' + elem['candidateId'] + '}' + '{' + elem['interviewRoom']['name'] + '}' + '{' + str(index + 1) + '}' + '\n'

	
	file = open('Latex_template.tex','r')
	text = file.read()
	text = text.replace('$Interviews$', string)
	text = text.replace('$Name$', company)
	file.close()

	company = str(company).replace(' ','_')
	with open('Companies/' + company + '_schedule.tex', 'w') as output:
		output.write(text)
		output.close()

	
	print(company)
	os.system('pdflatex -interaction=batchmode -output-directory=Companies/ Companies/'+ company + '_schedule.tex' + '>/dev/null')
	
os.system('find Users/ -type f ! -iname "*.pdf" -delete')
os.system('find Companies/ -type f ! -iname "*.pdf" -delete')



