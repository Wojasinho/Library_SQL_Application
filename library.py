# -*- coding: utf-8 -*-
"""
Aplikacja ma na celu pokazania aspektu praktycznego zaimplementowanej bazy danych dla biblioteki. 
Wykorzystuje ona integralna bibliotekę cx_Oracle z Pythonem 2.7.5 

Dostępne funkcje ( pobieranie danych, wpisywanie nowych rekordów do bazy etc. zostały opisane w dokumentacji
Bazy dla Biblioteki 


Wykonała: Anna Meller
e-mail: 219263@student.pwr.edu.pl
"""

import cx_Oracle

# Defined connection
con = cx_Oracle.connect('dbadmin/password@192.168.1.103/library')

cur = con.cursor()

# a = raw_input("Co chcesz zrobić")
cur.execute('select * from dbadmin.books')

res = cur.fetchmany(numRows=3)
print res[1]

cur.close()
