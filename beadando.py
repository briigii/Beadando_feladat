from abc import ABC, abstractmethod
from datetime import date, datetime


# Szoba absztrakt osztály
class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam


# EgyagyasSzoba osztály
class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=5000, szobaszam=szobaszam)


# KetagyasSzoba osztály
class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=8000, szobaszam=szobaszam)


# Szalloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def hozzaad_szoba(self, szoba):
        self.szobak.append(szoba)


# Foglalas osztály
class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum


# Szálloda és foglalások kezelése
class SzallodaKezelo:
    def __init__(self):
        self.szallodak = []

    def hozzaad_szalloda(self, szalloda):
        self.szallodak.append(szalloda)

    def foglalas(self, szalloda_nev, szoba_szam, datum):
        szalloda = self._get_szalloda(szalloda_nev)
        if not szalloda:
            return "Szálloda nem található."
        if not self._validal_datum(datum):
            return "Érvénytelen dátum."

        szoba = self._get_szoba(szalloda, szoba_szam)
        if not szoba:
            return "Szoba nem található."

        if self._foglalt_e(szalloda, szoba, datum):
            return "A szoba már foglalt ezen a napon."

        foglalas = Foglalas(szoba, datum)
        szalloda.foglalasok.append(foglalas)
        return f"Foglalás sikeres. Ár: {szoba.ar} Ft"

    def lemondas(self, szalloda_nev, szoba_szam, datum):
        szalloda = self._get_szalloda(szalloda_nev)
        if not szalloda:
            return "Szálloda nem található."

        foglalas = self._get_foglalas(szalloda, szoba_szam, datum)
        if not foglalas:
            return "Foglalás nem található."

        szalloda.foglalasok.remove(foglalas)
        return "Foglalás lemondva."

    def listaz_foglalasok(self, szalloda_nev):
        szalloda = self._get_szalloda(szalloda_nev)
        if not szalloda:
            return "Szálloda nem található."

        foglalas_lista = []
        for foglalas in szalloda.foglalasok:
            foglalas_lista.append(f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")

        return foglalas_lista if foglalas_lista else "Nincsenek foglalások."

    def _get_szalloda(self, szalloda_nev):
        for szalloda in self.szallodak:
            if szalloda.nev == szalloda_nev:
                return szalloda
        return None

    def _get_szoba(self, szalloda, szoba_szam):
        for szoba in szalloda.szobak:
            if szoba.szobaszam == szoba_szam:
                return szoba
        return None

    def _validal_datum(self, datum):
        try:
            foglalas_datum = datetime.strptime(datum, "%Y-%m-%d").date()
            return foglalas_datum > date.today()
        except ValueError:
            return False

    def _foglalt_e(self, szalloda, szoba, datum):
        for foglalas in szalloda.foglalasok:
            if foglalas.szoba == szoba and foglalas.datum == datum:
                return True
        return False

    def _get_foglalas(self, szalloda, szoba_szam, datum):
        for foglalas in szalloda.foglalasok:
            if foglalas.szoba.szobaszam == szoba_szam and foglalas.datum == datum:
                return foglalas
        return None


# Példányosítás és feltöltés
szalloda_kezelo = SzallodaKezelo()

szalloda = Szalloda("Budapest Hotel")
szalloda_kezelo.hozzaad_szalloda(szalloda)

szoba1 = EgyagyasSzoba(101)
szoba2 = EgyagyasSzoba(102)
szoba3 = KetagyasSzoba(201)

szalloda.hozzaad_szoba(szoba1)
szalloda.hozzaad_szoba(szoba2)
szalloda.hozzaad_szoba(szoba3)

szalloda_kezelo.foglalas("Budapest Hotel", 101, "2024-06-01")
szalloda_kezelo.foglalas("Budapest Hotel", 102, "2024-06-01")
szalloda_kezelo.foglalas("Budapest Hotel", 201, "2024-06-01")
szalloda_kezelo.foglalas("Budapest Hotel", 101, "2024-06-02")
szalloda_kezelo.foglalas("Budapest Hotel", 102, "2024-06-02")


# Felhasználói interfész
def felhasznaloi_interfesz():
    while True:
        print("\nVálasszon műveletet:")
        print("1. Foglalás létrehozása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")

        valasztas = input("Adja meg a művelet számát: ")

        if valasztas == "1":
            szalloda_nev = input("Adja meg a szálloda nevét: ")
            szoba_szam = int(input("Adja meg a szoba számát: "))
            datum = input("Adja meg a dátumot (YYYY-MM-DD): ")
            eredmeny = szalloda_kezelo.foglalas(szalloda_nev, szoba_szam, datum)
            print(eredmeny)

        elif valasztas == "2":
            szalloda_nev = input("Adja meg a szálloda nevét: ")
            szoba_szam = int(input("Adja meg a szoba számát: "))
            datum = input("Adja meg a dátumot (YYYY-MM-DD): ")
            eredmeny = szalloda_kezelo.lemondas(szalloda_nev, szoba_szam, datum)
            print(eredmeny)

        elif valasztas == "3":
            szalloda_nev = input("Adja meg a szálloda nevét: ")
            foglalasok = szalloda_kezelo.listaz_foglalasok(szalloda_nev)
            if isinstance(foglalasok, list):
                for foglalas in foglalasok:
                    print(foglalas)
            else:
                print(foglalasok)

        elif valasztas == "4":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás, próbálja újra.")


# Futtatás
felhasznaloi_interfesz()
