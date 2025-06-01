from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional


class Auto(ABC):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def info(self) -> str:
        pass


class Szemelyauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, utasok_szama: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.utasok_szama = utasok_szama

    def info(self) -> str:
        return f"Személyautó | Rendszám: {self.rendszam}, Típus: {self.tipus}, Díj: {self.berleti_dij} Ft/nap, Utasok: {self.utasok_szama}"


class Teherauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, teherbiras_kg: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras_kg = teherbiras_kg

    def info(self) -> str:
        return f"Teherautó | Rendszám: {self.rendszam}, Típus: {self.tipus}, Díj: {self.berleti_dij} Ft/nap, Teherbírás: {self.teherbiras_kg} kg"


class Berles:
    def __init__(self, auto: Auto, datum: date, berlo_neve: str):
        self.auto = auto
        self.datum = datum
        self.berlo_neve = berlo_neve

    def info(self) -> str:
        return f"{self.datum} | {self.auto.rendszam} | {self.auto.tipus} | Bérlő: {self.berlo_neve} | Ár: {self.auto.berleti_dij} Ft"


class Autokolcsonzo:
    def __init__(self, nev: str):
        self.nev = nev
        self.autok: List[Auto] = []
        self.berlesek: List[Berles] = []

    def auto_hozzaad(self, auto: Auto):
        self.autok.append(auto)

    def berles_hozzaad(self, berles: Berles):
        self.berlesek.append(berles)

    def auto_keres(self, rendszam: str) -> Optional[Auto]:
        for auto in self.autok:
            if auto.rendszam == rendszam:
                return auto
        return None

    def berles_keres(self, rendszam: str, datum: date) -> Optional[Berles]:
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                return berles
        return None

    def berles_torles(self, berles: Berles):
        if berles in self.berlesek:
            self.berlesek.remove(berles)

    def listaz_autok(self):
        print("\nAutók:")
        if not self.autok:
            print("Nincs ilyen autó a rendszerben.")
        for auto in self.autok:
            print(auto.info())

    def listaz_berlesek(self):
        print("\nBérlések:")
        if not self.berlesek:
            print("Nincs ilyen bérlés a rendszerben.")
        for berles in self.berlesek:
            print(berles.info())

def datum_bekeres():
    while True:
        datum_str = input("Add meg a bérlés napját (ÉÉÉÉ-HH-NN): ")
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
            if datum < date.today():
                print("A dátum nem lehet múltbeli!")
                continue
            return datum
        except ValueError:
            print("Hibás dátumformátum! Próbáld újra.")

def elerheto_auto(kolcsonzo: Autokolcsonzo, rendszam: str, datum: date) -> bool:
    for berles in kolcsonzo.berlesek:
        if berles.auto.rendszam == rendszam and berles.datum == datum:
            return False
    return True

def berles_felvitel(kolcsonzo: Autokolcsonzo):
    kolcsonzo.listaz_autok()
    rendszam = input("Melyik autót szeretnéd? (rendszám): ")
    auto = kolcsonzo.auto_keres(rendszam)
    if not auto:
        print("Nincs ilyen rendszámú autó!")
        return
    datum = datum_bekeres()
    if not elerheto_auto(kolcsonzo, rendszam, datum):
        print("Ez az autó már foglalt!")
        return
    berlo = input("Add meg a neved: ")
    berles = Berles(auto, datum, berlo)
    kolcsonzo.berles_hozzaad(berles)
    print(f"Sikeres bérlés! Ár: {auto.berleti_dij} Ft")

def berles_lemondas(kolcsonzo: Autokolcsonzo):
    rendszam = input("Melyik bérlést szeretnéd lemondani? (rendszám): ")
    datum = datum_bekeres()
    berles = kolcsonzo.berles_keres(rendszam, datum)
    if not berles:
        print("Nincs ilyen bérlés!")
        return
    kolcsonzo.berles_torles(berles)
    print("A bérlés törölve.")

def menu():
    print("\n*** Autókölcsönző ***")
    print("\n1. Autók listázása")
    print("2. Bérlések listázása")
    print("3. Autó bérlése")
    print("4. Bérlés lemondása")
    print("0. Kilépés")

def elore_feltoltott_kolcsonzo() -> Autokolcsonzo:
    kolcsonzo = Autokolcsonzo("Teszt Kölcsönző")
    auto1 = Szemelyauto("TXT-546", "Opel Corsa", 8000, 5)
    auto2 = Szemelyauto("DDK-789", "Mazda RX-7", 12000, 4)
    auto3 = Teherauto("FFH-456", "Ford Transit", 15990, 1500)
    kolcsonzo.auto_hozzaad(auto1)
    kolcsonzo.auto_hozzaad(auto2)
    kolcsonzo.auto_hozzaad(auto3)
    kolcsonzo.berles_hozzaad(Berles(auto1, date.today(), "Sunyi Sanya"))
    kolcsonzo.berles_hozzaad(Berles(auto2, date.today(), "Csoró Béla"))
    kolcsonzo.berles_hozzaad(Berles(auto3, date.today(), "Csülök Csaba"))
    try:
        holnap = date.today().replace(day=date.today().day + 1)
    except ValueError:
        if date.today().month == 12:
            holnap = date(date.today().year + 1, 1, 1)
        else:
            holnap = date(date.today().year, date.today().month + 1, 1)
    kolcsonzo.berles_hozzaad(Berles(auto1, holnap, "Szevasz Szilveszter"))
    return kolcsonzo

def main():
    kolcsonzo = elore_feltoltott_kolcsonzo()
    while True:
        menu()
        valasztas = input("\nVálasszon a menüből : ")
        if valasztas == "1":
            kolcsonzo.listaz_autok()
        elif valasztas == "2":
            kolcsonzo.listaz_berlesek()
        elif valasztas == "3":
            berles_felvitel(kolcsonzo)
        elif valasztas == "4":
            berles_lemondas(kolcsonzo)
        elif valasztas == "0":
            print("Kilépés...")
            break
        else:
            print("Ismeretlen művelet!")

if __name__ == "__main__":
    main()