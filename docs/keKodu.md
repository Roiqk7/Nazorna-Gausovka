# Programátorská dokumentace

## Struktura projektu

- `src/` - zdrojové kódy programu
    - `main.py` - vstupní soubor programu
    - `gauss.py` - soubor s implementací funkcí pro řešení soustavy lineárních rovnic
    - `gaussPomocne.py` - obsahuje pomocné funkce pro řešení soustavy lineárních rovnic
    - `matice.py` - soubor s implementací třídy Matice
    - `teorie.py` - teoretický úvod do lineární algebry
    - `test.py` - soubor s testy
    - `tisk.py` - soubor s funkcemi pro tisk výstupu
    - `ukazka.py` - snaží se předvést program na ukázkovém vstupu
    - `vektor.py` - soubor s implementací třídy Vektor
    - `zpracovaniVstupu.py` - soubor s funkcemi pro zpracování vstupu

## Průběh programu

Uživatel spustí funkci `main` ze souboru `main.py` se vstupními argumenty. Argumenty se předají funkci `zpracujArgumenty` ze souboru `zpracovaniVstupu.py`, která zpracuje vstupní argumenty a rozhodne o dalším postupu programu. Další průběh programu závisí na uživatelských argumentech. Zde je jednoduchý diagram průběhu programu:

```
main -> zpracujArgumenty -> 1. Matice? -> zpracuj_Matici -> GaussovaEliminace -> zpetnaSubstituce -> 1. Uložit řešení? -> ulozReseniDoSouboru
                         -> 2. Spustit testy? -> testuj
                         -> 3. Teorie? -> teorieMain
                         -> 4. Ukázka? -> mainUkazka
                         -> 5. Vypsat nápovědu? -> pomoc
```

## Třídy

### Matice

Třída `Matice` se používá zejména ve funkci `GaussovaEliminace` a s ní souvisejících funkcích. Od toho se odvíjí i většina metod třídy `Matice`. Jak z názvu vyplývá tak třída slouží k reprezentaci matic jako [NumPy matic](https://numpy.org/doc/2.1/reference/generated/numpy.matrix.html) s metodami pro řešení soustavy lineárních rovnic. Třída obsahuje metody pro výpis matice na příkazovou řádku, zjištění počtu řádků a sloupců, zjištění hodnoty na zadaných souřadnicích, jednotlivé elementární řádkové operace a další.

### Vektor

Třída `Vektor` slouží k reprezentaci vektoru. Třída `Vektor` dědí od třídy `Matice` a používá se zejména ve funkci `zpetnaSubstituce` a s ní souvisejících funkcích. Od toho se například odvíjí interpretace hodnot vektoru, kde prvky 1 - N se interpretují jako proměnné a poslední prvek jako absolutní hodnota. Na rozdíl od třídy `Matice` obsahuje zajímavější výpis na příkazovou řádku. Většina metod třídy `Vektor` je převzata z třídy `Matice`, akorát počet sloupců je nastaven na 1.

## Funkce

Výběr nejdůležitějších funkcí:

### GaussovaEliminace(matice, miraTisku = MiraTisku.ZADNA)

Jedná se o implementaci algoritmu Gaussovy eliminace ze skript pana prof. Milana Hladíka. Já jsem funkci doplnil o naučné výpisy, které ovšem nijak nemění základní logiku. Co ovšem logiku mění je výběr pivota, kde se používá tvz. `hezkost pivota`, která je určena pomocnou funkcí `jeHezkyPivot(pivot)`.

### zpetnaSubstituce(matice, miraTisku = MiraTisku.ZADNA)

Tato funkce obdrží matici v odstupňovaném tvaru a provede zpětnou substituci. Funkce je implementována dle mého vlastního algoritmu, jenž se snaží napodobit lidský přístup k řešení soustavy lineárních rovnic. Algoritmus funguje následovně:

```
0. Spočítáme hodnost matice a zjistíme, zda je soustava řešitelná
1. Pokuď není soustava řešitelná, skončíme
2. Najdeme pivoty
3. Pro každého pivota od zadu:
        1) Vytvoříme rovnici pro i-tého pivota
        2) Převedeme vše kromě pivota na pravou stranu
        3) Substituujeme spočítané proměnné
        4) Vydělíme pivotem
        5) Přidáme rovnici do výsledného pole
4. Vytiskneme řešení
```
