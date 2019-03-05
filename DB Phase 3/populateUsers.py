user_file = open('MOCK_DATA.csv','r')
script_file = open('Add_Users.txt','w+')
# readlines = file.readlines() readlines creates an array, each element is a line entry
for line in user_file.readlines():
	script_file.write(
	'DROP USER '+line+';'+'\n'
	'CREATE USER '+line+'\n'
  	'IDENTIFIED BY password\n'
  	'DEFAULT TABLESPACE USERS\n'
  	'TEMPORARY TABLESPACE TEMP\n'
  	'QUOTA 200M on USERS;'+'\n'

	'GRANT create session TO '+line+';'+'\n'
	'GRANT create table TO '+line+';'+'\n'
	'GRANT create view TO '+line+';'+'\n'
	'GRANT create any trigger TO '+line+';'+'\n'
	'GRANT create any procedure TO '+line+';'+'\n'
	'GRANT create sequence TO '+line+';'+'\n'
	'GRANT create synonym TO '+line+';'+'\n'
		)
user_file.close()
script_file.close()

# 	CREATE USER line
#   IDENTIFIED BY password
#   DEFAULT TABLESPACE USERS
#   TEMPORARY TABLESPACE TEMP
#   QUOTA 200M on USERS;

# GRANT create session TO line;
# GRANT create table TO line;
# GRANT create view TO line;
# GRANT create any trigger TO line;
# GRANT create any procedure TO line;
# GRANT create sequence TO line;
# GRANT create synonym TO line;