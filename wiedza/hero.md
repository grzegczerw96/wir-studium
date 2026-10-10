# Hero: decyzje i warianty (10.10.2026)

Przeniesione z CLAUDE.md (§2). Próby leżą w `lab/hero.html` (zamrożony pokaz, wszystkie warianty dostępne przez parametry adresu). Na stronę główną przenosimy tylko to, co wybrane.

## Wybrane (do przeniesienia na stronę główną)

| Co | Wybór | W labie |
|---|---|---|
| Układ | 2: okno jako litera „O” w „TO”, wiersze wyśrodkowane | `?v=2` |
| Krój tytułu | A: Inter Tight Black, normalna szerokość | `?f=1` |
| Wejście | C: elipsa ładowania wskakuje w „O” | `?w=C` |
| Tytuł | d3: dym w zwolnionym tempie (WebGL) spod „O” | `?fx=d3` |
| Wyjście przy rośnięciu okna | 1: rozmycie | `?x=1` |
| Notka | bezszeryfowa, `text-align-last:left`, prawy dolny róg; wejście a (słowa od środka na boki) | domyślnie (przycisk notki) |

**Wersja 5 (dym z „O”, maska) to kandydat na telefony**, nie wersja odrzucona: jest lżejsza niż WebGL. Jeśli d3 okaże się za ciężki na prawdziwym telefonie (`tools/phone.py`), na telefonach używamy 5 (`?fx=5`).

Jeśli „O” nie zadziała na stronie, wracamy do układu 1 (jak w oryginale, `?v=1`).

## Uwagi Grzegorza i ustalenia (pełna lista)

- obecny układ hero mu się nie podoba; szukamy nowego (jeden wariant podobny do cappen, inne, w których obraz współpracuje z napisem);
- notka hero tylko bezszeryfowa (bez kursywy szeryfowej), ostatnia linia nie rozciągnięta (`text-align-last:left`);
- wejście bez losowego rozrzutu liter; punkt wyjścia to wejście oryginału (litery i linie przewracają się w 3D po kolei);
- krój tytułu do wyboru: obecny Archivo 125% to nie krój oryginału (ten ma normalną szerokość);
- kolejność: najpierw wygląd hero, potem wejście i przewijanie intro.
- **wybrane:** układ 2 z `lab/hero.html` (okno jako litera „O” w „TO”, wiersze wyśrodkowane) i krój A (Inter Tight Black, normalna szerokość);
- bez kreski pod nagłówkiem i bez najwyższego (1 px) paska na dole; paski wchodzą od najniższego, wyższe niewidoczne do swojej kolejki;
- spirala w „O” mniejsza (ok. 72% wysokości litery) i na wprost, dziura na środku; przechyla się dopiero, gdy okno rośnie;
- notka na desktopie: pierwsza linia na równi z górą wersalików tytułu (liczone z linii bazowej i `actualBoundingBoxAscent`);
- gasnący szary napis przy rośnięciu okna rozprasza; **wybrane wyjście 1: rozmycie** (litery w miejscu, rozmywają się i gasną; nie prześwitują przez rosnącą ramkę);
- „O” = obrys prawdziwego znaku O kroju (zmierzony z canvas: szerokość, pudełko farby), w środku **metalowa spirala 3D z głównej strony** (ok. 90% szerokości światła litery), **na wprost, bez kołysania i bez reakcji na mysz** (obrót wokół pionu i kołysanie robiły jedną stronę pierścienia grubszą i bryła wyglądała na przesuniętą; zmierzone: odchylenie środka ok. 1,5 px); biała spirala 2D rozciągnięta do światła była „za duża i płaska”; jeśli „O” nie zadziała, wracamy do układu 1 (jak w oryginale, `?v=1`);
- paski na dole po wejściu zawsze wszystkie trzy, pełne;
- desktop wg ustawienia Grzegorza (1536×742): tytuł 5,68rem w lewo i 1,07rem w górę od środka, notka na dole po prawej, 2,8rem nad paskami (`bottom: 7,8rem`, `right: gut + .38rem`); tytuł w układzie 2 większy: 9,75rem (tablet 8,4rem) zamiast 8,75rem;
- **tytuł: tylko d3** (Grzegorz 10.10): dym w zwolnionym tempie (WebGL) wypływa **spod litery „O”** (nie z jej środka: wtedy „O” szarzało), gdy elipsa już w nim jest, rozchodzi się pierścieniem, napis wyłania się za jego czołem; notka, gdy czoło minie środek tytułu; pozostałe wersje tylko przez `?fx=`;
- **wersja 5 (dym z „O”, maska) zachowana** w `lab/hero.html?fx=5`: może się przydać na telefony (lżejsza niż WebGL);
- **wybrane wejście: C** (elipsa ładowania wskakuje w „O”); potem **tytuł pojawia się jak z dymu**; zostają 3 wersje (`?fx=3|5|7|7b|7c`): zawirowanie, dym z „O”, zbieranie się (a szept, b podmuch, c kłąb); **wspólny rytm**: powolny, bardzo jasny początek (połowa czasu), szybki rdzeń, w którym forma i czerń przychodzą razem (nie „szary napis zmieniający kolor”), końcówka spokojna; notka od środka na boki, nierówno, startuje z rdzeniem tytułu, kreski po niej, te same czasy w każdej wersji;
- wejście hero do wyboru w `lab/hero.html` (`?w=A|B|C`): A jak w oryginale; B najpierw „O” (bryła się wkręca), litery falą od niego; C elipsa ładowania z bryłą na środku pustej strony (CSS od pierwszego malowania, 10 × 10,5rem), po gotowości przejeżdża w „O” (1,15 s quart in-out), litery wstają wokół; rekomendacja Claude: C;
- `lab/hero.html` ma tryb „przesuń”: Grzegorz sam przesuwa tytuł i notkę, przesunięcia (w rem) są w adresie (`&t=x,y&n=x,y`) i do skopiowania.
