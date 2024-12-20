""" 
Datum: 15. 12. 2024

Teorie řešení soustav lineárních rovnic pomocí matic

Pozn.: Látka je čerpána ze skript pana prof. Milana Hladíka.
"""

from gauss import GaussovaEliminace, zpetnaSubstituce
from gaussPomocne import prevedReseniNaSeznam
from matice import Matice
from vektor import Vektor
from test import porovnejSeznamy
from tisk import pockej, MiraTisku, vytiskniChybu, FIALOVA, ZLUTA, RESET

def teorieMain():
        """
        Základní úvod do teorie řešení soustav lineárních rovnic
        """
        print("Čísla v [N] závorkách reprezentují reference ze skript pana prof. Milana Hladíka.")
        print("<=== Úvod ===> [2]")
        print("Celý úvod zabere ~15 minut. Tempo si ale určuješ sám.")
        pockej()
        v1 = Vektor(4, [3, 2, 1, 39], 2)
        v2 = Vektor(4, [2, 3, 1, 34], 2)
        v3 = Vektor(4, [1, 2, 3, 26], 2)
        print("Mějme soustavu lineárních rovnic: [2.1]")
        v1.vypis()
        v2.vypis()
        v3.vypis()
        xyz = f"{FIALOVA}x{RESET}, {FIALOVA}y{RESET} a {FIALOVA}z{RESET}"
        print(f"Tato soustava má tři rovnice a tři neznámé: {xyz}.")
        print(f"Cílem je najít hodnoty {xyz}, které splňují všechny tři rovnice najednou.")
        pockej()
        print("Soustavu lze zapsat pomocí matice následovně:")
        prava = Matice(3, 1, [39, 34, 26])
        matice = Matice(3, 3, [3, 2, 1, 2, 3, 1, 1, 2, 3], prava)
        matice.vypis()
        print("Do matice tedy zapisujeme koeficienty před neznámými a pravé strany rovnic.")
        print("Jednotlivé rovnice pak zapisujeme jako řádky matice.")
        print("Lze si snadno uvědomit, že počet řádků matice odpovídá počtu rovnic.")
        print("Počet sloupců matice pak odpovídá počtu neznámých.")
        pockej()
        print("Jenže proč se vlastně snažíme řešit soustavu lineárních rovnic pomocí matic?")
        print("\t> 1. Soustavy je lehčí řešit pomocí matic (i když to chce trochu cviku ;-]).")
        print("\t> 2. Matice, jak v průběhu semestru uvidíš, mají spoustu šikovných vlastností...")
        pockej()
        print("Jak se tedy řeší soustavy lineárních rovnic pomocí matic?")
        print("\t> 1. Převedeme soustavu lineárních rovnic na matici.")
        print("\t> 2. Převedeme matici do odstupňovaného tvaru pomocí Gaussovy eliminace. [2.2]")
        print("\t> 3. Z odstupňované matice získáme řešení soustavy pomocí zpětné substituce.")
        pockej()
        print("1. Jak převést soustavu lineárních rovnic na matici?")
        print("\t> To už víme. Jedná se o zápis koeficientů před neznámými do matice rozšířené o pravé strany rovnic.")
        pockej()
        print("2. Jak převést matici do odstupňovaného tvaru pomocí Gaussovy eliminace? [2.2]")
        print("Zde si nejdříve musíme představit základní elementární operace:")
        print("\t> Vynásobení řádku nenulovou konstantou")
        print("\t> Přičtení násobku jednoho řádku k jinému řádku")
        print("\t> Prohození dvou řádků")
        print("Možná to zní složitě, ale ve skutečnosti je to velmi jednoduché.")
        pockej()
        print("Co znamená, že jsou operace elementární?")
        print(f"\t> Nemění množinu řešení soustavy. Tedy pokud vektor {ZLUTA}Ř{RESET} byl řešením soustavy před operací, bude jím i po operaci.")
        print("Jsou ale skutečně elementární operace 'elementární'?")
        print("\t> Ne. Prohození dvou řádků lze simulovat předchozími dvěma operacemi. Jak? (cvičení pro čtenáře ;-])")
        pockej()
        print("Jak tedy postupovat při Gaussově eliminaci?")
        print("Zde je například postup pro vyřešení soustavy uvedené výše:")
        matice.vypis()
        GaussovaEliminace(matice, MiraTisku.MEGA)
        print("Výsledná matice je v odstupňovaném tvaru. Tedy 0 tvoří 'schody' v matici. Definice [2.12]")
        print("Ovšem to nevypadá jako řešení soustavy... Je tam toho stále hodně.")
        print("Navíc pokud jsi se pokusil(a) soustavu vyřešit, mohl(a) si dojít k jinému výsledku.")
        pockej()
        print("Nejdříve si musíme uvědomit, že postup uvedený výše je tvz. Gaussova eliminace.")
        print("Důležité tvrzení o Gaussově eliminaci je, že není jednoznačná.")
        print("Tedy může existovat více odstupňovaných tvarů matice pro stejnou soustavu.")
        print("Ovšem pozice pivotů v matici jsou jednoznačné.")
        print("Pivoty jsou nenulové prvky, které tvoří 'schody' v matici.")
        pockej()
        print("Sloupcům s pivoty se říká bázické sloupce.")
        print("Sloupcům bez pivotů se říká nebázické sloupce.")
        print("Tyto pojmy začnou dávat smysl až ke konci semestru. Je ale dobré je už teď znát.")
        pockej()
        print("3. Jak z odstupňované matice získat řešení soustavy?")
        print("Zde se využívá zpětné substituce. Tedy postupné dosazování do rovnic.")
        print("Zde je postup pro dořešení soustavy uvedené výše:")
        matice.vypis()
        reseni = prevedReseniNaSeznam(zpetnaSubstituce(matice, MiraTisku.MEGA))
        if not porovnejSeznamy(reseni, [37/4, 17/4, 11/4]):
                vytiskniChybu(f"Chybné řešení soustavy. Očekáváno: [37/4, 17/4, 11/4], obdrženo: {reseni}")
                vytiskniChybu("TOTO SE NEMĚLO STÁT! Nedůvěřuj výpočtům. Teorie je ovšem správná...")
        print()
        print("Řešení soustavy jednoznačné už ale je.")
        print(f"Tedy {FIALOVA}x{RESET} = 37/4, {FIALOVA}y{RESET} = 17/4, {FIALOVA}z{RESET} = 11/4.")
        print("Pokud ti to nevyšlo, zkus se podívat na výpočet výše. Matice jsou náchylné na numerické chyby.")
        pockej()
        print("Pokud jsi došel až sem, gratuluji! Toto je tvůj první krok k pochopení lineární algebry.")
        print("Typy pro studium lineární algebry:")
        print("\t> Obstarej si skripta pana prof. Milana Hladíka z knihovny. Zabere to jen pár minut.")
        print("\t> Před každou přednáškou si přečti odpovídající kapitolu ze skript alespoň jednou.")
        print("\t> Počítej si příklady a dávej pozor na cvičeních. (osobně jsem měl Pangráce a velmi ho doporučuji)")
        print("\t> Více najdeš na matfyz wiki a od kolegů. :-)")

if __name__ == "__main__":
        teorieMain()