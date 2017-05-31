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

class Library() :

    def __init__(self):
        self.con = cx_Oracle.connect('dbadmin/password@192.168.1.103/library')

    def interface(self):

        intro = (
            "Witamy w Bibliotece " + "Libary_SQL . Zdefiniuj co chcesz zrobić ? \n")

        self.lista_funkcji = [
            "\n1. : Sprawdź dostępność interesującej książki",
            "2. : Dodaj nową książke",
            "3. : Usuń książkę"]

        print intro

        for gwiazdka in range(30):
            print "*",

        for opcja in self.lista_funkcji :
            print opcja

        wybor = raw_input(" \nWybierz z listy funkcję  ")

        #Konieczna konwersja przy wywołaniu zawartości z tablicy na int
        print ("Wybrano opcję :    " +  self.lista_funkcji[int(wybor)-1])


# Stworzenie objektu klasy Library
aplikacja = Library()
aplikacja.interface()



#     res = cur.fetchmany(numRows=3)
#     print res[1]
#
#
# cur.close()
# cur = con.cursor()
# # a = raw_input("Co chcesz zrobić")
# cur.execute('select * from dbadmin.books')
