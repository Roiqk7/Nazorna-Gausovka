"""
Datum: 8. 12. 2024

Třída Vektor reprezentuje vektor pro potřeby řešení soustav lineárních rovnic pomocí Gaussovy eliminace.
"""

from matice import Matice
import numpy as np
from math import isclose
from tisk import *

# Konstanta pro toleranci rozdílu při porovnávání floatů
PRAH_ROVNOSTI_FLOATU = 1e-10
MAXIMALNI_JMENOVATEL = 1000

class Vektor(Matice):
# Základní metody
        def __init__(self, n, hodnoty = None, indexRovnitka = None):
                """
                Konstruktor třídy Vektor

                @param n: počet prvků vektoru
                @param hodnoty: hodnoty vektoru
                """
                super().__init__(n, 1, hodnoty)
                self.indexRovnitka = indexRovnitka

        def jsouIndexyOk(self, i, j = 0):
                return 0 <= i < self.m and j == 0

        def prvek(self, i):
                """
                Vrátí prvek vektoru na pozici i

                @param i: index prvku
                """
                return super().prvek(i, 0)

        def nastavPrvek(self, i, hodnota):
                return super().nastavPrvek(i, 0, hodnota)
# Operace s vektory
        def __add__(self, vektor):
                """
                Sčítání vektorů

                @param vektor: vektor, se kterým chceme sečíst
                """
                # Aby fungovalo sčítání s číslem (např. pokud je nulové řešení)
                if isinstance(vektor, (int, float)):
                        if vektor != 0:
                                for i in range(self.m):
                                        self.hodnoty[i] += vektor
                elif isinstance(vektor, Vektor):
                        if self.m != vektor.m:
                                raise ValueError("Vektory mají různé rozměry")
                else: # Jiný typ
                        raise ValueError("Nelze sčítat vektor s jiným typem")
                return Vektor(self.m, self.hodnoty + vektor.hodnoty, self.indexRovnitka)

        def __mul__(self, skalar):
                """
                Násobení vektoru skalárem

                @param skalar: skalární hodnota
                """
                return Vektor(self.m, self.hodnoty * skalar, self.indexRovnitka)

        def __truediv__(self, skalar):
                """
                Dělení vektoru skalárem

                @param skalar: skalární hodnota
                """
                return Vektor(self.m, self.hodnoty / skalar, self.indexRovnitka)

        def __eq__(self, vektor):
                """
                Porovnání vektorů

                @param vektor: vektor, se kterým chceme porovnat
                """
                if not isinstance(vektor, Vektor):
                        return False
                if self.m != vektor.m:
                        return False
                for i in range(self.m):
                        if not isclose(self.prvek(i), vektor.prvek(i), abs_tol=PRAH_ROVNOSTI_FLOATU):
                                return False
                return True
# Manipulace s prvky vektoru
        def prevedClenNaDruhouStranu(self, i):
                """
                Převede prvek na druhou stranu rovnice

                @param i: index prvku
                """
                self.hodnoty[i] *= -1
# Reprezentace vektoru
        def vypis(self):
                """
                Vypíše vektor jako rovnici
                """
                vypsano = False
                for i in range(self.m):
                        prvek = self.prvek(i)
                        # Pokud je prvek nenulový nebo je absolutní člen, vypíšeme ho
                        if not isclose(prvek, 0, abs_tol=PRAH_ROVNOSTI_FLOATU) or i == self.m - 1:
                                if i == self.m - 1: # Absolutní člen
                                        vytiskniCislo(prvek, vypsano, end = " ")
                                else: # Proměnná
                                        vytiskniPromennou(prvek, i, self.m - 1, vypsano, end = " ")
                                vypsano = True
                        if i == self.indexRovnitka:
                                print("= ", end="")
                                vypsano = False
                print()

        def __str__(self):
                """
                Vrátí vektor jako řetězec
                """
                return str(self.hodnoty)