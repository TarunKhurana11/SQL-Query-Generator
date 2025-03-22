import sqlite3

##connect to sqlite
connection=sqlite3.connect("student.db")

## create a cursor object to insert record,create table,retrieve
cursor=connection.cursor()

##create the table
table_info="""
Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT);

"""

cursor.execute(table_info)

##Insert some more records

cursor.execute('''Insert Into STUDENT values('Tarun','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Anuj','Data Science','B',85)''')
cursor.execute('''Insert Into STUDENT values('Navdeep','Data Science','A',100)''')
cursor.execute('''Insert Into STUDENT values('Harry','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Piyush','DEVOPS','B',35)''')

##Display all the records
print("The Inserted records are")

data=cursor.execute('''Select * From STUDENT''')

for row in data:
    print(row)

##Close the connection

connection.commit()
connection.close 