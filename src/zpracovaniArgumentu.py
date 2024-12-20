"""
Datum: 15. 12. 2024

Definuje funkce pro zpracování argumentů z konzole
"""

from gauss import reseniSoustavy
from matice import Matice
from parsovani import zpracujMatlabMatici, latexNaMatici, reseniNaLatex
from ukazka import mainUkazka
from teorie import teorieMain
from test import testuj
from tisk import MiraTisku, vytiskniChybu, vytiskniUspech
import argparse
import os
import numpy as np

# Vytvoření parseru pro argumenty v konzoli
parser = argparse.ArgumentParser()

# Definice argumentů
parser.add_argument("--vstup", help="Soustava lineárních rovnic ve formátu matlabu")
parser.add_argument("--nacti", help="Název souboru se vstupními daty")
parser.add_argument("--uloz", help="Název souboru pro uložení výstupních dat")
parser.add_argument("--tisk", help="Míra tisku (0-3), 0 je žádné, 3 je vše", type=int)
parser.add_argument("--ukazka", help="Předvede program na ukázkovém vstupu", action='store_true')
parser.add_argument("--teorie", help="Zobrazí teorii", action='store_true')
parser.add_argument("--test", help="Spustí testy", action='store_true')
parser.add_argument("--pomoc", help="Zobrazí nápovědu", action='store_true')

def zpracujArgumenty(argumenty):
        """
        Zpracuje argumenty z konzole

        @param argumenty: argumenty z konzole
        """
        reseni = None
        if argumenty.tisk:
                if argumenty.tisk == 0:
                        tisk = MiraTisku.ZADNA
                elif argumenty.tisk == 1:
                        tisk = MiraTisku.NIZKA
                elif argumenty.tisk == 2:
                        tisk = MiraTisku.VYSOKA
                elif argumenty.tisk == 3:
                        tisk = MiraTisku.MEGA
        else:
                tisk = MiraTisku.NIZKA
        try:
                # Nelze načíst vstup ze souboru a z konzole zároveň
                if argumenty.vstup:
                        matice = zpracujMatlabMatici(argumenty.vstup)
                        reseni = reseniSoustavy(matice, tisk)
                elif argumenty.nacti:
                        matice = nactiMaticiZeSouboru(argumenty.nacti)
                        reseni = reseniSoustavy(matice, tisk)
        except:
                vytiskniChybu("Nepodařilo se načíst vstupní data. Zkontrolujte formát vstupu. (viz --pomoc)")
                raise ValueError("Nepodařilo se načíst vstupní data. Zkontrolujte formát vstupu. (viz --pomoc)")
        if argumenty.uloz:
                ulozReseniDoSouboru(argumenty.uloz, reseni)
        if argumenty.test:
                testuj()
        if argumenty.ukazka:
                mainUkazka()
        if argumenty.teorie:
                teorieMain()
        if argumenty.pomoc:
                pomoc()

def nactiMaticiZeSouboru(soubor):
        """
        Načte matici ze souboru

        @param soubor: soubor se vstupními daty

        @return: matice
        """
        if not os.path.exists(soubor):
                vytiskniChybu(f"Nepodařilo se najít soubor {soubor} pro načtení vstupních dat.")
                soubor = "data/vstup.tex"
                print(f"Vstupní data budou načtena ze souboru {soubor}.")
        try:
                with open(soubor, "r") as f:
                        vstup = f.read()
                return latexNaMatici(vstup)
        except Exception as e:
                vytiskniChybu(f"Nepodařilo se načíst vstupní data ze souboru {soubor}. Zkontrolujte formát. (viz --pomoc)")
                raise ValueError(f"Nepodařilo se načíst vstupní data ze souboru {soubor}: {e}")

def ulozReseniDoSouboru(soubor, reseni):
        """
        Uloží řešení do souboru v latexu

        @param soubor: soubor pro uložení výstupních dat
        @param reseni: řešení
        """
        if not os.path.exists(soubor):
                vytiskniChybu(f"Nepodařilo se najít soubor {soubor} pro uložení výstupních dat.")
                soubor = "data/vystup.tex"
                print(f"Výstupní data budou uložena do souboru {soubor}.")
        try:
                with open(soubor, "w") as f:
                        f.write(reseniNaLatex(reseni))
                vytiskniUspech(f"Výstupní data byla úspěšně uložena do souboru {soubor}.")
        except Exception as e:
                vytiskniChybu(f"Nepodařilo se uložit výstupní data do souboru {soubor}: {e}")
                raise e

def pomoc():
        """
        Vytiskne nápovědu
        """
        print("<========================================================= N Á P O V Ě D A =========================================================>")
        print("Program na vizualizaci řešení soustavy lineárních rovnic pomocí Gaussovy eliminace.")
        print("Použití:")
        print("\t> python3 src/main.py [--vstup VSTUP] [--nacti NACTI] [--uloz ULOZ] [--tisk TISK] [--ukazka] [--teorie] [--test] [--pomoc]")
        print("Parametry:")
        print("\t> --vstup: Soustava lineárních rovnic (*)")
        print("\t> --nacti: Název souboru se vstupními daty v LaTeXu (*)")
        print("\t> --uloz: Název souboru pro uložení výstupních dat (*)")
        print("\t> --tisk: Míra tisku (0-3), 0 je žádné, 3 je vše")
        print("\t> --ukazka: Předvede program na ukázkovém vstupu")
        print("\t> --teorie: Zobrazí stručný úvod do teorie lineární algebry")
        print("\t> --test: Spustí testy")
        print("\t> --pomoc: Zobrazí tuto nápovědu")
        print("(*) Pro formát vstupu a výstupu viz níže sekci 'Formát vstupu a výstupu'")
        print("Příklady spuštění:")
        print("\t> python3 src/main.py --vstup=\"[1 3 5; 2 4 6; 7 8 10]\" --tisk=3")
        print("\t> python3 src/main.py --nacti=\"soubor.txt\" --uloz=\"vystup.txt\" --tisk=2")
        print("\t> python3 src/main.py --teorie")
        print("Formát vstupu a výstupu:")
        print("\t> parametr --vstup očekává matici ve formátu matlabu např.: [1 3 5; 2 4 6; 7 8 10]")
        print("\t> parametr --nacti očekává soubor s maticí ve formátu LaTeXu")
        print("\t> parametr --uloz uloží výstup do souboru ve formátu LaTeXu")
        print("Závislosti:")
        print("\t> Program je napsán v Pythonu 3.13.0")
        print("\t> Použité externí knihovny: colorama, numpy")
        print("Doporučení:")
        print("\t> Pokud o lineární algebře nevíte nic, zobrazte si teorii (--teorie).")
        print("\t> Pokud chcete vidět, jak program funguje, spusťte ukázku (--ukazka).")
        print("\t> Doporučuji začít s maximálním tiskem (--tisk=3) a s nabývajícím pochopením snižovat míru tisku.")
        print("\t> Pokud chcete zkontrolovat, zda program funguje správně, spusťte testy (--test).")
        print("Feedback:")
        print("\t> Pokud jste našli chybu, nebo máte nápad na vylepšení, vytvořte issue na GitHubu.")
        print("\t> GitHub: https://github.com/Roiqk7/nazorna-gausovka")
        print("\t> GitLab: https://gitlab.mff.cuni.cz/sevecep/nazorna-gausovka")
        print("Více informací naleznete v README.md")