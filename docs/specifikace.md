# Naučná Gaussova eliminace

Petr Ševěček, 25. 11. 2024

## 1. Idea a základní popis problému

Program na vizualizaci řešení soustavy rovnic pomocí Gaussovy eliminace.

## 2. Formalizace problému

Pro látku lineární algebry budu využívat zejména skripta pana prof. Milana Hladíka. Implementuji algoritmus REF definovaný ve skriptech. REF bude při každém kroku vypisovat změny v lidsky přívětivém formátu. Pro zpětnou substituci použiji vlastní algoritmus snažící se napodobit lidský přístup. Program bude vypisovat průběh výpočtu do konzole.

## 3. Základní popis algoritmu

Po načtení vstupu z konzole se matice pomocí Gaussovy eliminace upraví na odstupňovaný tvar. Tento algoritmus opisuji ze skript, proto si na ně dovolím odkázat. Po dosažení odstupňovaného tvaru se provede zpětná substituce, která je popsána následovně. Nejdříve algoritmus získá hodnost a pivoty odstupňované matice. Následně se postupně prochází od posledního řádku a postupně vypočítávají hodnoty jednotlivých proměnných, přičemž každá proměnná je definovaná vektorem. Algoritmus podporuje i parametry.

## 4. Vstup a výstup

Vstup a výstup je dvojího druhu. Jednodušší je vstup, ve formátu matlabu. Tedy např.: `[1 2 3; 4 5 6; 7 8 9]`. Výstup je pak výpis postupu výpočtu a výsledný vektor řešení soustavy rovnic. Jako druhý typ vstupu je možné zadat jméno souboru s latexovým zápisem matice. Následně pomocí vlastního parseru se matice převede do formátu, který je pro program srozumitelný. Jako výstup je pak možné opět specifikovat soubor, do kterého se výsledek uloží v latexové notaci.

## 5. Formát interakce

Interakce probíhá exkluzivně přes konzoli. Program se spouští s parametry, které určují vstupní a výstupní hodnoty či soubory. Dále program vypisuje informace o průběhu výpočtu a výsledný vektor řešení soustavy rovnic.