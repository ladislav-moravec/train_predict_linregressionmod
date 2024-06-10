# Vyhodnocení cílené kampaně
 Tento projekt analyzuje finanční dopad marketingové kampaně zaměřené na prodej krátkodobého cestovního pojištění. V roce 2019 byla uskutečněna direct-marketingová kampaň, při které byli zákazníci oslovení s nabídkou slevy na cestovní pojištění. Tento soubor obsahuje přehled funkcí a vysvětlení postupu, včetně interpretace dat a aplikace regresního modelu.

## Struktura projektu
### Soubory:
- main.py: Hlavní skript provádějící analýzu
- customer_data.xlsx: Excel soubor s daty
- README.md: Tento soubor s popisem projektu 
### Funkce:
- load_data(file_path)
-- Načte data z Excel souboru.

- convert_dates(df_target, df_purchases)
-- Převede sloupce s daty na datetime formát.

- calculate_common_customers(df_target, df_control)
-- Vypočítá procento zákazníků v Target, kteří jsou také v Control.

- is_within_campaign(row)
-- Kontroluje, zda byly nákupy uskutečněny do 3 měsíců od target_month.

- calculate_campaign_purchases(df_purchases, df_target)
-- Vypočítá celkovou sumu nákupů během kampaně a mimo kampaň pro Target.

- calculate_control_purchases(df_purchases, df_control)
-- Vypočítá celkovou sumu nákupů pro Control group v období leden 2019 - červen 2019.

- additional_statistics(df_purchases)
-- Vypočítá další statistiky, jako je průměrná výše nákupu, medián a směrodatná odchylka.

- apply_regression_model(df_purchases)
-- Aplikuje lineární regresní model na data a vrací model a Mean Squared Error (MSE).

- main()
-- Hlavní funkce, která koordinuje všechny ostatní funkce a vytiskne výsledky.


## Postup
- Načtení dat: Data jsou načtena z Excel souboru customer_data.xlsx a uložena do datových rámců.

- Konverze dat: Datumová pole jsou převedena na datetime formát pro snadnější manipulaci.

- Výpočet společných zákazníků: Identifikujeme zákazníky, kteří jsou v obou skupinách (Target a Control) a vypočítáme jejich procento.

- Výpočet nákupů během kampaně: Zjišťujeme, zda nákupy v Purchases tabulce spadají do 3 měsíců od target_month a vypočítáme celkovou sumu nákupů během a mimo kampaň pro Target skupinu.

- Výpočet nákupů pro kontrolní skupinu: Vypočítáme celkovou sumu nákupů pro kontrolní skupinu v období leden 2019 - červen 2019.

- Další statistiky: Vypočítáme průměrnou, mediánovou a směrodatnou odchylku výše nákupů.

- Regresní model: Používáme lineární regresní model pro predikci budoucích nákupů na základě historických dat. Model je testován pomocí Mean Squared Error (MSE).

### Interpretace dat a výsledků
#### Procento společných zákazníků
- Toto procento ukazuje, kolik zákazníků z Target skupiny bylo také v Control skupině. Je důležité zajistit, aby tyto dvě skupiny byly co nejvíce nezávislé, aby výsledky byly relevantní.

#### Celková suma nákupů během a mimo kampaň
- Tento výsledek nám ukazuje, jak efektivní byla kampaň v motivaci zákazníků k nákupu během určeného období.

#### Průměrná, mediánová a směrodatná odchylka výše nákupů
- Tyto statistiky poskytují přehled o rozdělení nákupních částek, což může pomoci při plánování budoucích kampaní.

#### Regresní model
- Lineární regresní model se používá k predikci budoucích nákupů na základě historických dat. MSE poskytuje míru přesnosti modelu. Nižší MSE znamená vyšší přesnost.



#### Interpretace a vyhodnocení kampaně
- Čistý příjem: Rozdíl mezi celkovými nákupy během kampaně a náklady na kampaň.


- Návratnost investic (ROI): Procentuální návratnost investovaných prostředků. Pokud je ROI pozitivní, kampaň byla úspěšná. Pokud je negativní, kampaň nebyla finančně úspěšná.

