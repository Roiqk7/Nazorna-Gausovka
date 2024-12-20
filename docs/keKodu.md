# Programátorská dokumentace

## Struktura projektu

- `src/` - zdrojové kódy programu
    - `main.py` - vstupní soubor programu
    - `gauss.py` - soubor s implementací funkcí pro řešení soustavy rovnic
    - `gaussPomocne.py` - obsahuje pomocné funkce pro řešení soustavy rovnic
    - `matice.py` - soubor s implementací třídy Matice
    - `teorie.py` - teoretický úvod do lineární algebry
    - `test.py` - soubor s testy
    - `tisk.py` - soubor s funkcemi pro tisk výstupu
    - `ukazka.py` - snaží se předvést program na ukázkovém vstupu
    - `vektor.py` - soubor s implementací třídy Vektor
    - `zpracovaniVstupu.py` - soubor s funkcemi pro zpracování vstupu

## Průběh programu

Uživatel spustí funkci `main` ze souboru `main.py` se vstupními argumenty. Argumenty se předají funkci `zpracujArgumenty` ze souboru `zpracovaniVstupu.py`, která zpracuje vstupní argumenty a rozhodne o dalším postupu programu. Další průběh programu závisí na uživatelských argumentech.

## Třídy

### Matice

TřízpetnaSubstituce slouží k reprezentaci matice. Třída `Matice` se používá zejména ve funkci `GaussovaEliminace` a s ní souvisejících funkcích. Od toho se odvíjí i většina metod třídy `Matice`.

### Vektor

Třída `Vektor` slouží k reprezentaci vektoru. Třída `Vektor` dědí od třídy `Matice` a používá se zejména ve funkci `zpetnaSubstituce` a s ní souvisejících funkcích. Od toho se například odvíjí interpretace hodnot vektoru, kde prvky 1 - N se interpretují jako proměnné a poslední prvek jako absolutní hodnota. Na rozdíl od třídy `Matice` obsahuje zajímavější výpis na příkazovou řádku.