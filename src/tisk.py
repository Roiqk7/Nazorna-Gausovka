""" 
Datum: 14. 12. 2024

Funkce pro tisk do konzole
"""

from colorama import init, Fore, Style
from enum import IntEnum
from fractions import Fraction
from math import isclose

init(autoreset=True) # Nemusíme volat reset po každém výpisu

# Konstanty pro barvy
CERVERNA = Fore.RED
ZELENA = Fore.GREEN
FIALOVA = Fore.MAGENTA
ZLUTA = Fore.YELLOW
SEDA = Fore.LIGHTBLACK_EX
RESET = Style.RESET_ALL
# Konstanty pro formátování čísel
PRAH_ROVNOSTI_FLOATU = 1e-10
MAXIMALNI_JMENOVATEL = 1000
# Konstanty pro míru tisku
class MiraTisku(IntEnum):
        ZADNA = 0 # Žádné výpisy
        NIZKA = 1 # Pouze informativní výpisy
        VYSOKA = 2 # Všechny výpisy (postup výpočtu, jednotlivé kroky, ...)
        MEGA = 3 # Všechny výpisy + základy teorie

def zformatujZnamenko(cislo, znamenko = False):
        """
        Zformátuje znaménko pro výpis do konzole

        @param cislo: číslo
        @param znamenko: zda se má vypsat znaménko speciálně

        @return: zformátované znaménko
        """
        if znamenko:
                znamenko = "+ " if cislo >= 0 else "- "
        else:
                znamenko = "" if cislo >= 0 else "-"
        return znamenko

def zformatujCislo(cislo, znamenko = False, end = "\n", doplnitDo = 0):
        """
        Zformátuje číslo pro výpis do konzole

        @param cislo: číslo
        @param znamenko: zda se má vypsat znaménko speciálně
        @param end: konec řádku
        @param doplnitDo: minimální délka výstupu (doplněno mezerami)

        @return: zformátované číslo
        """
        if isclose(cislo, int(cislo), abs_tol=PRAH_ROVNOSTI_FLOATU):
                cislo = int(cislo)
        else:
                cislo = Fraction(cislo).limit_denominator(MAXIMALNI_JMENOVATEL)

        zformatovaneZnamenko = zformatujZnamenko(cislo, znamenko)
        zformatovaneCislo = f"{zformatovaneZnamenko}{abs(cislo)}"

        if doplnitDo > 0:
                zformatovaneCislo = zformatovaneCislo.rjust(doplnitDo)

        return f"{zformatovaneCislo}{end}"

def vytiskniCislo(cislo, znamenko = False, end = "\n", doplnitDo = 0, barevne = False):
        """
        Vytiskne zformátované číslo do konzole

        @param cislo: číslo
        @param znamenko: zda se má vypsat znaménko speciálně
        @param end: konec řádku
        @param doplnitDo: minimální délka výstupu (doplněno mezerami)
        """
        zformatovaneCislo = zformatujCislo(cislo, znamenko, end, doplnitDo)
        if barevne:
                print(f"{ZLUTA}{zformatovaneCislo}", end="")
        else:
                print(zformatovaneCislo, end="")

def vytiskniPromennou(hodnota, index, promenychCelkem, znamenko = False, end = "\n"):
        """
        Vytiskne proměnnou do konzole

        @param hodnota: hodnota proměnné
        @param index: index proměnné
        @param promenychCelkem: celkový počet proměnných
        @param end: konec řádku
        """
        promene = ['x', 'y', 'z'] if promenychCelkem <= 3 else [f"x{i + 1}" for i in range(promenychCelkem)]
        promena = promene[index]
        # Pokud je koeficient 1 nebo -1, vypíšeme pouze proměnnou (pro hezčí výstup)
        if isclose(abs(hodnota), 1, abs_tol=PRAH_ROVNOSTI_FLOATU):
                zformatovaneZnamenko = zformatujZnamenko(hodnota, znamenko)
                print(f"{zformatovaneZnamenko}", end="")
        else:
                vytiskniCislo(hodnota, znamenko, end = "")
        print(f"{FIALOVA}{promena}", end=end)

def vytiskniChybu(text):
        """
        Vytiskne chybu do konzole

        @param text: text chyby
        """
        print(f"{CERVERNA}[CHYBA]: {text}")

def vytiskniUspech(text):
        """
        Vytiskne úspěch do konzole

        @param text: text úspěchu
        """
        print(f"{ZELENA}{text}")

def vytiskniAssertChybu(skutecna, ocekavana, identifikator):
        """
        Vytiskne chybu z assertu

        @param skutecna: skutečná hodnota
        @param ocekavana: očekávaná hodnota
        @param identifikator: identifikátor testu
        """
        vytiskniChybu(f"Test {identifikator} selhal")
        print(f"Skutečná hodnota:\n\t{skutecna}")
        print(f"Očekávaná hodnota:\n\t{ocekavana}")

def vytiskni(text, miraTisku = MiraTisku.NIZKA, hladinaTisku = MiraTisku.NIZKA):
        """
        Vytiskne text podle míry tisku

        @param text: text
        @param miraTisku: míra tisku programu
        @param hladinaTisku: minimální hladina tisku pro výpis
        """
        if miraTisku >= hladinaTisku:
                print(text)

def vytiskniMatici(text, matice, miraTisku = MiraTisku.NIZKA, hladinaTisku = MiraTisku.NIZKA, end = "\n"):
        """
        Vytiskne matici do konzole s textem před ní

        @param text: text před maticí
        @param matice: matice
        @param miraTisku: míra tisku programu
        @param hladinaTisku: minimální hladina tisku pro výpis

        @note Funguje i pro vektory
        """
        if miraTisku >= hladinaTisku:
                if text != "":
                        print(text, end=end)
                matice.vypis()

def vytiskniRozdilMatic(text, puvodni, nova, miraTisku = MiraTisku.NIZKA, hladinaTisku = MiraTisku.NIZKA):
        """
        Vytiskne rozdíl dvou matic do konzole s barevným zvýrazněním

        @param matice: první matice
        @param matice2: druhá matice
        @param miraTisku: míra tisku programu
        @param hladinaTisku: minimální hladina tisku pro výpis
        """
        if miraTisku >= hladinaTisku:
                rozdilneIndexy = []
                pravaRozdilneIndexy = []
                for i in range(puvodni.m):
                        for j in range(puvodni.n):
                                if not isclose(puvodni.prvek(i, j), nova.prvek(i, j), abs_tol=PRAH_ROVNOSTI_FLOATU):
                                        rozdilneIndexy.append((i, j))
                if puvodni.pravaStrana != None:
                        for i in range(puvodni.pravaStrana.m):
                                for j in range(puvodni.pravaStrana.n):
                                        if not isclose(puvodni.pravaStrana.prvek(i, j), nova.pravaStrana.prvek(i, j), abs_tol=PRAH_ROVNOSTI_FLOATU):
                                                pravaRozdilneIndexy.append((i, j))
                if text != "":
                        print(text)
                nova.vypis(rozdilneIndexy, pravaRozdilneIndexy)

def pockej(miraTisku = MiraTisku.NIZKA, hladinaTisku = MiraTisku.NIZKA):
        """
        Počká na stisk klávesy
        """
        if miraTisku >= hladinaTisku:
                input(f"{SEDA}Stiskněte enter pro pokračování...")
                print()

def zformatujCisloProLatexVypis(cislo, znamenko = False, promenychCelkem = 0, promenna = -1):
        """
        Zformátuje číslo pro výpis do latexu

        @param cislo: číslo
        @param znamenko: zda se má vypsat znaménko speciálně
        @param promenychCelkem: celkový počet proměnných
        @param promenna: index proměnné

        @return: formátované číslo pro výpis do latexu
        """
        if isclose(cislo, int(cislo), abs_tol=PRAH_ROVNOSTI_FLOATU):
                cislo = int(cislo)
        if isinstance(cislo, float):
                cislo = Fraction(cislo).limit_denominator(MAXIMALNI_JMENOVATEL)
        zformatovaneZnamenko = zformatujZnamenko(cislo, znamenko)
        cislo = abs(cislo)

        # Proměnná
        if promenna != -1:
                promene = ['x', 'y', 'z'] if promenychCelkem <= 3 else [f"x_{i + 1}" for i in range(promenychCelkem)]
                promena = promene[promenna]
                if cislo == 1:
                        return f"{zformatovaneZnamenko}{promena}"
                elif isinstance(cislo, Fraction):
                        return f"{zformatovaneZnamenko}\\frac{{{cislo.numerator}}}{{{cislo.denominator}}}{promena}"
                else:
                        return f"{zformatovaneZnamenko}{cislo}{promena}"
        # Absolutní člen
        else:
                return f"{zformatovaneZnamenko}{cislo}"