import random
import copy

#Program do zarządzania flotą samolotów, rejetrowania rezerwacji i sprawdzania stanu samolotów.

class Samolot:

    __slots__ = ['nazwa', 'siedzenia', 'ilosc_rezerwacji']

    def zamien_litere_na_liczbe(self, litera):
        return ord(litera.upper()) - ord('A')

    def zamien_liczbe_na_litere(self, liczba):
        return chr(liczba + ord('A'))

    def __init__(self, nazwa, liczba_rzedow, ile_miejsc_w_rzedzie):
        self.nazwa = nazwa
        self.siedzenia = [[0] * ile_miejsc_w_rzedzie for i in range(liczba_rzedow)]
        self.ilosc_rezerwacji = 0

    def __repr__(self):
        przedstawienie = f'{self.nazwa}\n  '

        for i in range(len(self.siedzenia[0])):
            przedstawienie += f'{self.zamien_liczbe_na_litere(i)}'
        przedstawienie += '\n'

        for i in range(len(self.siedzenia)):
            przedstawienie += f'{i + 1} '
            for j in range(len(self.siedzenia[0])):
                przedstawienie += f'{self.siedzenia[i][j]}'
            przedstawienie += '\n'
        return przedstawienie

    def rezerwuj_miejsce_losowo(self):

        assert self.ilosc_rezerwacji < len(self.siedzenia)*len(self.siedzenia[0]), "Brak wolnych miejsc"

        nr_rzedu = random.randint(1, len(self.siedzenia))
        nr_kolumny = random.randint(1, len(self.siedzenia[0]))
        rzad = f'{nr_rzedu}'
        kolumna = f'{self.zamien_liczbe_na_litere(nr_kolumny-1)}'
        miejsce = rzad + kolumna

        while self.sprawdz_czy_miejsce_wolne(miejsce) == False:
            nr_rzedu = random.randint(1, len(self.siedzenia))
            nr_kolumny = random.randint(1, len(self.siedzenia[0]))
            rzad = f'{nr_rzedu}'
            kolumna = f'{self.zamien_liczbe_na_litere(nr_kolumny - 1)}'
            miejsce = rzad + kolumna

        self.ilosc_rezerwacji += 1
        self.siedzenia[nr_rzedu - 1][nr_kolumny - 1] = 1
        return miejsce

    def sprawdz_czy_miejsce_wolne(self, miejsce):
        nr_rzedu = int(miejsce[0]) - 1
        nr_kolumny = self.zamien_litere_na_liczbe(miejsce[1])
        if self.siedzenia[nr_rzedu][nr_kolumny] == 1:
            return False
        else:
            return True

    def ile_zajetych_miejsc(self):
        return self.ilosc_rezerwacji

    @staticmethod
    def skopiuj_samolot_z_rezerwacjami(samolot, nowa_nazwa):
        kopia = copy.deepcopy(samolot)
        kopia.nazwa = nowa_nazwa
        return kopia

    #Mnożenie polega na utworzeniu samolotu, którego ma rezerwacje tylko w miejscach, gdzie oba samoloty mają rezerwacje
    def __mul__(self, other):
        assert len(self.siedzenia) == len(other.siedzenia)
        assert len(self.siedzenia[0]) == len(other.siedzenia[0])

        wynik = Samolot.skopiuj_samolot_z_rezerwacjami(self, self.nazwa)
        for i in range(len(self.siedzenia)):
            for j in range(len(self.siedzenia[0])):
                if other.siedzenia[i][j] == 0:
                    wynik.siedzenia[i][j] = 0
        return wynik

def main():
    random.seed(1234)

    airbus = Samolot('Embraer 175', 6, 4)
    print(airbus)

    #Sprawdzenie działania rezerwowania miejsc
    zarezerwowane_miejsca = [None] * 10
    for i in range(len(zarezerwowane_miejsca)):
        zarezerwowane_miejsca[i] = airbus.rezerwuj_miejsce_losowo()
        print(f'Zarezerwowano miejsce: {zarezerwowane_miejsca[i]}')

    assert not airbus.sprawdz_czy_miejsce_wolne(zarezerwowane_miejsca[0]), 'Miejsce dopiero zostało zarezerwowane'
    for przykladowe_siedzenie in ['1D', '2C', '3B']:
        if not przykladowe_siedzenie in zarezerwowane_miejsca:
            assert airbus.sprawdz_czy_miejsce_wolne(
                przykladowe_siedzenie), f'Miejsce {przykladowe_siedzenie} jeszcze nie zostało zarezerwowane'

    print()
    print(airbus)

    #Sprawdzenie kopiowania samolotu
    airbus_kopia = Samolot.skopiuj_samolot_z_rezerwacjami(airbus, 'Embraer 175+')
    print(airbus_kopia)

    #Sprawdzenie, czy zmiany w kopii wpływają na oryginał
    dodatkowe_rezerwacje = [None] * 5
    for i in range(len(dodatkowe_rezerwacje)):
        miejsce_w_kopii = airbus_kopia.rezerwuj_miejsce_losowo()
        dodatkowe_rezerwacje[i] = miejsce_w_kopii
        assert not airbus_kopia.sprawdz_czy_miejsce_wolne(
            miejsce_w_kopii), f'Miejsce {miejsce_w_kopii} w kopi samolotu dopiero zostało zarezerwowane'
        assert airbus.sprawdz_czy_miejsce_wolne(
            miejsce_w_kopii), f'Miejsce {miejsce_w_kopii} w orginalnym samolocie jest  wolne'
    print(f'Ilość zajetych miejsc w oryginalnym samolocie to: {airbus.ile_zajetych_miejsc()}')
    print(f'Ilość zajetych miejsc w samolocie to: {airbus_kopia.ile_zajetych_miejsc()}')
    print(airbus)
    print(airbus_kopia)

    #Sprawdzenie mnożenie samolotów
    samolot_z_wspolnymi = airbus_kopia * airbus
    print(samolot_z_wspolnymi)

    #Sprawdzenie, czy zmiany w iloczynie mają wpływ na składniki
    nowa_rezerwacja = airbus_kopia.rezerwuj_miejsce_losowo()
    print(f'Zarezerwowano miejsce {nowa_rezerwacja}')
    assert samolot_z_wspolnymi.sprawdz_czy_miejsce_wolne(nowa_rezerwacja), "Nie powinno się zmienić miejsce w samolocie z wspólnymi"

if __name__ == '__main__':
  main()

