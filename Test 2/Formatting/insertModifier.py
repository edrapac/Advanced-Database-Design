import random
import fileinput
import random
phonefile = open('Phones.txt','r')
phones = []
for lines in phonefile:
	phones.append(lines)

with fileinput.FileInput('O_Customer.txt',inplace=True,backup='.bak') as file:
	
	

	for line in file:
		phone1 = phones[random.randrange(0,129)]
		phone2 = phones[random.randrange(0,129)]
		print(line.replace("PHONES()",("PHONES("+"\'"+str(phone1)+"\'"+','+"\'"+str(phone2)+"\'"+")")),end='')