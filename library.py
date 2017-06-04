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


class App():
    def __init__(self):

        # Inicjalizacyjne połączenie się do bazy na użytkownika dbadmin // Mało 'compliance' - hasło dostępne
        # Można pomyśleć, w jaki sposób to obejść / można np. ograniczył użytkownikowi DBADMIN uprawnienia (jedna z metod)
        self.polaczenie = cx_Oracle.connect('dbadmin/password@192.168.1.103/library')

    def interface(self):
        # Ustawienia triggera do funkcji 2
        self.trigger = 0
        intro = (
            "Witamy w Bibliotece " + "Libary_SQL . Zdefiniuj co chcesz zrobić ? \n")

        # Definicja listy funkcji
        lista_funkcji = [
            "1. : Sprawdź dostępność interesującej książki",
            "2. : Sprawdź ilość egzemplarzy książki",
            "3. : Dodaj nową książkę",
            "4. : Usuń książkę"]

        for gwiazdka in range(30):
            print "*",
        print ('\n')
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
            self.sprawdz_ksiazke()

        if (pytanie_1 == 2):
            self.zlicz_egzemplarze()

        if (pytanie_1 == 3):
            # dodaj_ksiazke()
            pass

        if (pytanie_1 == 4):
            self.usun_ksiazke()
            pass

    def sprawdz_ksiazke(self):

        while True:
            self.podaj_ISBN = raw_input("Podaj proszę poprawny ISBN Książki (np.9788311130487)  : \n")
            dlugosc = len(self.podaj_ISBN)

            # Warunek który jest potrzebny przy sprawdzeniu formatu ISBN, musimy uniknąc sytacji kiedy użytkownik wpisze
            # inny format ISBN ( ISBN składa się z 13 cyfr ; do 31 grudnia 2006 r. zawierał 10 cyfr)
            if (self.podaj_ISBN.isdigit() and (dlugosc == 13 or 10)):
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

        cur = self.polaczenie.cursor()

        # Konstrukcja zapytania
        zapytanie_ISBN = "select TITLE from DBADMIN.BOOKS where id_books =" + self.podaj_ISBN

        # Wywołanie w CMDL SQL zapytania
        cur.execute(zapytanie_ISBN)

        odpowiedz_bazy = cur.fetchmany(numRows=3)

        try:
            # Wyciecie tytułu z zapytania
            self.tytul_znaleziony = str(odpowiedz_bazy[0][0])
        except:
            IndexError
            pass

        if len(odpowiedz_bazy) == 0:
            print "Nie znaleziono książki o " + self.podaj_ISBN + " w bazie danych"

            # Efekt czystego ekranu i uruchom interfejs bazy
            # print("\n\n\n")
            return False
            self.zakoncz()

        else:
            print ("Znaleziono książkę o ISBN : " + self.podaj_ISBN + " w bazie danych.  "
                                                                 "Tytuł szukanej książki to : '" + self.tytul_znaleziony) + "'"
            return True

        # print odpowiedz_bazy

        pytanie__2 = raw_input((
                               " \nCzy chcesz sprawdzić liczbę dostępnych egzemplarzy książki : '" + self.tytul_znaleziony + "' ? [tak / nie]\n"))

        if pytanie__2 == "tak":
            # Zmienna trigger majaca na celu pominiecie w nastepnej metodzie zapytania o podanie nazwy szukanego tytułu
            self.trigger = 1
            self.zlicz_egzemplarze()

        if pytanie__2 == "nie":
            self.interface()
            # Efekt czystego ekranu i uruchom interfejs bazy

            # print("\n\n\n\n\n\n\n")
            # aplikacja.interface()

    def zlicz_egzemplarze(self):
        # polaczenie = cx_Oracle.connect('dbadmin/password@192.168.1.103/library')
        cur = self.polaczenie.cursor()

        if self.trigger == 0:
            self.podaj_tytul = raw_input("Podaj proszę tytuł interesującej Książki (np. Steve Jobs)  : \n")


        else:
            self.podaj_tytul = self.tytul_znaleziony
        # Skonstruowanie zapytania
        zapytanie_egzemplarz = ("SELECT COUNT(1) FROM DBADMIN.BOOKS B, DBADMIN.COPY C  WHERE B.ID_BOOKS = C.ID_BOOKS  " \
                                "AND TITLE ='%s'" % self.podaj_tytul)

        # Wywołanie w CMDL SQL zapytania
        cur.execute(zapytanie_egzemplarz)

        odpowiedz_bazy = cur.fetchmany(numRows=3)
        print ("Znaleziono w bazie danych " + str(
            odpowiedz_bazy[0][0]) + " egzemplarze książki :" + "'" + self.podaj_tytul + "'")

        self.zakoncz()

    def dodaj_ksiazke(self):
        self.pytanie_4 = raw_input("")

        slownik = {"ISBN": int, "Tytul": None, "Imie autora": None, "Nazwisko autora": None, "Wydawnictwo": None,
                   "Miejsce wydania": None, "Ilosc stron": None, "Indeks egzemplarza": None}

        kolejnosc = ["ISBN", "Tytul", "Imie autora", "Nazwisko autora", "Wydawnictwo", "Miejsce wydania", "Ilosc stron",
                     "Indeks egzemplarza"]

        self.polaczenie = cx_Oracle.connect('dbadmin/password@192.168.1.103/library')

        for i, j in enumerate(kolejnosc):
            # j = raw_input("Podaj dla %r " %(j))
            slownik[j] = raw_input("Podaj dla %r " % (j))

        # zapytanie = "INSERT INTO DBADMIN.BOOKS(ID_BOOKS, TITLE, NAME, LASTNAME, PUBLISHING_HOUS, YEAR, PLACE_OF_PUBLISH, " \
        #             "NUMBER_OF_PUBLIC, PAGE,ID_CATHEGORY) VALUES("+slownik[kolejnosc[0]]","+
        #             slownik[kolejnosc[0]]"," slownik[kolejnosc[2]], slownik[kolejnosc[3]],
        #        slownik[kolejnosc[4]], slownik[kolejnosc[5]], slownik[kolejnosc[6]], slownik[kolejnosc[7]],
        #        slownik[kolejnosc[8]]);
        print slownik



    def usun_ksiazke(self):

        if self.sprawdz_ksiazke() == False :

        if self.sprawdz_ksiazke() == True :
            pytanie_usun = raw_input("Czy na pewno chcesz usunąć książkę o ISBN : "+self.podaj_ISBN +"? [tak]/[nie]""\n")

            if pytanie_usun == "tak" :
                # Zapytanie o dropowanie wiersza
            else :
                self.zakoncz()

    def zakoncz(self):

        self.pytanie_3 = raw_input("Co robisz dalej : zakończ aplikacje / powrót  ?        [zakończ]/[powrót]""\n")
        if self.pytanie_3 == "zakończ":
            exit

        if self.pytanie_3 == "powrót":
            self.interface()


aplikacja = App()
aplikacja.interface()
# interface()


