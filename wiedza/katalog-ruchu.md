# Katalog ruchu

Słownik, z którego Claude dobiera ruch. Każda pozycja: co robi, kiedy pasuje, liczby, ryzyka (z kontroli `tools/overlap.py`), gdzie już użyta. Status: **wybrane** / do oceny / odrzucone (z powodem).

## Pojawianie się tekstu

| Ruch | Co robi | Liczby | Kiedy pasuje | Ryzyko | Gdzie |
|---|---|---|---|---|---|
| Przewrót liter | Litera obraca się w 3D z −90° do 0 wokół osi za sobą, rośnie z 1,5× w pionie | 1,1 s quart in-out, co .035 s; oś .85em za literą | Wielkie tytuły; „podpis” oryginału | Litera startuje .85em pod swoim miejscem i przelatuje przez wiersz niżej: gdy tam coś stoi, obrócić od góry (+90°) | hero A–D, „O nas”, stopka, nagrody |
| Przewrót linii | Jak wyżej, cała linia słów | .5 s quad in-out, co .1 s | Akapity, notki | Na wąskich ekranach notka pod tytułem: startować po tytule | notka hero, „O nas” |
| Fala od punktu | Opóźnienie liter rośnie z odległością od punktu (np. od „O”) | do .55 s rozrzutu | Gdy jeden element jest źródłem ruchu | Wiersze nad źródłem muszą wchodzić od góry | hero B |
| Taśma z kolumny | Litery po każdej stronie kolumny wysuwają się z niej razem, jak taśma; widoczne dopiero po wyjściu z kolumny | 1,05 s power2.out; wiersz źródła 0, pozostałe +.12 s | Gdy coś „wydaje” tekst (wir, szczelina, maszyna) | Taśma jest sztywna, więc litery się nie zderzają; litery w samej kolumnie jadą niewidoczne i pokazują się na ostatnią ćwierć litery | hero G |
| Wyostrzenie z rozmycia | Tekst wyłania się z rozmycia i przezroczystości | rozmycie 18px·(rem/14) → 0 | Jako lustro wyjścia przez rozmycie; spokojne, „kinowe” | Rozmycie dużych liter bywa drogie na telefonie (zmierzyć) | hero E, F; wyjście 1 |

### Tekst „z dymu” (do oceny, 10.10.2026; Grzegorz chce subtelnie i delikatnie)

| Nr | Ruch | Jak zrobione | Liczby |
|---|---|---|---|
| 1 | Mgła | każda litera: krycie, rozmycie 14px·k → 0, skala 1,06 → 1; losowa kolejność | 1,6 s power2.out, rozrzut .7 s |
| 2 | Dym w górę | litera unosi się o .18em, rozmycie 12px·k → 0, wyższa 1,15× → 1 (od dołu); wiersze od najniższego | 1,8 s power3.out, co .18 s + losowo .25 s |
| 3 | Zawirowanie | filtr SVG: `feTurbulence` + `feDisplacementMap` (falowanie krawędzi 45px·k → 0) + rozmycie 9px·k → 0 | 2,1 s power2.out |
| 4 | Rozpraszanie | filtr SVG: szum (`fractalNoise`, 0,035/k) jako maska krycia, próg rośnie, maska lekko rozmyta (kłęby) | 1,9 s power1.inOut |
| 5 | Dym z „O” | maska: miękkie koło rośnie od środka „O” + rozmycie 10px·k → 0 | 2,1 s power2.out |
| 6 | Smugi wiru | filtr SVG: poziome rozmycie 36px·k → 0; wiersze na przemian z prawej/lewej o .35em | 1,8 s power3.out |
| 7 | Zbieranie się | litery blisko miejsca (.1 odległości od środka + losowo .12em), gęsty dym (rozmycie 22px·k, skala 1,08), położenie ustala się wcześnie, czerń dopiero na końcu | 2,1 s; krycie `.35·min(1,t/.2) + .65·t³` |
| 8 | Oddech | cały tytuł z mgiełki (rozmycie 6px·k), skala 1,035 → 1 | 2,4 s power1.out |
| 9 | Zawirowanie, czerń na końcu | jak 3, ale dym jasny i czerń dopiero na końcu, zawirowanie uspokaja się wolniej | 2,4 s; krycie jak w 7 |

k = rem/14 (rozmycie rośnie z wielkością liter). Notka po tytule: a) słowa od środka na boki z losowym opóźnieniem, b) miękka maska od środka, c) litery jak pył. Wersje 3 i 4 pierwotnie za mocne (zniekształcone litery, ostre plamy), złagodzone.
**d · dym w zwolnionym tempie (WebGL, 10.10, po filmie „Smoke Text Reveal”):** warstwa WebGL nad tytułem; dym = szum fbm (5 oktaw) z zawinięciem dziedziny, płynie powoli; czoło (z lewej albo od „O”) przechodzi przez tytuł w 3,3 s (sine in-out), jego poszarpany brzeg przykrywa dym, litery w dymie lekko falują; dym rzednie od 2,4 s przez 1,5 s; tytuł narysowany w teksturze literami w ich miejscach, na końcu na wierzch wchodzi tekst strony (.35 s), potem warstwa znika (przenikanie obu dawało szary dołek). d1 jasny z lewej, d2 jak tusz, d3 jasny od „O”.
**Wybrane: d3** (dym wypływa spod „O”, rozchodzi się pierścieniem). **5 zachowana** jako lżejsza wersja na telefony (`?fx=5`).
**Zostają 3, 5 i 7 (a, b, c); reszta odrzucona (10.10).** Wspólny rytm (`form`, `ink` w `lab/hero.html`): [0–.5] wolno i bardzo jasno (krycie do .12, forma do .2, lekkie kołysanie), [.5–.8] szybki rdzeń (forma i krycie razem, cubic in-out), [.8–1] spokojne domknięcie. 5: wypełnienie koła dogania jego brzeg na końcu, więc zdjęcie maski nic nie zmienia (wcześniej skok przy prawej krawędzi). Grzegorz: „nie lubię, jak tekst tylko zmienia kolor z jednego w drugi – to ma być cała forma”.
**Uwagi Grzegorza (10.10, wcześniej):** na razie 3, podoba się też 7; „czerń dopiero na samym końcu” (lekki dym od razu, gęstnienie w czerń w ostatniej części); notka a rusza w połowie pojawiania się tytułu.

## Okna i bryła

| Ruch | Co robi | Liczby | Kiedy pasuje | Ryzyko | Gdzie |
|---|---|---|---|---|---|
| Okno rośnie do ekranu | Wycięcie warstwy z bryłą rośnie od elementu do pełnego ekranu | krawędzie quad out przez 75%, rogi w ostatnich 25% | Przejście hero → następna sekcja | Mierzyć w układzie warstwy, nie okna przeglądarki (pasek przewijania) | hero, intro |
| Elipsa ładowania → litera | Elipsa z bryłą na środku pustej strony (CSS od pierwszego malowania) przejeżdża w „O” | 1,15 s quart in-out; elipsa 10 × 10,5rem | Ładowanie, które nie jest pustą stroną; ciągłość | Litery wstają w trakcie: wiersz nad „O” od góry | hero C, D, G |
| Nawijanie drutu | Bryła rysuje się wzdłuż długości (`setDrawRange`) | 1,5–1,6 s power2.inOut | Ładowanie jako „materiał powstaje”; może pokazywać prawdziwy postęp | W lab tylko pokaz; prawdziwy postęp wymaga ładowania bibliotek w tle | hero D, F |
| Z wnętrza „O” | Start jak koniec przewijania intro (czerń, duża bryła), potem to samo przewijanie wstecz | 2,1 s power2.inOut | Pętla opowieści: wchodzimy z „O”, przewijamy z powrotem w „O” | Tekst przy kurczącej się czerni gaśnie z odległością (inaczej czarny na czarnym) | hero E, F |
| Wkręcenie bryły | Bryła dostaje rozpęd obrotu, który wygasa | `kick` 2,5–4 → 0 przez 1,4–2,6 s | Akcent na starcie; „wir” | — | hero B, C, G |

## Zasady, które wyszły z prób
- **Tekst gaśnie, gdy zbliża się czarne okno:** krycie liczone z odległości do krawędzi okna (0 przy styku, 1 przy 1,5rem). To zasada, a nie dobrany czas, więc działa na każdym ekranie.
- **Elementy w ruchu sprawdza narzędzie co klatkę** (`tools/overlap.py`), nie oko na jednym zrzucie.
- **Bryła w literze:** na wprost i nieruchoma (bez kołysania i myszy), inaczej wygląda na przesuniętą.

## Pomysły jeszcze niezrobione
- **Paski stają się literami:** paski z dołu podnoszą się jak kurtyna i „wycinają” z siebie wiersze tytułu.
- **Prawdziwy postęp ładowania:** nawijanie drutu sterowane wczytywaniem fontów i biblioteki 3D (ładowanej w tle).
