""" 
Datum: 30. 11. 2024

Funkce pro řešení soustavy rovnic
"""

from vektor import Vektor
import gaussPomocne as gp
from tisk import *

def GaussovaEliminace(matice, miraTisku = MiraTisku.ZADNA):
        """
        Převede matici do odstupňovaného tvaru pomocí Gaussovy eliminace

        @param matice: matice soustavy rovnic
        @param miraTisku: míra tisku programu

        @return matice v odstupňovaném tvaru

        @note: Algoritmus je inspirován vzoru ze skript pana prof. Milana Hladíka.
        """
        vytiskni("Převedeme matici do odstupňovaného tvaru...\n", miraTisku)
        vytiskni("K tomu využijeme Gaussovu eliminační metodu. Využívat budeme 3 elementárních operací:", miraTisku, MiraTisku.MEGA)
        vytiskni("\t> 1. Vynásobení řádku nenulovou reálnou konstantou.", miraTisku, MiraTisku.MEGA)
        vytiskni("\t> 2. Přičtení alpha-násobku řádku k jinému řádku.", miraTisku, MiraTisku.MEGA)
        vytiskni("\t> 3. Prohození dvou řádků.\n", miraTisku, MiraTisku.MEGA)
        puvodniMatice = None
        # 1. i = j = 0
        i = 0
        j = 0
        while True:
                if miraTisku >= MiraTisku.VYSOKA:
                        puvodniMatice = matice.kopije()
                # 2. Pokud A[i][j] = 0 pro všechna k >= i a l >= j, pak končíme (detekce nulové podmatice)
                k = i
                l = j
                saméNuly = True
                for k in range(i, matice.m):
                        for l in range(j, matice.n):
                                if matice.prvek(k, l) != 0:
                                        saméNuly = False
                                        break
                        if not saméNuly:
                                break
                if saméNuly:
                        return matice
                # 3. j = min{l; l >= j, A[k][l] != 0 pro nějaké k >= i} (přeskočíme nulové podsloupečky)
                k = i
                l = j
                while l < matice.n:
                        saméNuly = True
                        k = i
                        while k < matice.m:
                                if matice.prvek(k, l) != 0:
                                        saméNuly = False
                                        break
                                k += 1
                        if not saméNuly:
                                break
                        l += 1
                j = l
                # 4. Urči k takové, že A[k][j] != 0, k >= i a vyměň řádky i a k (na pozici pivota A[i][j] je nenulový prvek)
                # Tento krok upravíme tak, aby byla čísla hezčí (ale jedná se spíše o heuristiku, hezkost není zaručena)
                k = gp.ziskejVhodnehoPivota(matice, i, j)
                if k != i:
                        matice.prohoditRadky(i, k)
                        vytiskniRozdilMatic(f"Vyměníme řádky {i} a {k}:", puvodniMatice, matice, miraTisku, MiraTisku.VYSOKA)
                        pockej(miraTisku, MiraTisku.VYSOKA)
                # 4.5 Pokud je pivot ošklivý, vytvoříme z něj 1
                if not gp.jeHezkyPivot(matice.prvek(i, j)):
                        pivot = matice.prvek(i, j)
                        koeficientStr = zformatujCislo(1 / pivot, end="")
                        vytiskni(f"Pivot rovný +-1 je ideální. Snadno se s ním počítá. Proto si ze současného pivota {zformatujCislo(pivot, end="")} uděláme 1", miraTisku, MiraTisku.MEGA)
                        matice.vynasobitRadek(i, 1 / pivot)
                        vytiskniRozdilMatic(f"Vynásobíme řádek {i} {koeficientStr} tak, aby byl pivot 1:", puvodniMatice, matice, miraTisku, MiraTisku.VYSOKA)
                        pockej(miraTisku, MiraTisku.VYSOKA)
                # 5. Pro všechna k > i polož A[k] = A[k] - A[k][j]/A[i][j] * A[i] (2. elementární úprava)
                if i + 1 < matice.m:
                        vytiskni(f"Od řádků s indexem k > {i}, odečteme aplha-násobek řádku {i}. Alpha je dána podílem prvku A[k][{j}] s vybraným pivotem A[{i}][{j}]", miraTisku, MiraTisku.MEGA)
                        for k in range(i + 1, matice.m):
                                if matice.prvek(k, j) != 0:
                                        matice.pricistNasobekRadku(k, i, -matice.prvek(k, j) / matice.prvek(i, j))
                        vytiskniRozdilMatic(f"Po odečtení aplha-násobků řádku {i} dostáváme:", puvodniMatice, matice, miraTisku, MiraTisku.VYSOKA)
                        pockej(miraTisku, MiraTisku.VYSOKA)
                # 6. i = i + 1, j = j + 1 a pokračujeme od kroku 2
                i += 1
                j += 1

def rank(odstupnovanaMatice):
        """
        Spočítá hodnost matice v odstupňovaném tvaru

        @param odstupnovanaMatice: matice v odstupňovaném tvaru

        @return: hodnost matice
        """
        hodnost = 0
        for i in range(odstupnovanaMatice.m):
                for j in range(odstupnovanaMatice.n):
                        if odstupnovanaMatice.prvek(i, j) != 0:
                                hodnost += 1
                                break
        return hodnost

def FrobeniovaVeta(hodnostMatice, hodnostPraveStrany):
        """
        Určí řešitelnost soustavy rovnic podle Frobeniovy věty

        @param odstupnovanaMatice: matice v odstupňovaném tvaru

        @return: True, pokud je soustava řešitelná, jinak False
        """
        return hodnostMatice >= hodnostPraveStrany

def zpetnaSubstituce(odstupnovanaMatice, miraTisku = MiraTisku.ZADNA):
        """
        Provede zpětnou substituci a vrátí vektor řešení

        @param odstupnovanaMatice: matice v odstupňovaném tvaru
        @param miraTisku: míra tisku programu

        @return: vektor řešení

        @note Očekává řešitelnou matici v odstupňovaném tvaru

        Algoritmus:
        0. Spočítáme hodnost matice a zjistíme, zda je soustava řešitelná
        2. Najdeme pivoty
        3. Pro každého pivota od zadu:
                1) Vytvoříme rovnici pro i-tého pivota
                2) Převedeme vše kromě pivota na pravou stranu
                3) Substituujeme spočítané proměnné
                4) Vydělíme pivotem
                5) Přidáme rovnici do výsledného pole
        4. Vytiskneme řešení
        """
        # 0. Spočítáme hodnost matice a zjistíme, zda je soustava řešitelná
        hodnost = rank(odstupnovanaMatice)
        pravaHodnost = rank(odstupnovanaMatice.pravaStrana)
        if not FrobeniovaVeta(hodnost, pravaHodnost):
                vytiskni("Frobeniova věta říká, že pokud hodnost matice se nerovná hodnosti matice rozšířené o pravou stranu, pak soustava není řešitelná.", miraTisku, MiraTisku.MEGA)
                vytiskni(f"Po bližší inspekci si lze uvědomit, že to je náš případ. Hodnost matice {hodnost} se nerovná hodnosti matice rozšířené, což je {pravaHodnost}.", miraTisku, MiraTisku.MEGA)
                vytiskni(f"{CERVERNA}Soustava není řešitelná!", miraTisku)
                return None
        # 1. Najdeme pivoty
        pivoty, pozicePivotu = gp.ziskejPivoty(odstupnovanaMatice, hodnost)
        # 2. Provedeme zpětnou substituci
        vytiskni("Provedeme zpětnou substituci...\n", miraTisku)
        vytiskni("To znamená, že matici převedeme zpět na snadnou soustavu rovnic a ty vyřešíme postupně od poslední.", miraTisku, MiraTisku.MEGA)
        vytiskni("Zároveň budeme využívat již spočítaných proměnných a ty budeme do rovnic substituovat.\n", miraTisku, MiraTisku.MEGA)
        reseni = [0] * hodnost
        vyresenychPromennych = 0
        # Proměnné x1, x2, ..., xR (R = hodnost matice)v
        for i in reversed(range(hodnost)):
                # Získáme rovnici
                vektor = gp.vytvorRovnici(odstupnovanaMatice, i, pozicePivotu)
                # Hezký výpis původní rovnice
                vytiskniMatici(f"Rovnice {i + 1}:", vektor, miraTisku, MiraTisku.VYSOKA)
                # If statement zabrání akci, která nic nedělá (hezčí výpis)
                if pozicePivotu[i] != vektor.indexRovnitka:
                        # Převedeme vše kromě pivota na pravou stranu
                        gp.prevedRovniciNaDruhouStranu(vektor, pozicePivotu[i])
                        # Hezký výpis rovnice převedené na pravou stranu
                        vytiskniMatici("Vše kromě pivota převedeme na pravou stranu:", vektor, miraTisku, MiraTisku.VYSOKA)
                # Substituujeme spočítané proměnné
                if i != hodnost - 1:
                        vektor = gp.provedZpetnouSubstituci(vektor, reseni, vyresenychPromennych, hodnost, pozicePivotu, miraTisku)
                # Vydělíme pivotem
                if pivoty[i] != 1:
                        # Vydělíme pivotem
                        vektor /= pivoty[i]
                        # Hezký výpis po vydělení pivotem
                        vytiskniMatici(f"Vydělíme pivotem {zformatujCislo(pivoty[i], end="")}:", vektor, miraTisku, MiraTisku.VYSOKA)
                # Přidáme do výsledku
                reseni[i] = vektor
                vyresenychPromennych += 1

                pockej(miraTisku, MiraTisku.VYSOKA)

        # 3. Vytiskneme řešení
        if miraTisku != MiraTisku.ZADNA:
                print("Řešení:")
                kopijeReseni = reseni.copy()
                for i in range(odstupnovanaMatice.n):
                        # Není pivot
                        if i not in pozicePivotu:
                                vytiskniPromennou(1, i, odstupnovanaMatice.n, False, end=" je volná proměnná\n")
                        else: # Je pivot
                                # Výsledek je vektor
                                if isinstance(kopijeReseni[0], Vektor):
                                        kopijeReseni[0].vypis()
                                # Výsledek je číslo
                                else:
                                        print(kopijeReseni[0])
                                kopijeReseni.pop(0)

        vytiskni("Pokud jsi nejen koukal, ale i počítal, mělo by ti to vyjít stejně.", miraTisku, MiraTisku.MEGA)
        vytiskni("", miraTisku)

        return reseni

def reseniSoustavy(matice, miraTisku = MiraTisku.ZADNA):
        """
        Vypočítá řešení soustavy rovnic

        @param matice: matice soustavy rovnic
        @param miraTisku: míra tisku programu

        @return: vektor řešení
        """
        vytiskniMatici("Původní matice:", matice, miraTisku)
        odstupnovanaMatice = GaussovaEliminace(matice, miraTisku)
        vytiskniMatici("Odstupňovaná matice:", odstupnovanaMatice, miraTisku)
        return zpetnaSubstituce(odstupnovanaMatice, miraTisku)