""" 
Datum: 30. 11. 2024

Testovací skript pro testování programu

Stránka na kontrolu výpočtů: https://matrix.reshish.com
"""

from gauss import FrobeniovaVeta, GaussovaEliminace, rank, reseniSoustavy
import gaussPomocne as gp
from matice import Matice
from parsovani import zpracujMatlabMatici, latexNaMatici
from tisk import vytiskniChybu, vytiskniUspech, vytiskniAssertChybu, MiraTisku
from vektor import Vektor
from math import isclose

PRAH_ROVNOSTI_CISEL = 1e-5

def testuj():
        """
        Hlavní testovací funkce
        """
        print("Testování...")
        try:
                # betaTest()
                testujMatice()
                testujGaussovaEliminace()
                testujGaussPlus()
                testujGauss()
                testujZpracovaniArgumentu()
        except AssertionError:
                return vytiskniChybu("Test(y) selhal(y)")
        except Exception as e:
                return vytiskniChybu(f"Nastala neočekávaná chyba: {e}")
        vytiskniUspech("Všechny testy proběhly úspěšně")

def betaTest():
        """
        Beta testování programu (a hlavně tisku)
        """
        prava = Matice(3, 1, [4, 0, -4])
        matice = Matice(3, 3, [1, 1, 2, 1, -2, 1, 1, -5, 0], prava)
        skutecne = gp.prevedReseniNaSeznam(reseniSoustavy(matice, MiraTisku.MEGA))
        ocekavane = [-1/3, -1/3, 1/3, 13/3]
        assert skutecne == ocekavane

def porovnejSeznamy(seznam1, seznam2):
        """
        Porovná dva seznamy

        @param seznam1: první seznam
        @param seznam2: druhý seznam

        @return: True, pokud jsou seznamy shodné, jinak False
        """
        if len(seznam1) != len(seznam2):
                return False
        if isinstance(seznam1[0], (int, float)):
                for i in range(len(seznam1)):
                        if not isclose(seznam1[i], seznam2[i], abs_tol=PRAH_ROVNOSTI_CISEL):
                                return False
        else:
                for i in range(len(seznam1)):
                        if seznam1[i] != seznam2[i]:
                                return False
        return True

def test(ocekavane, skutecne, identifikator):
        """
        Jednoduchý testovací assert

        @param ocekavane: očekávaná hodnota
        @param skutecne: skutečná hodnota
        @param identifikator: identifikátor testu

        @return: True, pokud test prošel, jinak False
        """
        # Porovnání seznamů
        if isinstance(ocekavane, list) and isinstance(skutecne, list):
                if not porovnejSeznamy(ocekavane, skutecne):
                        vytiskniAssertChybu(skutecne, ocekavane, identifikator)
                        return False
        # Porovnání čísel
        elif isinstance(ocekavane, (int, float)) and isinstance(skutecne, (int, float)):
                if not isclose(skutecne, ocekavane, abs_tol=PRAH_ROVNOSTI_CISEL):
                        vytiskniAssertChybu(skutecne, ocekavane, identifikator)
                        return False
        # Jiné
        elif ocekavane != skutecne:
                vytiskniAssertChybu(skutecne, ocekavane, identifikator)
                return False
        return True

def zhodnotVysledek(testuCelkem, uspesne, identifikator):
        """
        Zhodnotí výsledek testu

        @param testuCelkem: počet testů
        @param uspesne: počet úspěšných testů
        @param identifikator: identifikátor testu

        @throws: AssertionError, pokud test selhal
        """
        if testuCelkem == uspesne:
                vytiskniUspech(f"Testy {identifikator} proběhly úspěšně: {uspesne}/{testuCelkem}")
        else:
                vytiskniChybu(f"Test {identifikator} selhaly: {testuCelkem-uspesne}/{testuCelkem}")
                raise AssertionError

def testujMatice():
        """
        Testování třídy Matice
        """
        uspesneTesty = 0
        testyCelkem = 0

        matice = Matice(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])

        # Test metody jsouIndexyOk
        testyCelkem += 1
        if test(True, matice.jsouIndexyOk(0, 0), f"jsouIndexyOk (0, 0)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(True, matice.jsouIndexyOk(0, 1), f"jsouIndexyOk (0, 1)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(True, matice.jsouIndexyOk(2, 2), f"jsouIndexyOk (2, 2)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(False, matice.jsouIndexyOk(3, 3), f"jsouIndexyOk (3, 3)"):
                uspesneTesty += 1

        # Test metody prvek
        for i in range(3):
                for j in range(3):
                        testyCelkem += 1
                        if test(i*3 + j + 1, matice.prvek(i, j), f"prvek ({i}, {j})"):
                                uspesneTesty += 1

        # Test metody nastavPrvek
        matice.nastavPrvek(0, 0, 10)
        testyCelkem += 1
        if test(10, matice.prvek(0, 0), "nastavPrvek (0, 0, 10)"):
                uspesneTesty += 1
        matice.nastavPrvek(2, 2, 20)
        testyCelkem += 1
        if test(20, matice.prvek(2, 2), "nastavPrvek (2, 2, 20)"):
                uspesneTesty += 1

        # Test metody vynasobitRadek
        matice = Matice(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        matice.vynasobitRadek(0, 2)
        testyCelkem += 1
        if test(2, matice.prvek(0, 0), "vynasobitRadek (0, 2)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(4, matice.prvek(0, 1), "vynasobitRadek (0, 2)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(6, matice.prvek(0, 2), "vynasobitRadek (0, 2)"):
                uspesneTesty += 1
        matice.vynasobitRadek(0, 0.5)
        testyCelkem += 1
        if test(1, matice.prvek(0, 0), "vynasobitRadek (0, 0.5)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(2, matice.prvek(0, 1), "vynasobitRadek (0, 0.5)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(3, matice.prvek(0, 2), "vynasobitRadek (0, 0.5)"):
                uspesneTesty += 1

        # Test metody pricistNasobekRadku
        matice.pricistNasobekRadku(1, 0, 1)
        testyCelkem += 1
        if test(5, matice.prvek(1, 0), "pricistNasobekRadku (1, 0, 1)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(7, matice.prvek(1, 1), "pricistNasobekRadku (1, 0, 1)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(9, matice.prvek(1, 2), "pricistNasobekRadku (1, 0, 1)"):
                uspesneTesty += 1
        matice.pricistNasobekRadku(1, 0, -1)
        testyCelkem += 1
        if test(4, matice.prvek(1, 0), "pricistNasobekRadku (1, 0, -1)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(5, matice.prvek(1, 1), "pricistNasobekRadku (1, 0, -1)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(6, matice.prvek(1, 2), "pricistNasobekRadku (1, 0, -1)"):
                uspesneTesty += 1

        # Test metody prohoditRadky
        matice.prohoditRadky(0, 1)
        testyCelkem += 1
        if test(4, matice.prvek(0, 0), "prohoditRadky (0, 1)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(5, matice.prvek(0, 1), "prohoditRadky (0, 1)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(6, matice.prvek(0, 2), "prohoditRadky (0, 1)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(1, matice.prvek(1, 0), "prohoditRadky (0, 1)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(2, matice.prvek(1, 1), "prohoditRadky (0, 1)"):
                uspesneTesty += 1
        testyCelkem += 1
        if test(3, matice.prvek(1, 2), "prohoditRadky (0, 1)"):
                uspesneTesty += 1

        zhodnotVysledek(testyCelkem, uspesneTesty, "Matice")

def testujGauss():
        """
        Testování funkce pro řešení soustav rovnic

        @note Zdroj: https://www.priklady.com/cs/index.php/matice/soustavy-rovnic-resene-pomoci-matic
        """
        uspesneTesty = 0
        testyCelkem = 0

        # Základní soustavy rovnic
        prava = Matice(3, 1, [5, 5, 4])
        matice = Matice(3, 3, [1, 2, 0, 0, 1, -3, 3, 0, -1], prava)
        skutecne = gp.prevedReseniNaSeznam(reseniSoustavy(matice))
        ocekavane = [1, 2, -1]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (snadné)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(3, 1, [13, 5, 2])
        matice = Matice(3, 3, [1, 1, 0, 0, 1, -1, 1, 0, -1], prava)
        skutecne = gp.prevedReseniNaSeznam(reseniSoustavy(matice))
        ocekavane = [5, 8, 3]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (snadné)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(3, 1, [0, 0, 0])
        matice = Matice(3, 3, [1, -2, -3, 3, 2, -1, 0, 3, 1], prava)
        skutecne = gp.prevedReseniNaSeznam(reseniSoustavy(matice))
        ocekavane = [0, 0, 0]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (nulové řešení)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(3, 1, [4, 0, -4])
        matice = Matice(3, 3, [1, 1, 2, 1, -2, 1, 1, -5, 0], prava)
        skutecne = reseniSoustavy(matice)
        ocekavane = [Vektor(4, [1, 0, -5/3, 8/3]), Vektor(4, [0, 1, -1/3, 4/3])]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (parametrizované řešení)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(3, 1, [0, 0, 0])
        matice = Matice(3, 3, [1, 2, 3, 1, 1, -2, 2, 3, 1], prava)
        skutecne = reseniSoustavy(matice)
        ocekavane = [Vektor(4, [1, 0, 7, 0]), Vektor(4, [0, 1, -5, 0])]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (parametrizované řešení)"):
                uspesneTesty += 1
        testyCelkem += 1

        # Složitější soustavy rovnic
        prava = Matice(4, 1, [4, 6, 12, 6])
        matice = Matice(4, 4, [-1, 1, -1, 1, 4, 3, -1, 2, 8, 5, -3, 4, 3, 3, -2, 2], prava)
        skutecne = gp.prevedReseniNaSeznam(reseniSoustavy(matice))
        ocekavane = [-1/3, -1/3, 1/3, 13/3]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (středně těžké)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(4, 1, [20, 11, 40, 37])
        matice = Matice(4, 4, [2, 5, 4, 1, 1, 3, 2, 1, 2, 10, 9, 7, 3, 8, 9, 2], prava)
        skutecne = gp.prevedReseniNaSeznam(reseniSoustavy(matice))
        ocekavane = [1, 2, 2, 0]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (středně těžké)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(4, 1, [4, 6, 12, 6])
        matice = Matice(4, 4, [2, 2, -1, 1, 4, 3, -1, 2, 8, 5, -3, 4, 3, 3, -2, 2], prava)
        skutecne = gp.prevedReseniNaSeznam(reseniSoustavy(matice))
        ocekavane = [1, 1, -1, -1]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (středně těžké)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(4, 1, [1, 2, 4, 1])
        matice = Matice(4, 4, [2, 1, -1, 1, 3, -2, 2, -3, 2, -1, 1, -3, 5, 1, -1, 2], prava)
        skutecne = gp.prevedReseniNaSeznam(reseniSoustavy(matice))
        ocekavane = None
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (nemá řešení)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(4, 1, [1, 3, 4, 7])
        matice = Matice(4, 4, [2, 2, -1, 5, 4, 5, 0, 9, 0, 1, 2, 2, 2, 4, 3, 7], prava)
        skutecne = reseniSoustavy(matice)
        ocekavane = [Vektor(5, [1, 0, 5/2, 0, -4]), Vektor(5, [0, 1, -2, 0, 2]), Vektor(5, [0, 0, 0, 1, 1])]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (parametrizované řešení)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(1, 1, [5])
        matice = Matice(1, 1, [1], prava)
        skutecne = reseniSoustavy(matice)
        ocekavane = [Vektor(2, [1, 5])]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (jedna rovnice)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(1, 1, [5])
        matice = Matice(1, 2, [1, 3], prava)
        skutecne = reseniSoustavy(matice)
        ocekavane = [Vektor(3, [1, -3, 5])]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (parametrizované řešení, jedna rovnice)"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(4, 1, [0, 0, 0, 0])
        matice = Matice(4, 4, [1, -3, -26, 22, 1, -8, 0, 7, 1, 1, -2, 2, 4, 5, -2, 3], prava)
        skutecne = reseniSoustavy(matice)
        # Pozn.: V zdrojové sadě je jiné řešení. Ovšem reshish se shoduje s mým řešením.
        ocekavane = [Vektor(5, [1, 0, 0, -9/7, 0]), Vektor(5, [0, 1, 0, 5/7, 0]), Vektor(5, [0, 0, 1, 5/7, 0])]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (čistě parametrizované řešení)"):
                uspesneTesty += 1
        testyCelkem += 1

        # Hilbertova matice
        prava = Matice(3, 1, [1, 1, 1])
        matice = Matice(3, 3, [1, 1/2, 1/3, 1/2, 1/3, 1/4, 1/3, 1/4, 1/5], prava)
        skutecne = gp.prevedReseniNaSeznam(reseniSoustavy(matice))
        ocekavane = [3, -24, 30]
        if test(ocekavane, skutecne, f"Řešení soustavy {testyCelkem} (Hilbertova matice)"):
                uspesneTesty += 1
        testyCelkem += 1

        zhodnotVysledek(testyCelkem, uspesneTesty, "Řešení soustav")

def testujGaussPlus():
        """
        Dodatečné testy pro funkce v gauss.py

        @note: Zdroj: https://www.karlin.mff.cuni.cz/~kuncova/1617LS_fsv2/07_reseni.pdf
        """
        uspesneTesty = 0
        testyCelkem = 0

        # Rank
        matice = Matice(3, 3, [1, -2, -1, 0, 2, -1, 0, 0, 1])
        skutecne = rank(matice)
        ocekavane = 3
        if test(ocekavane, skutecne, f"Rank matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        matice = Matice(3, 3, [1, 0, 0, 0, 1, 0, 0, 0, 0])
        skutecne = rank(matice)
        ocekavane = 2
        if test(ocekavane, skutecne, f"Rank matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        matice = Matice(3, 3, [1, 0, 0, 0, 1, 0, 0, 0, 1])
        skutecne = rank(matice)
        ocekavane = 3
        if test(ocekavane, skutecne, f"Rank matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        matice = Matice(5, 3, [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        skutecne = rank(matice)
        ocekavane = 2
        if test(ocekavane, skutecne, f"Rank matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        matice = Matice(5, 5, [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1])
        skutecne = rank(matice)
        ocekavane = 5
        if test(ocekavane, skutecne, f"Rank matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        # Frobeniova věta
        prava = Matice(3, 1, [6, 1, -1])
        matice = Matice(3, 3, [1, -2, -1, 0, 2, -1, 0, 0, 1], prava)
        skutecne = FrobeniovaVeta(rank(matice), rank(prava))
        ocekavane = True
        if test(ocekavane, skutecne, f"Frobeniova věta {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(3, 1, [1, 1, 1])
        matice = Matice(3, 3, [1, 1, 1, 0, 1, 1, 0, 0, 1], prava)
        skutecne = FrobeniovaVeta(rank(matice), rank(prava))
        ocekavane = True
        if test(ocekavane, skutecne, f"Frobeniova věta {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(3, 1, [6, 1, -1])
        matice = Matice(3, 3, [1, -2, -1, 0, 2, -1, 0, 0, 0], prava)
        skutecne = FrobeniovaVeta(rank(matice), rank(prava))
        ocekavane = False
        if test(ocekavane, skutecne, f"Frobeniova věta {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(3, 1, [1, 1, 1])
        matice = Matice(3, 3, [1, 1, 1, 0, 1, 1, 0, 0, 0], prava)
        skutecne = FrobeniovaVeta(rank(matice), rank(prava))
        ocekavane = False
        if test(ocekavane, skutecne, f"Frobeniova věta {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        zhodnotVysledek(testyCelkem, uspesneTesty, "Rank a Frobeniova věta")

def testujGaussovaEliminace():
        """
        Test pro Gaussovu eliminaci

        @note: Tvar matice po Gaussově eliminaci není jednoznačný, ovšem pozice pivotů jsou
        @note2: Zdroj: https://www.karlin.mff.cuni.cz/~kuncova/1617LS_fsv2/07_reseni.pdf
        """
        uspesneTesty = 0
        testyCelkem = 0

        prava = Matice(3, 1, [2, -30, -22])
        matice = Matice(3, 2, [2, 5, -4, 3, 4, 23], prava)
        odstupnovanaMatice = GaussovaEliminace(matice)
        _, skutecne = gp.ziskejPivoty(odstupnovanaMatice, rank(odstupnovanaMatice))
        ocekavane = [0, 1]
        if test(ocekavane, skutecne, f"Pivoty matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(4, 1, [1, 5, 4, 5])
        matice = Matice(4, 3, [1, 1, -1, 1, -1, 1, 2, 1, -1, 3, 2, -2], prava)
        odstupnovanaMatice = GaussovaEliminace(matice)
        _, skutecne = gp.ziskejPivoty(odstupnovanaMatice, rank(odstupnovanaMatice))
        ocekavane = [0, 1]
        if test(ocekavane, skutecne, f"Pivoty matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(4, 1, [1, 3, 5, 8])
        matice = Matice(4, 4, [1, 2, 1, -1, 2, 3, -1, 2, 4, 7, 1, 0, 5, 7, -4, 7], prava)
        odstupnovanaMatice = GaussovaEliminace(matice)
        _, skutecne = gp.ziskejPivoty(odstupnovanaMatice, rank(odstupnovanaMatice))
        ocekavane = [0, 1]
        if test(ocekavane, skutecne, f"Pivoty matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        prava = Matice(4, 1, [1, 1, 1, 1])
        matice = Matice(5, 5, [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1])
        odstupnovanaMatice = GaussovaEliminace(matice)
        _, skutecne = gp.ziskejPivoty(odstupnovanaMatice, rank(odstupnovanaMatice))
        ocekavane = [0, 1, 2, 3, 4]
        if test(ocekavane, skutecne, f"Pivoty matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        zhodnotVysledek(testyCelkem, uspesneTesty, "Gaussova eliminace")

def testujZpracovaniArgumentu():
        """
        Testování zpracování argumentů
        """
        # Předejdeme cyklickému importu
        from zpracovaniArgumentu import zpracujMatlabMatici

        uspesneTesty = 0
        testyCelkem = 0

        # Zpracování MatLab matice
        skutecne = zpracujMatlabMatici("[1 2 3; 4 5 6; 7 8 9]")
        ocekavane = Matice(3, 2, [1, 2, 4, 5, 7, 8], Matice(3, 1, [3, 6, 9]))
        if test(ocekavane, skutecne, f"Zpracování MatLab matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        skutecne = zpracujMatlabMatici("[1 3 5; 2 4 6; 7 8 10]")
        ocekavane = Matice(3, 2, [1, 3, 2, 4, 7, 8], Matice(3, 1, [5, 6, 10]))
        if test(ocekavane, skutecne, f"Zpracování MatLab matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        skutecne = zpracujMatlabMatici("[1 2 3 4 5; 6 7 8 9 10; 11 12 13 14 15; 16 17 18 19 20]")
        ocekavane = Matice(4, 4, [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19], Matice(4, 1, [5, 10, 15, 20]))
        if test(ocekavane, skutecne, f"Zpracování MatLab matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        # Matlab matice (divný vstup)
        skutecne = zpracujMatlabMatici("[1, 2, 3; 4, 5, 6; 7, 8, 9]")
        ocekavane = Matice(3, 2, [1, 2, 4, 5, 7, 8], Matice(3, 1, [3, 6, 9]))
        if test(ocekavane, skutecne, f"Zpracování MatLab matice {testyCelkem} (čárky)"):
                uspesneTesty += 1
        testyCelkem += 1

        skutecne = zpracujMatlabMatici("[1,2,3;4,5,6;7,8,9]")
        ocekavane = Matice(3, 2, [1, 2, 4, 5, 7, 8], Matice(3, 1, [3, 6, 9]))
        if test(ocekavane, skutecne, f"Zpracování MatLab matice {testyCelkem} (čárky, bez mezer)"):
                uspesneTesty += 1
        testyCelkem += 1

        skutecne = zpracujMatlabMatici("[1,2,3;4,5,6;7,8,9")
        ocekavane = Matice(3, 2, [1, 2, 4, 5, 7, 8], Matice(3, 1, [3, 6, 9]))
        if test(ocekavane, skutecne, f"Zpracování MatLab matice {testyCelkem} (čárky, bez mezer, neuzavřené hranaté závorky)"):
                uspesneTesty += 1
        testyCelkem += 1

        # Latex na matici
        latexMatice = "\\begin{pmatrix}\n1 & 2 & 3 \\\\\n4 & 5 & 6 \\\\\n7 & 8 & 9\n\\end{pmatrix}"
        skutecne = latexNaMatici(latexMatice)
        ocekavane = Matice(3, 2, [1, 2, 4, 5, 7, 8], Matice(3, 1, [3, 6, 9]))
        if test(ocekavane, skutecne, f"Zpracování Latex matice {testyCelkem}"):
                uspesneTesty += 1
        testyCelkem += 1

        # Pozn.: r"" je tzv. raw string. Tedy se nemusí psát dvojité '\\'
        latexMatice = r"\begin{matrix}1 & 2 & 3 \\4 & 5 & 6 \\7 & 8 & 9\end{matrix}"
        skutecne = latexNaMatici(latexMatice)
        ocekavane = Matice(3, 2, [1, 2, 4, 5, 7, 8], Matice(3, 1, [3, 6, 9]))
        if test(ocekavane, skutecne, f"Zpracování Latex matice {testyCelkem} (matrix)"):
                uspesneTesty += 1
        testyCelkem += 1

        latexMatice = r"\begin{bmatrix}1 & 2 & 3\end{bmatrix}"
        skutecne = latexNaMatici(latexMatice)
        ocekavane = Matice(1, 2, [1, 2], Matice(1, 1, [3]))
        if test(ocekavane, skutecne, f"Zpracování Latex matice {testyCelkem} (bmatrix)"):
                uspesneTesty += 1
        testyCelkem += 1

        latexMatice = r"\begin{pmatrix}1 & 2 & 3 & 4 \\4 & 5 & 6 & 7 \\7 & 8 & 9 & 10 \\ 10 & 11 & 12 & 13\end{pmatrix}"
        skutecne = latexNaMatici(latexMatice)
        ocekavane = Matice(4, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], Matice(4, 1, [4, 7, 10, 13]))
        if test(ocekavane, skutecne, f"Zpracování Latex matice {testyCelkem} (pmatrix)"):
                uspesneTesty += 1
        testyCelkem += 1

        zhodnotVysledek(testyCelkem, uspesneTesty, "Zpracování argumentů")

if __name__ == "__main__":
        testuj()