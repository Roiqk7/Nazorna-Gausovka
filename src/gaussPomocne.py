""" 
Datum: 14. 12. 2024

Pomocné funkce pro výpočet soustavy rovnic
"""

from matice import Matice
from vektor import Vektor
from tisk import vytiskniMatici, MiraTisku, vytiskni, pockej
from math import isclose, inf

PRAH_ROVNOSTI_INTU = 1e-3

def jeHezkyPivot(pivot):
        """
        Zjistí, zda je pivot hezký

        @param pivot: pivot

        @return: True, pokud je pivot hezký, jinak False
        """
        if isclose(pivot, 0, abs_tol=PRAH_ROVNOSTI_INTU):
                return False
        # Nejhezčí pivot je 1 nebo -1
        if isclose(abs(pivot), 1, abs_tol=PRAH_ROVNOSTI_INTU):
                return True
        # Další hezké pivots jsou malá celá čísla
        if isclose(pivot, int(pivot), abs_tol=PRAH_ROVNOSTI_INTU) and abs(pivot) < 5:
                return True
        return False

def ziskejVhodnehoPivota(matice, i, j):
        """
        Získá řádek vhodného pivota pro jednu iteraci Gaussovy eliminaci

        @param matice: matice soustavy rovnic
        @param i: index řádku
        @param j: index sloupce

        @return: index řádku pivota
        """
        # Najdeme nejmenšího pěkného pivota
        minPivot = inf
        radekPivota = None
        for k in range(i, matice.m):
                kandidat = matice.prvek(k, j)
                # Kontrola, zda splňuje podmínky
                if jeHezkyPivot(kandidat):
                        if abs(kandidat) < abs(minPivot):
                                minPivot = kandidat
                                radekPivota = k
        # Pokud nenajdeme vhodného pivota, najdeme první nenulový prvek
        if radekPivota is None:
                for k in range(i, matice.m):
                        if matice.prvek(k, j) != 0:
                                radekPivota = k
                                break

        return radekPivota

def ziskejPivoty(odstupnovanaMatice, hodnost):
        """
        Získá pivoty a jejich pozice z matice

        @param matice: matice soustavy rovnic
        @param hodnost: hodnost matice

        @return: seznam pivotů
        @return: seznam pozic pivotů

        @note: Předpokládá se, že matice je v odstupňovaném tvaru
        """
        pivoty = []
        pozicePivotu = []
        for i in range(hodnost):
                for j in range(odstupnovanaMatice.n):
                        # Najdeme první nenulový prvek v řádku (pivot)
                        if odstupnovanaMatice.prvek(i, j) != 0:
                                pivoty.append(odstupnovanaMatice.prvek(i, j))
                                pozicePivotu.append(j)
                                break
        return pivoty, pozicePivotu

def vytvorRovnici(odstupnovanaMatice, i, pozicePivotu):
        """
        Vytvoří rovnici z i-tého řádku odstupňované matice

        @param odstupnovanaMatice: odstupňovaná matice
        @param i: index řádku
        @param pozicePivotu: pozice pivotů

        @return: vektor rovnice
        """
        # Vytvoříme vektor rovnice
        rovnice = [0] * odstupnovanaMatice.n
        absolutniClen = odstupnovanaMatice.pravaStrana.prvek(i, 0)
        for j in range(pozicePivotu[i], odstupnovanaMatice.n):
                rovnice[j] = odstupnovanaMatice.prvek(i, j)
        rovnice += [absolutniClen]
        return Vektor(odstupnovanaMatice.n + 1, rovnice, odstupnovanaMatice.n - 1)

def prevedRovniciNaDruhouStranu(vektor, pozicePivotu):
        """
        Převede rovnici na druhou stranu

        @param vektor: vektor rovnice
        @param pozicePivotu: pozice pivotu
        """
        for j in range(vektor.m - 1):
                if j != pozicePivotu:
                        vektor.prevedClenNaDruhouStranu(j)
        vektor.indexRovnitka = pozicePivotu

def provedZpetnouSubstituci(vektor, reseni, vyresenychPromennych, hodnost, pozicePivotu, miraTisku = MiraTisku.ZADNA):
        """
        Provede zpětnou substituci

        @param vektor: vektor rovnice
        @param reseni: řešení proměnných
        @param vyresenychPromennych: počet vyřešených proměnných
        @param hodnost: hodnost matice
        @param pozicePivotu: pozice pivotů
        @param miraTisku: míra tisku programu

        @return: vektor rovnice po zpětné substituci
        """
        pockej(miraTisku, MiraTisku.VYSOKA)
        vytiskni("Zpětná substituce:", miraTisku, MiraTisku.VYSOKA)
        # Najdeme přítomné proměnné a jejich koeficienty
        # Pozn.: Jedeme odzadu až po vyřešené proměnné
        for i in range(hodnost - 1, hodnost - vyresenychPromennych - 1, -1):
                promena = reseni[i]
                koeficient = vektor.prvek(pozicePivotu[i])
                promena *= koeficient
                # Hezký výpis
                vytiskniMatici("Proměnou:", promena, miraTisku, MiraTisku.VYSOKA, end=" ")
                vytiskniMatici("Dosadíme do rovnice:", vektor, miraTisku, MiraTisku.VYSOKA, end=" ")
                # Dosadíme proměnnou do rovnice
                vektor += promena
                vektor.hodnoty[pozicePivotu[i]] = 0
                # Hezký výpis
                vytiskniMatici("Po dosazení:", vektor, miraTisku, MiraTisku.VYSOKA)
        return vektor

def prevedReseniNaSeznam(reseni):
        """
        Převede řešení na seznam

        @param reseni: vektor řešení

        @return: řešení jako seznam
        """
        if reseni is None:
                return None
        reseniSeznam = []
        for vektor in reseni:
                if isinstance(vektor, Vektor):
                        reseniSeznam.append(vektor.hodnoty[-1])
                else: # int
                        reseniSeznam.append(vektor)
        return reseniSeznam