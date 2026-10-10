# Pomiary oryginału (cappen.com)

Przeniesione z CLAUDE.md (§5 i §6.3) 10.10.2026. Czytać przy pracy nad daną sekcją. Liczby z kodu oryginału (`main.js`) albo zmierzone w Playwright; nowe pomiary dopisywać tutaj.

## Mapa strony i pomiary (desktop, H = wysokość ekranu)

| Sekcja | Długość | Co się dzieje (zmierzone w oryginale) |
|---|---|---|
| Preloader (oryginał) | – | Treść w `.root.hide` (`display:none`), tło i tekst `#fcfcfc`; preloader czeka na fonty i zasoby, potem `finishIntro()`: słowa gasną (.35/1.25/1.55 s), obrazki odlatują, po 1,5 s treść odsłonięta. U nas: bez preloadera, strona pusta do gotowości |
| Hero (oryginał) | – | Tytuł Helvetica Now Display Black 900, normalna szerokość, −.04em, interlinia .8, 4rem / 7,5rem / 8,75rem; desktop: wiersze od lewej, 2. i 3. wcięte o 1,94/1,93em, okno 1,8571em (260/160) w przerwie 1,97em ostatniego wiersza („FOR ▢ TODAY”), „O” w FOR to znak-ikona; telefon: wiersze wyśrodkowane, okno pod tytułem. Wejście: litery `rotateX −90→0`, `scaleY 1.5→1`, 1,1 s quart in-out co .035 s; notka liniami od .35 s. Przewijanie: okno quad out przez 75%, rogi w ostatnich 25%, spirala obraca się (X −45°→0, Z 9°→−180°, quart out) i skaluje do .75 (tablet .5), tytuł, notka i paski gasną w pierwszej połowie (`--o` 1→0, quad out) |
| Intro | 200svh | Litery nagłówka wstają, okno ze spiralą rośnie do pełnego ekranu |
| Manifest | 647svh (telefon 501) | Oś 0→1: miniatury spadają kaskadą (.15–.50), słowa wstają w 3D (.25–.48), pauza (.48–.58), słowa się przewracają (.60–.80), miniatury zsuwają się (.72–.80); spirala w środku, przyciemniana od góry |
| Przejście „Wybrane realizacje” | 350svh + tor 385svh | Etykieta z prawej, tytuł z lewej (do +1,15 H, quad out), postój do +2,2 H, rozjazd i wygaszenie do +3,2 H; spirala gaśnie w cień od S0−0,95 do S0+2,25 H |
| Karty realizacji | – | Obraz wchodzi przy 1/5 na ekranie (skala .5→1, .65 s quad out, soczewka 5→0); duże karty zjeżdżają o 30% wysokości przez 125% ekranu |
| Lista projektów | – | Wiersze rozwijają się w .6 s (quart in-out); pasek najechania rośnie od środka; na telefonie pierwszy wiersz otwiera się sam |
| O nas | – | Strona czarna → `#fcfcfc` (power1.inOut), z powrotem do czerni od „dół na 115%” do „dół na −45%”; tytuł litera po literze (.9 s quart out, co .035 s); linie tekstu .5 s quad in-out, co .1 s |
| Klienci | 350svh, margin −100svh | Od „góra przy górze” do „koniec − 0,25 H”: okno otwiera się od środka (`--mask` 49,5%→0, quart in-out), spirala wychodzi z cienia, skala .5→1, przechył 45°→90°. Po 15% wolne przewijanie w dół jest **dociągane do końca** (patrz niżej, „Mechanizmy prowadzenia przewijania”). Przy 70% wchodzą tytuł i nazwy. **Wyjście:** okno ze spiralą odjeżdża w górę w pełnym kryciu, a słowa gasną, gdy okno jest od 5% do 35% swojej wysokości nad górną krawędzią |
| Nagrody | plakaty 400svh, lista 250svh | Kolumny plakatów przesuwane zmiennymi `--progress`/`--scale`/`--spacing`; pary nazw na liście rozpisane co 1/6 osi |
| Kontakt: tytuł | 500svh, margin −30svh | Wielki napis przesuwa się z prawej krawędzi do całkowitego zniknięcia z lewej (liniowo) |
| Kontakt: formularz | 500svh (telefon 300), margin −250svh | Trzy ramki wjeżdżają z lewej (`--start` 1→0, quad in-out, co .1, scrub .5): u nas od formWrap+1,2 H przez 1,25 H (telefon od +0,9 H przez 1,1 H). Wygaszanie od formWrap+2,5 H do „dół kontaktu przy dole” (tylko desktop) |
| Stopka | 350svh, margin −160svh (telefon −50svh) | Jedna oś przewijana od „góra przy górze” do „dół przy dole”, zmierzona klatka po klatce w Playwright (pozycja w ekranach od góry stopki): litery ruszają od .2, pierwsza gotowa przy .6, każda następna ok. .03 później; copyright .35–.75, social .42–1.5, tagi .5–1.6, e-mail 1.0–1.4, potem nic do 2.5. Jednostka osi = 1,2 ekranu, więc oś ustalona na 2,08 (litera .69 co .025, linie .35). Dawne „1,1 s co .035” dawało litery 2× za wolne, copyright przy .25, social przy .3+i/10, tagi na środku przy .2 (quart in-out, co .15), e-mail przy .75. **Nic ze stopki nie pojawia się, zanim formularz zgaśnie** |

## Telefon i tablet (do 1024 px; zmierzone w oryginale przy 375×812, 1rem = 14,5 px)

| Element | Oryginał (i u nas) |
|---|---|
| Nagłówek | Padding 1,25rem; przycisk 2,5rem z obwódką o kryciu .2; linia pod rzędem logo przez całą szerokość, krycie .2, rysuje się od lewej (1 s, od 600 px 1,5 s, opóźnienie .5 s); przycisk wpada z góry z obrotem −10° (1 s quart out) |
| Menu | Strona gaśnie (.35 s), tło → `#DBDAD5` (.6 s); czarna scena ze spiralą kurczy się z całego ekranu do ramki pod nagłówkiem (.6 s quart in-out, rogi 4 px); biała karta z linkami odsłania się od góry (.65 s od .35 s); linki co 1/8 s od .45 s (napis wjeżdża, linia rośnie, czarne kółko ze strzałką się otwiera); adres na dole; zamykanie to odwrócenie 1,25× |
| Intro | Tytuł, okno i tekst wyśrodkowane w pionie między nagłówkiem a paskami; okno 15rem (tablet 20rem), proporcja 260/160, marginesy 2,44/4,61 svh; tekst 16,25rem, .9375rem, wyjustowany z ostatnią linią, wcięcie 4,75em i 1,35em po pierwszym słowie. 4 paski (1 px, .25, .5, 2,5rem; odstępy 1,1875/1/.75rem); w oryginale 3,5rem nad dołem, u nas przy samym dole (decyzja Grzegorza); wjeżdżają od najniższego, zatrzymane na 75% |
| Intro, przewijanie | Krawędzie okna otwierają się przez 75% zakresu (quad out), rogi znikają w ostatnich 25%; dociąganie jak w hero oryginału (tylko mysz/gładzik): >10%, prędkość <50 px/klatkę → do końca w `min(.25+|v/50−1|+|p−1|, 1,25)` s |
| Manifest | Tekst 2,25rem (tablet 2,875rem), interlinia 1, wyjustowany, wcięcie 15rem, góra na 20% ekranu; tylko 4 miniatury po 5rem (tablet 8), dół 5,5 svh |
| „Wybrane realizacje”, „Nagrody” | Bez przypiętego toru: etykieta z lewej, tytuł z prawej (1,375rem, max 12,125rem; tablet 1,5625rem/1,16, max 18,75rem); odtwarzane raz po wejściu na ekran, 1,75× szybciej (etykieta z 3rem w prawo, tytuł z 3rem w lewo). Odstęp nad nagłówkiem i pod nim 6,25rem |
| Karty | Wszystkie w ramce 374/464, tytuł 1,375rem; tagi schowane (pokazują się tylko po najechaniu, czyli na desktopie) |
| Lista projektów | Wiersz 1,875rem góra/dół, tytuł .9375rem, rok w mono .625rem po prawej; rozwinięcie: tekst i link do prawej. Przewinięcie do wiersza tylko wtedy, gdy lista jest na ekranie |
| O nas | Środkowe zdjęcie 339/508; tytuł 4rem łamany między słowami (wiersze to rzędy słów z odstępem .625rem); kolor strony kończy przejście, gdy góra sekcji jest 30% nad ekranem |
| Nagrody | Tylko pierwsza kolumna plakatów (padding 2,3125rem, odstęp 2,5rem; tablet 30rem), sekcja 12,5rem pod klientami; każda nazwa odtwarza się sama po wejściu na ekran |
| Kontakt | Napis 7,5rem (tablet 12,5rem). Formularz rusza, gdy ogon napisu jest 42% od lewej, i kończy wjazd przed końcem toru formularza (`tkMob()`) |
| Stopka | Lista social po prawej na 77% wysokości głowy (5,25rem, tablet 7,5rem); copyright, tagi i adres jeden pod drugim na środku (.609rem, tablet .625rem) |


## Mechanizmy prowadzenia przewijania (z kodu cappen)
- **Automatyczne przewijanie** (hero, klienci). Gdy przewijasz w dół, postęp sekcji jest powyżej progu (0,1 albo 0,15), a prędkość Lenisa poniżej 50 px na klatkę, strona sama dojeżdża do końca sekcji.
  - Czas u klientów: `min(0,5 + |v/50 − 1| + |p − 1|, 1,5) s`; w hero: `min(0,25 + |v/50 − 1| + |p − 1|, 1,25) s`, na telefonie ×0,75.
  - Krzywa: quad in-out, gdy v < 25; quad out, gdy szybciej (wtedy przejmuje ruch bez zatrzymania).
  - Przewijanie jest blokowane na czas jazdy (`lock:true`).
- **Dociąganie po zatrzymaniu** (power1.inOut):

  | Miejsce | Warunek | Kierunek | Czas |
  |---|---|---|---|
  | Wejście formularza | > 10% | do końca | 1,75 s |
  | Wygaszanie formularza | < 80% | z powrotem do pełnego formularza | 1,75 s |
  | Stopka | > 10% | do końca strony | 2 s |
  | Manifest w oryginale, początek | > 20% | do końca | 2,5 s |
  | Manifest w oryginale, koniec | < 50% | z powrotem | 2 s |

  U nas działa to na zdarzeniu `scroll` Lenisa: 180 ms po zatrzymaniu, tylko gdy nic nie jedzie automatycznie (`window.__autoScrolling`), z zabezpieczeniem czasowym na zdjęcie tej flagi. Wszystko to działa tylko z myszą lub gładzikiem (`carry = !coarse`); na ekranach dotykowych przewijanie jest w pełni natywne (decyzja z 9.10.2026, w oryginale działa też na telefonie).

