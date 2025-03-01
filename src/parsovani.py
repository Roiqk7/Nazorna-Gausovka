""" 
Datum: 19. 12. 2024

Tento soubor obsahuje funkce pro parsování z a do latexu.

Nástroj na testování texu: https://www.quicklatex.com
"""

from matice import Matice
from tisk import zformatujCisloProLatexVypis, vytiskniChybu, zformatujPromenou
import numpy as np

PRAH_ROVNOSTI_INTU = 1e-5

def numpyNaMatice(numpyMatice):
        """
        Převede numpy matici na Matici

        @param numpyMatice: numpy matice

        @return: Matice
        """
        m, n = numpyMatice.shape
        # Pravá strana
        pravaStrana = numpyMatice[:, -1]
        numpyMatice = numpyMatice[:, :-1]
        # Matice
        prava = Matice(m, 1, pravaStrana.flatten())

        return Matice(m, n - 1, numpyMatice.flatten(), prava)

def zpracujMatlabMatici(vstup):
        """
        Zpracuje vstupní matici ve formátu matlabu

        @param vstup: vstupní matice ve formátu matlabu

        @return: matice

        @note Očekávaný formát např.: [1 3 5; 2 4 6; 7 8 10]
        """
        # Prázdný vstup
        if not vstup.strip():
                vytiskniChybu("Nelze zpracovat prázdný vstup.")
                raise ValueError("Nelze zpracovat prázdný vstup.")
        radky = vstup.replace(",", " ").strip("[]").split(";")
        hodnoty = [list(map(float, radek.split())) for radek in radky]
        numpyMatice = np.array(hodnoty).astype(np.float64)

        return numpyNaMatice(numpyMatice)

def latexNaMatici(latex):
        """
        Převede latex na matici

        @param latex: latex

        @return: matice

        @note: Referenční formát: https://www.overleaf.com/learn/latex/Matrices
        """
        latex = latex.strip()
        # Předpokládáme, že je matice obalena matrix, pmatrix nebo bmatrix
        latex = latex.replace("\\begin{matrix}", "").replace("\\end{matrix}", "")
        latex = latex.replace("\\begin{bmatrix}", "").replace("\\end{bmatrix}", "")
        latex = latex.replace("\\begin{pmatrix}", "").replace("\\end{pmatrix}", "")
        # Rozdělíme na řádky podle "\\"
        radky = latex.strip().split("\\\\")
        # Odstraníme prázdné řádky
        radky = [radek for radek in radky if radek.strip()]
        # Rozdělíme na sloupce podle "&"
        hodnoty = [radek.strip().split("&") for radek in radky]
        # Převedeme na floaty
        hodnoty = [[float(hodnota) for hodnota in radek] for radek in hodnoty]

        # Převedeme na numpy matici
        numpyMatice = np.array(hodnoty).astype(np.float64)

        return numpyNaMatice(numpyMatice)

def pripravReseniNaLatex(reseni, N):
        """
        Připraví řešení pro latex formát

        @param reseni: řešení
        @param N: počet proměnných

        @return: řešení připravené pro výpis do latexu
        """
        pripraveneReseni = [0] * N
        volnePromene = [False] * N

        for i in range(N):
                if len(reseni) > 0:
                        vektor = reseni.pop(0)
                        # Najdi pivota
                        while i < N and vektor.prvek(i) == 0:
                                pripraveneReseni[i] = f"x_{i + 1}"
                                i += 1
                        if i != N:
                                pivotLatex = ""
                                if volnePromene[i]:
                                        pripraveneReseni[i] = "je volná proměnná"
                                        print(i)
                                else:
                                        # Aby bylo znaménko hezké
                                        prvníPridanyClen = False
                                        # Najdi volné proměnné
                                        for j in range(i + 1, N):
                                                koeficient = vektor.prvek(j)
                                                if koeficient != 0:
                                                        pivotLatex += zformatujCisloProLatexVypis(koeficient, prvníPridanyClen, N, j)
                                                        volnePromene[j] = True
                                                        prvníPridanyClen = True

                                        # Absolutní člen
                                        absolutniClen = vektor.prvek(N)
                                        if absolutniClen != 0 or not prvníPridanyClen:
                                                pivotLatex += zformatujCisloProLatexVypis(absolutniClen, prvníPridanyClen)

                                        pripraveneReseni[i] = pivotLatex
                else:
                        # Dopln zbylé parametry
                        for j in range(N):
                                if volnePromene[j]:
                                        pripraveneReseni[j] = zformatujPromenou(j, N)
                        while i < N:
                                # Ošetříme, že se nepřepíše nějaký pivot
                                # Např. pro reseniNaLatex([Vektor(5, [1, 0, 5/2, 0, -4]), Vektor(5, [0, 1, -2, 0, 2]), Vektor(5, [0, 0, 0, 1, 1])])
                                if pripraveneReseni[i] == "":
                                        pripraveneReseni[i] = zformatujPromenou(j, N)
                                i += 1

        return pripraveneReseni

def reseniNaLatex(reseni):
        """
        Převede řešení na latex

        @param reseni: řešení

        @return: řešení v latexu
        """
        vyslednyRetezec = "\\documentclass{article}\n" \
                          "\\usepackage[utf8]{inputenc}\n" \
                          "\\usepackage[T1]{fontenc}\n" \
                          "\\usepackage{amsmath}\n" \
                          "\\begin{document}\n" \
                          "\\section*{Reseni}\n" # Řešení nelze zapsat, jelikož to na Windowsech dělá potíže
        if reseni == None:
                vyslednyRetezec += "x = \\emptyset\n"
        else:
                # Zjisti počet proměnných
                N = reseni[0].m - 1

                # Levá strana (x1, x2, ..., xn)^T
                vyslednyRetezec += "\\[\n\\begin{pmatrix}\n"
                for i in range(0, N):
                        promenna = zformatujPromenou(i, N)
                        vyslednyRetezec += f"{promenna} \\\\\n"
                vyslednyRetezec += "\\end{pmatrix} = \n"

                # Pravá strana
                reseni = pripravReseniNaLatex(reseni, N)
                vyslednyRetezec += "\\begin{pmatrix}\n"
                for i in range(N):
                        vyslednyRetezec += f"{reseni[i]} \\\\\n"
                vyslednyRetezec += "\\end{pmatrix}\n"

        vyslednyRetezec += "\\end{document}"

        return vyslednyRetezec