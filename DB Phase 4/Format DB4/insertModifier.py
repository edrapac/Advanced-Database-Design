orders = []
import fileinput
import random
with fileinput.FileInput('--Populate CUSTOMER.txt',inplace=True,backup='.bak') as file:
	for i in range(0,529):
		if i < 10:
			orders.append(str('0000')+str(i))
		if i> 10 and i <100:
			orders.append(str('000')+str(i))
		if i > 100:
			orders.append(str('00')+str(i))
	

	for line in file:
		if len(orders) > 3:
			ranges = []
			for x in range(3):
				green = random.randint(0,(len(orders)-1))
				ranges.append(orders[green])
				orders.pop(green)
		print(line.replace("NULL",(str(ranges[0])+","+str(ranges[1])+","+str(ranges[2]))),end='')