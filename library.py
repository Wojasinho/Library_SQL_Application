# -*- coding: utf-8 -*-
"""
Aplikacja ma na celu pokazania aspektu praktycznego zaimplementowanej bazy danych dla biblioteki. 
Wykorzystuje ona integralna bibliotekę cx_Oracle z Pythonem 2.7.5 

Dostępne funkcje ( sprawdzenie książki, zliczenie egzemplarzy książki, dodanie nowej książki i egzemplarza, usunięcie 
książki z Bazy Danych Biblioteki). Funkcje opisane poniżej. 


Wykonała: Anna Meller
e-mail: 219263@student.pwr.edu.pl
"""

import cx_Oracle
import time


class App():

    def __init__(self):

        """Inicjalizacyjne połączenie się do bazy na użytkownika dbadmin // Mało 'compliance' - hasło dostępne
        # Można pomyśleć, w jaki sposób to obejść / można np. ograniczył użytkownikowi DBADMIN uprawnienia (jedna z metod)
        """
        self.polaczenie = cx_Oracle.connect('dbadmin/password@192.168.1.103/library')

    def interface(self):
        """
        Funkcja która definiuje interface, zarządza całą aplikacją , wykonuje poszczególne operacje zdefiniowane poniżej
         
        """

        # Ustawienia triggera do funkcji
        self.trigger = 0
        self.trigger_1 = 0
        self.trigger_2= 0

        intro = (
            "Witamy w Bibliotece " + "Libary_SQL . Zdefiniuj co chcesz zrobić ? \n")

        # Definicja listy funkcji
        lista_funkcji = [
            "1. : Sprawdź dostępność interesującej książki",
            "2. : Sprawdź ilość egzemplarzy książki",
            "3. : Dodaj nową książkę",
            "4. : Usuń książkę"]

    # Gwiazdki mające na celu poprawienie wyglądu aplikacji (czytelności aplikacji)
        for gwiazdka in range(30):
            print "*",

        print ('\n')
        print (intro)


        for gwiazdka in range(30):
            print "*",

        print ('\n')

        for opcja in lista_funkcji:
            print (opcja)

        pytanie_1 = raw_input(" \nWybierz z listy funkcję  ")

        # Konieczna konwersja "pytanie_1" przy wywołaniu w następnym etapi zawartości z tablicy na int
        pytanie_1 = int(pytanie_1)
        #
        print ("Wybrano opcję :    " + lista_funkcji[int(pytanie_1) - 1])

        # Wywoływanie funkcji zależnie od decyzji podjętej przez użytkownika aplikacji
        if (pytanie_1 == 1):
            self.sprawdz_ksiazke()

        if (pytanie_1 == 2):
            self.zlicz_egzemplarze()

        if (pytanie_1 == 3):
            self.dodaj_ksiazke()

        if (pytanie_1 == 4):
            self.usun_egzemplarz()


    def sprawdz_ksiazke(self):

        """
        Funkcja która sprawdza po numerze ISBN książki czy dana książka znajduję się w Bibliotece(DBADMIN.BOOKS). 
        Dodatkowo zwraca tytuł książki po wcześniejszym wprowadzeniu numeru ISBN. Jedną z dodatkowych opcji, 
        jest umożliwienie zliczenia wszystkich egzemplarzy książki w Bibliotece (wywołanie kolejnej funkcji 
        wewnątrz definicji). Wszystko zależne jest jakie życzenie, będzie miał użytkownik aplikacji
        """

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

        # Uniknięcie sytuacji gdzie w Bazie nie ma książki o podanym ISBN, wtedy nie możemy wywołać [0][0] elementu
        # z odpowiedzi_bazy - bo go poprostu nie ma.
        try:
            # Wyciecie tytułu z zapytania
            self.tytul_znaleziony = str(odpowiedz_bazy[0][0])
        except:
            IndexError
            pass

        if len(odpowiedz_bazy) == 0:
            print "Nie znaleziono książki o ISBN :  " + self.podaj_ISBN + " w bazie danych"
            if self.trigger_2==1:
                return True
            # Efekt czystego ekranu i uruchom interfejs bazy
            # print("\n\n\n")

            # self.zakoncz()

        else:
            if self.trigger_2 ==1:
                return False
            print ("Znaleziono książkę o ISBN : " + self.podaj_ISBN + " w bazie danych.  "
                                                                 "Tytuł szukanej książki to : '" + self.tytul_znaleziony) + "'"


        pytanie__2 = raw_input((
                               " \nCzy chcesz sprawdzić liczbę dostępnych egzemplarzy książki : '" + self.tytul_znaleziony
                               + "' ? [tak / nie]\n"))

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
        """
        Funkcja która sprawdza po tytule Książki czy istnieje w Bazie Danych podany rekord. Dodatkowo zwraca informację,
        w jakiej ilości dany tytuł występuje w Bazie Danych dla Biblioteki. 
        
        """
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

        if odpowiedz_bazy[0][0] !=0 :

            print ("Znaleziono w bazie danych " + str(odpowiedz_bazy[0][0]) + " egzemplarze książki :" + "'"
                   + self.podaj_tytul + "'")
            pytanie_4 = raw_input("Czy chcesz wyświetlić wszystkie egzemplarze książki ? [tak]/[nie]""\n")

            if pytanie_4 == "tak":

                # Konstukcja zapytania
                zapytanie_wyswietl = ("SELECT ID_COPY FROM DBADMIN.BOOKS B, DBADMIN.COPY C  WHERE B.ID_BOOKS = C.ID_BOOKS  " \
                                      "AND TITLE ='%s'" % self.podaj_tytul)

                # Nawiązanie połączenie + przekierowanie zapytania do SQLa
                cur = self.polaczenie.cursor()
                cur.execute(zapytanie_wyswietl)
                odpowiedz_bazy =cur.fetchall()

                print ("Egzemplarze książki : ")

                # Petla w pętli dlatego żeby unikąć sytuacji że printujemy ('numer indeksu') zamiast 'numer indeksu'
                # Estetyczne kwestie
                for item in odpowiedz_bazy :
                    for egzemplarz in item :
                        print egzemplarz,

                print('\n')
                if self.trigger_1 == 0:
                    self.zakoncz()


                return True

            if pytanie_4 == "nie":
                if self.trigger_1 == 0:
                    self.zakoncz()
                return True

        else :
            print ("Nie znaleziono w bazie danych żadnego egzemplarza")
        self.zakoncz()

    def dodaj_ksiazke(self):

        """
        Funkcja w której wywoływana jest już istniejąca metoda "sprawdz_ksiazke()" , jeśli okaże się że dana książka, 
        nie istnieje w Bazie Danych (sprawdza sie to po ISBNie książki), użytkwownik będzie mógł wprowadzić nowy rekord 
        do Bazy Danych według poprawnej kolejności : "Tytul", "Imie autora", "Nazwisko autora", "Wydawnictwo", 
        "Miejsce wydania", "Numer Wydania", "Ilosc stron","ID_kategorii", "Rok", "Indeks egzemplarza". 
        Następnie konsturowana jest komenda do Bazy Danych tłumaczona na język SQL i dodawany jest nowy rekord do tabeli
        DBADMIN.BOOKS oraz tworzony jest również egzemplarz książki do tabeli DBADMIN.COPY
        
        """
        # Zmiana triggera_2
        self.trigger_2 =1

        cur = self.polaczenie.cursor()

        # Ustawienie kolejności w jakiej użytkownik będzie konstruwał nowe zapytanie
        kolejnosc = ["Tytul", "Imie autora", "Nazwisko autora", "Wydawnictwo", "Miejsce wydania", "Numer Wydania", "Ilosc stron",
                    "ID_kategorii", "Rok", "Indeks egzemplarza"]

        # Pusta tabela na nowe dane wpisywane przez użytkownika
        dane_ksiazki=[]

        if self.sprawdz_ksiazke() == True :
            pytanie_potwierdzenie = raw_input("Czy chcesz napewno chcesz dodać nową książkę ? [tak]/[nie] \n")
            if pytanie_potwierdzenie == "tak" :
                for i, j in enumerate(kolejnosc):
                    j = raw_input("Wprowadź  %r " %(j))
                    dane_ksiazki.append(j)

                # Konstrukcja zapytania o dodanie nowej książki, ważnym momentem jest tutaj dodanie '' pomiędzy stringami
                zapytanie = ("INSERT INTO DBADMIN.BOOKS (ID_BOOKS,TITLE,NAME,LASTNAME, PUBLISHING_HOUS,PLACE_OF_PUBLISH,"
                             "NUMBER_OF_PUBLIC,PAGE,ID_CATHEGORY,YEAR) VALUES(" + str(self.podaj_ISBN) + ",'" +
                             dane_ksiazki[0] + "','" + dane_ksiazki[1] + "','" + dane_ksiazki[2] + "','" + dane_ksiazki[3]
                             + "','" + dane_ksiazki[4] + "'," + str(dane_ksiazki[5]) + "," + str(dane_ksiazki[6]) + ","
                             + str(dane_ksiazki[7]) + "," + dane_ksiazki[8] + ")" )

                cur.execute(zapytanie)
                cur.execute("commit")

                cur = self.polaczenie.cursor()
                zapytanie1 = ("INSERT INTO DBADMIN.COPY(ID_COPY,ID_BOOKS)   VALUES(" + str(dane_ksiazki[9]) + "," + str(self.podaj_ISBN) + ")")
                time.sleep(5)
                cur.execute(zapytanie1)
                cur.execute("commit")
                print ("Dodano nową książkę do Bazy Danych")
                self.zakoncz()
            else :
                self.zakoncz()
        else :
            print "Nie ma sensu dodawać tej samej książki do Bazy Biblioteki"
            self.zakoncz()



    def usun_egzemplarz(self):

        """
        Funkcja usun_egzemplarz() sprawdza czy dana książka znajduje się w Bazie Danych, jeśli tak zwraca ilość dostępnych
        egzemplarzy książki oraz indeksy egzemplarzy. Funkcja umożliwa użytkownikowi skasowanie dowolnego egzemplarza z
        tabeli DBADMIN.COPY z Bazy Danych
        
        """

        self.trigger_1=1
        if self.zlicz_egzemplarze() == True or False:
            podaj_indeks = raw_input("Wprowadź  numer indeksu egzemplarza który chcesz usunąć : ""\n")

            pytanie_potwierdzenie = raw_input("Czy napewno chcesz usunąć [egzemplarz : "+podaj_indeks+"] " +self.podaj_tytul +" "
                                              " z Bazy Danych? [tak]/[nie]""\n")

            if pytanie_potwierdzenie == "tak" :
                # Zapytanie o dropowanie wiersza
                cur = self.polaczenie.cursor()
                zapytanie = ("DELETE FROM DBADMIN.COPY WHERE ID_COPY =" + podaj_indeks)
                cur.execute(zapytanie)
                cur.execute("commit")
                # odpowiedz_bazy = cur.fetchmany(numRows=3)

                self.zakoncz()
            else :
                self.zakoncz()

        else :
            print ("Nie odnaleziono żadnego egzemplarza w Bazie Danych")

            self.zakoncz()


    def zakoncz(self):

        """
        Pomocna funkcja która daje użytkownikowi kontynuowanie bądź wyłączenie aplikacji po uprzednio wykonanej czyności
        """

        self.pytanie_3 = raw_input("Co robisz dalej : zakończ aplikacje / powrót  ?        [zakończ]/[powrót]""\n")
        if self.pytanie_3 == "zakończ":
            exit

        if self.pytanie_3 == "powrót":
            self.interface()


aplikacja = App()
aplikacja.interface()




