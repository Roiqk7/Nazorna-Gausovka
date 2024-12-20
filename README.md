# Názorná Gaussova eliminace

Program na vizualizaci řešení soustavy lineárních rovnic pomocí [Gaussovy eliminace](https://cs.wikipedia.org/wiki/Gaussova_eliminační_metoda).

## Závislosti

- [Python v3.13.0](https://www.python.org/downloads/)
- [Colorama v0.4.6](https://pypi.org/project/colorama/)
- [NumPy v2.2.0](https://numpy.org/)

Pro instalaci závislostí použijte následující příkaz:

```bash
pip install -r docs/zavislosti.txt
```

## Instalace

Naklonujte si tento repozitář:

[GitLab](https://gitlab.mff.cuni.cz/sevecep/nazorna-gausovka)
```bash
git clone https://gitlab.mff.cuni.cz/sevecep/nazorna-gausovka
```

[GitHub](https://github.com/Roiqk7/nazorna-gausovka)
```bash
git clone https://github.com/Roiqk7/nazorna-gausovka
```

## Použití

Pokud jste ještě neučinili, přejděte do složky s projektem:

```bash
cd nazorna-gausovka
```

Spusťte program pomocí příkazu:

```bash
python3 src/main.py [--vstup VSTUP] [--nacti NACTI] [--uloz ULOZ] [--tisk TISK] [--ukazka] [--teorie] [--test] [--pomoc]
```

### Příklady spuštění

```bash
python3 src/main.py --vstup="[1 3 5; 2 4 6; 7 8 10]" --tisk=3"
```

```bash
python3 src/main.py --nacti="data/vstup.tex" --uloz="data/vystup.tex" --tisk=1
```

```bash
python3 src/main.py --teorie
```

### Parametry

- `--vstup`: Soustava lineárních rovnic ve formátu matlabu (více viz níže)
- `--nacti`: Název souboru se vstupními daty v [LaTeXu](https://www.overleaf.com/learn/latex/Matrices)
- `--uloz`: Název souboru pro uložení výstupních dat
- `--tisk`: Míra tisku (0-3), 0 je žádné, 3 je vše
- `--ukazka`: Předvede program na ukázkovém vstupu
- `--teorie`: Zobrazí stručný úvod do teorie lineární algebry
- `--test`: Spustí testy
- `--pomoc`: Zobrazí nápovědu

*Pozn.:* Parametry `--vstup` a `--nacti` nelze použít současně.

### Vstupní a výstupní formát

- parametr `--vstup` očekává matici ve [formátu matlabu](https://www.mathworks.com/help/matlab/learn_matlab/matrices-and-arrays.html)
  - např.: `[1 3 5; 2 4 6; 7 8 10]`
  - matice musí být obalena hranatými závorkami
  - řádky musí být odděleny středníkem
  - prvky v řádku musí být **odděleny mezerou**
- parametr `--nacti` očekává soubor s maticí ve formátu [LaTeXu](https://www.overleaf.com/learn/latex/Matrices)
  - soubor musí obsahovat **pouze matici**
  - matice musí být uzavřena do prostředí `matrix`, `bmatrix` nebo `pmatrix`
  - řádky musí být odděleny `\\`
  - jednotlivé prvky matice musí být odděleny `&`
- parametr `--uloz` uloží výstup do souboru ve formátu [LaTeXu](https://www.overleaf.com/learn/latex/Matrices)

#### Matlab formát

- matice je uzavřena do hranatých závorek
- řádky jsou odděleny středníkem
- prvky v řádku jsou odděleny mezerou

Např. matice

```
1 2 3
4 5 6
7 8 9
```

je ve formátu matlabu: `[1 2 3; 4 5 6; 7 8 9]`.

Pro referenci použijte [Matlab](https://www.mathworks.com/help/matlab/learn_matlab/matrices-and-arrays.html)

#### LaTeX formát

- matice je uzavřena do prostředí `matrix`, `bmatrix` nebo `pmatrix`
- řádky jsou odděleny `\\`
- prvky v řádku jsou odděleny `&`

Např. matice

```
1 2 3
4 5 6
7 8 9
```

je ve formátu LaTeX:

```latex
\begin{pmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9 \\
\end{pmatrix}
```

Pro referenci použijte [Overleaf](https://www.overleaf.com/learn/latex/Matrices)

### Doporučení

- Pokud o lineární algebře nevíte nic, zobrazte si teorii (`--teorie`).
- Pokud chcete vidět, jak program funguje, spusťte ukázku (`--ukazka`).
- Doporučuji začít s maximálním tiskem (`--tisk=3`) a s nabývajícím pochopením snižovat míru tisku.
- Pokud chcete zkontrolovat, zda program funguje správně, spusťte testy (`--test`).

## Látka lineární algebry

Všechny znalosti jsou čerpány z přednášek [Lineární algebra 1](https://kam.mff.cuni.cz/~hladik/LA1/) na MFF UK. Především ze [skript pana prof. Milana Hladíka](https://matfyzpress.cz/cz/e-shop/vsechny-tituly/linearni-algebra-nejen-pro-informatiky-9788073783921)

## Feedback

Pokud jste našli chybu, nebo máte nápad na vylepšení, vytvořte issue na [GitHubu](https://github.com/Roiqk7/nazorna-gausovka).