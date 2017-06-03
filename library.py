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
import os



# Inicjalizacyjne połączenie się do bazy na użytkownika dbadmin // Mało 'compliance' - hasło dostępne
# Można pomyśleć, w jaki sposób to obejść / można np. ograniczył użytkownikowi DBADMIN uprawnienia (jedna z metod)

polaczenie = cx_Oracle.connect('dbadmin/password@192.168.1.103/library')

def interface():

    intro = (
        "Witamy w Bibliotece " + "Libary_SQL . Zdefiniuj co chcesz zrobić ? \n")

    # Definicja listy funkcji
    lista_funkcji = [
        "1. : Sprawdź dostępność interesującej książki",
        "2. : Sprawdź ilość egzemplarzy książki",
        "3. : Dodaj nową książkę",
        "4. : Usuń książkę"]

    print (intro)

    # Gwiazdki mające na celu poprawienie wyglądu aplikacji
    for gwiazdka in range(30):
        print "*",

    print ('\n')

    for opcja in lista_funkcji:
        print (opcja)

    pytanie_1 = raw_input(" \nWybierz z listy funkcję  ")
    # Dodatkowo liczymy tablice od zera stąd wymagana odjecie -1

    pytanie_1 = int(pytanie_1)
    #
    # Konieczna konwersja "pytanie_1" przy wywołaniu w następnym etapi zawartości z tablicy na int
    print ("Wybrano opcję :    " + lista_funkcji[int(pytanie_1) - 1])

    # Wywoływanie funkcji zależnie od decyzji podjętej przez użytkownika aplikacji
    if (pytanie_1 == 1):
        sprawdz_ksiazke()

    if (pytanie_1 == 2):
        zlicz_egzemplarze()


    if (pytanie_1 == 3):
        # usun_ksiazke()
        pass

def sprawdz_ksiazke():

    while True:
        podaj_ISBN = raw_input("Podaj proszę poprawny ISBN Książki (np.9788311130487)  : \n")
        dlugosc=len(podaj_ISBN)


        # Warunek który jest potrzebny przy sprawdzeniu formatu ISBN, musimy uniknąc sytacji kiedy użytkownik wpisze
        # inny format ISBN ( ISBN składa się z 13 cyfr ; do 31 grudnia 2006 r. zawierał 10 cyfr)
        if (podaj_ISBN.isdigit() and (dlugosc == (13 or 10))):
            print ("Wprowadzono poprawny ISBN książki")
            # W tym miejscu wychodzimy z pętli while i kontynujemy aplikację
            break
        else:
            print ("\nWprowadzono zły format ISBN książki")

            # W tym miejscu wracamy na początek pętli While
            continue

    # Gwiazdki mające na celu poprawienie wyglądu aplikacji
    for gwiazdka in range(30):
        print "*",

    # Nowa linia w celu poprawienia wyglądu aplikacji
    print ("\n")

    cur = polaczenie.cursor()

    # Konstrukcja zapytania
    zapytanie_ISBN = "select TITLE from DBADMIN.BOOKS where id_books =" + podaj_ISBN

    # Wywołanie w CMDL SQL zapytania
    cur.execute(zapytanie_ISBN)

    odpowiedz_bazy = cur.fetchmany(numRows=3)

    try:
        # Wyciecie tytułu
        tytul_znaleziony=str(odpowiedz_bazy[0][0])
    except:
        IndexError
        pass

    if len(odpowiedz_bazy) == 0 :
        print "Nie znaleziono książki o " + podaj_ISBN + " w bazie danych"

        # Efekt czystego ekranu i uruchom interfejs bazy
        # print("\n\n\n")
        interface()

    else :
        print ("Znaleziono książkę o ISBN : " + podaj_ISBN + " w bazie danych.  "
                                                             "Tytuł szukanej książki to : "+tytul_znaleziony)

    # print odpowiedz_bazy

    pytanie__2 = raw_input((" \nCzy chcesz sprawdzić liczbę dostępnych egzemplarzy książki "+ tytul_znaleziony + " ? [tak / nie]\n")                               )

    if pytanie__2 == "tak" :
        zlicz_egzemplarze()


    if pytanie__2== "nie" :
        interface()
        # Efekt czystego ekranu i uruchom interfejs bazy

        # print("\n\n\n\n\n\n\n")
        # aplikacja.interface()

def zlicz_egzemplarze():
    polaczenie = cx_Oracle.connect('dbadmin/password@192.168.1.103/library')
    cur = polaczenie.cursor()
    podaj_tytul = raw_input("Podaj proszę tytuł interesującej Książki (np. Steve Jobs)  : \n")

    # Skonstruowanie zapytania
    zapytanie_egzemplarz = "SELECT COUNT(1) FROM DBADMIN.BOOKS B, DBADMIN.COPY C  WHERE B.ID_BOOKS = C.ID_BOOKS  " \
                           "AND TITLE ='%s'" % (podaj_tytul)



    # Wywołanie w CMDL SQL zapytania
    cur.execute(zapytanie_egzemplarz)

    odpowiedz_bazy = cur.fetchmany(numRows=3)
    print ("Znaleziono w bazie danych " + str(odpowiedz_bazy[0][0])+ " egzemplarze książki " + podaj_tytul)





# interface()
zlicz_egzemplarze()

