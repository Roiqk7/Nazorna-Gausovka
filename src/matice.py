"""
Datum: 30. 11. 2024

Třída Matice reprezentuje matici pro potřeby řešení soustav lineárních rovnic pomocí Gaussovy eliminace.
"""

from tisk import vytiskniCislo, zformatujCislo
from math import isclose
import numpy as np

PRAH_ROVNOSTI_FLOATU = 1e-10

class Matice:
# Základní metody
        def __init__(self, m, n, hodnoty = None, pravaStrana=None):
                """
                Konstruktor třídy Matice

                @param m: počet řádků
                @param n: počet sloupců
                @param hodnoty: hodnoty matice (uložené jako 1D seznam čísel po řádcích)
                @param pravaStrana: pravá strana soustavy rovnic (jako matice)
                """
                self.m = m
                self.n = n
                if hodnoty is not None:
                        self.hodnoty = np.array(hodnoty, dtype=np.float64).reshape(m, n)
                else:
                        self.hodnoty = np.zeros((m, n), dtype=np.float64)
                self.pravaStrana = pravaStrana

        def jsouIndexyOk(self, i, j):
                """
                Zjistí, zda jsou indexy i, j v rozměrech matice

                @param i: řádek
                @param j: sloupec

                @return: True, pokud jsou indexy ok, jinak False
                """
                return 0 <= i < self.m and 0 <= j < self.n

        def prvek(self, i, j):
                """
                Vrátí prvek matice na pozici i, j

                @param i: řádek
                @param j: sloupec

                @return: prvek matice na pozici i, j
                """
                if not self.jsouIndexyOk(i, j):
                        raise IndexError("Indexy mimo rozsah")
                return self.hodnoty[i, j]

        def nastavPrvek(self, i, j, hodnota):
                """
                Nastaví prvek matice na pozici i, j

                @param i: řádek
                @param j: sloupec
                @param hodnota: nová hodnota prvku
                """
                if not self.jsouIndexyOk(i, j):
                        raise IndexError("Indexy mimo rozsah")
                self.hodnoty[i, j] = hodnota

        def kopije(self):
                """
                Vytvoří kopii matice

                @return: kopie matice
                """
                rozsirena = self.pravaStrana.kopije() if self.pravaStrana != None else None
                return Matice(self.m, self.n, self.hodnoty.copy(), rozsirena)

        def __eq__(self, matice):
                if not isinstance(matice, Matice):
                        return False
                if self.m != matice.m or self.n != matice.n:
                        return False
                for i in range(self.m):
                        for j in range(self.n):
                                if not isclose(self.prvek(i, j), matice.prvek(i, j), abs_tol=PRAH_ROVNOSTI_FLOATU):
                                        return False
                return True

# Elementární řádkové úpravy
        def vynasobitRadek(self, i, skalar):
                """
                Vynásobí i-tý řádek matice skalárem

                @param i: řádek
                @param skalar: číslo, kterým se vynásobí řádek
                """
                if not self.jsouIndexyOk(i, 0):
                        raise IndexError("Index mimo rozsah")
                self.hodnoty[i, :] *= skalar
                if self.pravaStrana != None:
                        self.pravaStrana.vynasobitRadek(i, skalar)

        def pricistNasobekRadku(self, i, j, skalar):
                """
                Přičte k i-tému řádku alfa násobek j-tého

                @param i: řádek, ke kterému se přičítá
                @param j: řádek, který se násobí
                @param skalar: násobek j-tého řádku
                """
                if not self.jsouIndexyOk(i, 0) or not self.jsouIndexyOk(j, 0):
                        raise IndexError("Index mimo rozsah")
                self.hodnoty[i, :] += skalar * self.hodnoty[j, :]
                if self.pravaStrana != None:
                        self.pravaStrana.pricistNasobekRadku(i, j, skalar)

        def prohoditRadky(self, i, j):
                """
                Prohodí i-tý a j-tý řádek

                @param i: první řádek
                @param j: druhý řádek
                """
                if not self.jsouIndexyOk(i, 0) or not self.jsouIndexyOk(j, 0):
                        raise IndexError("Index mimo rozsah")
                self.hodnoty[[i, j], :] = self.hodnoty[[j, i], :]
                if self.pravaStrana != None:
                        self.pravaStrana.prohoditRadky(i, j)

# Reprezentace matice
        def vypis(self, zvyraznitIndexy = [], zvyraznitPravaStrana = []):
                """
                Vypíše matici na obrazovku

                @param zvyraznitIndexy: indexy, které se mají zvýraznit
                @param zvyraznitPravaStrana: indexy pravé strany, které se mají zvýraznit
                """
                # Zjistíme maximální délku čísla
                maximalniTloustkaSloupce = [0] * self.n
                for j in range(self.n):
                        maximalniTloustkaSloupce[j] = max([len(zformatujCislo(self.prvek(i, j))) for i in range(self.m)])
                if self.pravaStrana != None:
                        pravaMaximalniTloustkaSloupce = [0] * self.pravaStrana.n
                        for j in range(self.pravaStrana.n):
                                pravaMaximalniTloustkaSloupce[j] = max([len(zformatujCislo(self.pravaStrana.prvek(i, j))) for i in range(self.m)])
                # Vytiskneme matici
                for i in range(self.m):
                        for j in range(self.n):
                                zvyraznit = (i, j) in zvyraznitIndexy
                                vytiskniCislo(self.prvek(i, j), end=" ", doplnitDo=maximalniTloustkaSloupce[j], barevne=zvyraznit)
                        if self.pravaStrana != None:
                                print("|", end=" ")
                                for j in range(self.pravaStrana.n):
                                        zvyraznit = (i, j) in zvyraznitPravaStrana
                                        vytiskniCislo(self.pravaStrana.prvek(i, j), end=" ", doplnitDo=pravaMaximalniTloustkaSloupce[j], barevne=zvyraznit)
                        print()
                print()