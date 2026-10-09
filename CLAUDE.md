# Wir Studio: studium animacji i przewodnik budowania stron z ruchem

Ten plik czyta Claude na początku każdej sesji w tym repozytorium. Jest też notatką dla Grzegorza: jak budujemy takie strony i co sprawia, że wyglądają profesjonalnie.
Stan na 9.10.2026, ostatnie zmiany: wersja na telefon zmierzona w oryginale (375×812) i przeniesiona sekcja po sekcji, menu na telefon jak w oryginale, wspólna jednostka `--r`.

---

## 1. Czym jest ten projekt

- **Cel:** nauka budowania stron z dużą ilością animacji na przykładzie nagradzanego studia (cappen.com). Odtwarzamy **technikę i timing**, a nie treść.
- **Wir Studio** to fikcyjna marka. Teksty są po polsku i nasze, grafiki generowane w przeglądarce, a klienci i nagrody zmyśleni.
- **Bez prawdziwych marek, logo i tekstów** z oryginału. Formularz kontaktowy niczego nie wysyła.
- **Wierność:** piksel w piksel nie jest wymagany, ale **czasy, kolejność i styl ruchu** mają się zgadzać z oryginałem.
- **Repo** jest publiczne i ma GitHub Pages (`https://grzegczerw96.github.io/wir-studium/`). Usunie je Grzegorz, Claude nigdy tego nie robi.
- **Wersja w czacie** to artefakt „Wir Studio”: https://claude.ai/artifact/4yg4BkHAu3zKmq4fjC6dWC (ta sama strona bez nagłówka `<head>`).

## 2. Jak Grzegorz lubi pracować

- **„Zmierz w oryginale”.** Opieramy się wyłącznie na tym, co da się zaobserwować lub odczytać z kodu oryginału. Opis Grzegorza bywa nieprecyzyjny i sam to zaznacza, a liczy się źródło.
- **Kod oryginału** (`/wp-content/themes/cappen/js/main.js`) to najlepsze źródło liczb. Filmy Grzegorza pokazują to, czego kod nie mówi wprost, np. kolejność warstw albo to, co faktycznie widać.
- **Jedna sekcja na raz.** Uwagi przychodzą ponumerowane („* …”). Każdą trzeba odhaczyć w odpowiedzi.
- **Najważniejsza jest czytelność.** Tekst nigdy nie może stać na tle, na którym go nie widać, ani nachodzić na inny tekst.
- **Odpowiedzi po polsku**, konkretne. Najpierw wynik, potem co zmieniono i dlaczego, a na końcu czego nie dało się sprawdzić.
- **Zatwierdzone odstępstwa od oryginału** (nie „naprawiać” ich z powrotem):
  - lista projektów zostaje dłużej na czarnym tle (przejście w biel startuje, gdy góra „O nas” jest na 55% ekranu, a nie przy dolnej krawędzi);
  - w kartach realizacji nie ma wybrzuszania obrazu po najechaniu ani wypływającego tekstu, tylko płynięcie obrazu z tekstem przy przewijaniu;
  - formularz kontaktowy wjeżdża później niż w cappen, dopiero gdy wielki napis prawie zniknął;
  - spirala przed kontaktem zaczyna się pojawiać od 70% wysokości ekranu (nasza warstwa spirali leży nad białą sekcją);
  - brak kursora „DISCOVER” i brak dociągania w manifeście.
- **Nasze dodatki, których oryginał nie ma** (zostawione celowo, do decyzji Grzegorza):
  - nagłówek chowa się przy przewijaniu w dół, bo inaczej tekst sekcji przejeżdża pod logo i przyciskiem;
  - na telefonie formularz kontaktowy startuje od położenia ogona wielkiego napisu (patrz §5), a nie od stałego progu; resztka napisu gaśnie tuż przed pierwszą ramką.
- **Zmiany po uwagach Grzegorza z 9.10.2026** (odstępstwa od oryginału wynikające z jego uwag; nie cofać bez pytania):
  - paski w intro na telefonie przylegają do dolnej krawędzi (w oryginale jest pod nimi 3,5rem bieli);
  - na ekranach dotykowych strona sama nie przewija (bez dociągania w intro i u klientów, bez przyciągania formularza i stopki), bo walczy to z palcem i pędem;
  - tytuł stopki składa się szybciej niż w oryginale (litera .5 s, co .018, gotowy w połowie toru);
  - „Kontakt” w menu prowadzi do gotowego formularza, a nie na górę sekcji (tam jest szare przejście koloru).
- **Fonty jak w oryginale:**
  - Inter Tight w roli Helvetica Now Display;
  - Instrument Serif w roli kroju szeryfowego;
  - JetBrains Mono na drobne etykiety;
  - szare nagłówki pomocnicze: `#989a96`.

## 3. Sposób pracy (pętla)

1. **Zmierz w oryginale.** W przeglądarce aplikacji Claude otwórz `https://cappen.com/`, pobierz `main.js` przez `fetch()` w konsoli strony i szukaj po nazwach klas sekcji (np. `about__clients`, `talk__form`, `footer__title`, `snap`, `scrollTo`). Geometrię mierz przez `getBoundingClientRect()` w oknie **1280×620** (jak na filmach Grzegorza).
   - Oryginał przewijaj przez `window.main.scroller.scrollTo(y,{immediate:true,force:true})`.
   - **Panel przeglądarki musi być widoczny.** Gdy jest schowany, `requestAnimationFrame` staje: preloader oryginału się nie kończy, a skrypty czekające na klatki wiszą.
2. **Zmień `index.html`.** Cała strona to jeden plik: HTML, CSS i JS razem.
3. **Sprawdź składnię:** wytnij skrypt inline i uruchom `node --check`.
4. **Test lokalny w Playwright** (Chromium, `--use-gl=swiftshader`), z kopią strony, w której biblioteki z CDN są podmienione na lokalne pliki. Na komputerze Grzegorza (Windows 10, Python 3.8): `pip install --target <scratchpad>/pw playwright==1.47.0`; pobrany Chromium Playwrighta nie startuje (błąd „konfiguracja równoczesna”), więc uruchamiaj zainstalowany Chrome przez `channel='chrome'`. W przeglądarce aplikacji system ma włączone ograniczanie ruchu: na naszej stronie ustaw `localStorage['wir-motion']='on'`. Testuj:
   - prawdziwymi ruchami kółka (`page.mouse.wheel`), a nie tylko skokami;
   - na desktopie 1280×620;
   - na telefonie 375×812 (`is_mobile`, `has_touch`);
   - brak przewijania w poziomie i brak błędów w konsoli.
   - **Filmy Grzegorza** (`.mp4`): brak ffmpeg; klatki wyciąga zainstalowany Chrome przez Playwright (strona z `<video>` ładowana jako plik, przewijanie `currentTime`, zrzut), a kilka klatek składa się w jeden arkusz.
5. **Commit** jako `grzegczerw96 <greg.wolwlod@gmail.com>`, z opisem po polsku. Push na `main`, GitHub Pages aktualizuje się po ok. 1 minucie. Przy sprawdzaniu dopisz do adresu `?v=<hash>`, żeby ominąć cache.
6. **Sprawdź na żywo** wersję z Pages, potem zaktualizuj artefakt.
7. **Po testach przywróć widok przeglądarki** do ustawienia „desktop”.

## 4. Technologia

- **GSAP 3.12.5 + ScrollTrigger** (cdnjs) do wszystkich animacji. Osie czasu są podpięte pod przewijanie (`scrub`).
- **Lenis 1.1.13** (`lerp: .1`) działa wszędzie, tak jak w oryginale: od 1025 px z płynnym kółkiem, poniżej z `smoothWheel:false` i `syncTouch:false`. Telefon przewija się natywnie; Lenis służy tam tylko do blokowania przewijania przy otwartym menu i skoków z menu. Instancja jest dostępna jako `window.__lenis`.
- **Three.js r149** do spirali 3D (`GLCoil`):
  - geometria: `TubeGeometry` po helisie, materiał `MeshPhysicalMaterial`, otoczenie PMREM („ciemne studio z paskami softboxów”);
  - przyciemnianie od góry: shader `onBeforeCompile` z uniformami `uY`/`uW`/`uAmt`;
  - API: `draw`, `size`, `setDark(v)`, `setShade(amt,y)`, `setPose(tilt,scale)`, `setPos(px,py)`, `kick`;
  - trzy instancje: intro i manifest (stała warstwa), okno klientów, kontakt i stopka (stała warstwa `.stage3`).
- **Obrazy z efektem cieczy** (`Fluid`): mały quad WebGL z kadrowaniem typu cover (`uScale .75`), paralaksą w pionie i soczewką na wejściu (5 → 0).
- **Jednostka płynna `--r`** (na `:root`) odpowiada `rem` oryginału:
  - `min(1.111vw, 2.556vh)` na desktopie;
  - `2.083vw` na tablecie (600–1024 px);
  - `3.865vw` na telefonie.
  - Margines strony `--gut` = `1.25 × --r`, jak `--global-padding` oryginału, na każdej szerokości. W px w JS: `remPx()`.
  - Progi jak w oryginale: telefon do 599 px, tablet 600–1024 px, desktop od 1025 px. Większość układu telefonu w oryginale dotyczy całego zakresu do 1024 px.
- **Wysokości sekcji** podajemy w `svh` („ile ekranów przewijania”), a sekcje przypinamy przez `position:sticky`, bez pinów GSAP.

## 5. Mapa strony i pomiary (desktop, H = wysokość ekranu)

| Sekcja | Długość | Co się dzieje (zmierzone w oryginale) |
|---|---|---|
| Intro | 200svh | Litery nagłówka wstają, okno ze spiralą rośnie do pełnego ekranu |
| Manifest | 647svh (telefon 501) | Oś 0→1: miniatury spadają kaskadą (.15–.50), słowa wstają w 3D (.25–.48), pauza (.48–.58), słowa się przewracają (.60–.80), miniatury zsuwają się (.72–.80); spirala w środku, przyciemniana od góry |
| Przejście „Wybrane realizacje” | 350svh + tor 385svh | Etykieta z prawej, tytuł z lewej (do +1,15 H, quad out), postój do +2,2 H, rozjazd i wygaszenie do +3,2 H; spirala gaśnie w cień od S0−0,95 do S0+2,25 H |
| Karty realizacji | – | Obraz wchodzi przy 1/5 na ekranie (skala .5→1, .65 s quad out, soczewka 5→0); duże karty zjeżdżają o 30% wysokości przez 125% ekranu |
| Lista projektów | – | Wiersze rozwijają się w .6 s (quart in-out); pasek najechania rośnie od środka; na telefonie pierwszy wiersz otwiera się sam |
| O nas | – | Strona czarna → `#fcfcfc` (power1.inOut), z powrotem do czerni od „dół na 115%” do „dół na −45%”; tytuł litera po literze (.9 s quart out, co .035 s); linie tekstu .5 s quad in-out, co .1 s |
| Klienci | 350svh, margin −100svh | Od „góra przy górze” do „koniec − 0,25 H”: okno otwiera się od środka (`--mask` 49,5%→0, quart in-out), spirala wychodzi z cienia, skala .5→1, przechył 45°→90°. Po 15% wolne przewijanie w dół jest **dociągane do końca** (patrz §6). Przy 70% wchodzą tytuł i nazwy. **Wyjście:** okno ze spiralą odjeżdża w górę w pełnym kryciu, a słowa gasną, gdy okno jest od 5% do 35% swojej wysokości nad górną krawędzią |
| Nagrody | plakaty 400svh, lista 250svh | Kolumny plakatów przesuwane zmiennymi `--progress`/`--scale`/`--spacing`; pary nazw na liście rozpisane co 1/6 osi |
| Kontakt: tytuł | 500svh, margin −30svh | Wielki napis przesuwa się z prawej krawędzi do całkowitego zniknięcia z lewej (liniowo) |
| Kontakt: formularz | 500svh (telefon 300), margin −250svh | Trzy ramki wjeżdżają z lewej (`--start` 1→0, quad in-out, co .1, scrub .5): u nas od formWrap+1,2 H przez 1,25 H (telefon od +0,9 H przez 1,1 H). Wygaszanie od formWrap+2,5 H do „dół kontaktu przy dole” (tylko desktop) |
| Stopka | 350svh, margin −160svh (telefon −50svh) | Jedna oś przewijana od „góra przy górze” do „dół przy dole”: litery tytułu (oryginał 1,1 s quart in-out, co .035; u nas szybciej: .5 s, co .018), copyright przy .25, social przy .3+i/10, tagi na środku przy .2 (quart in-out, co .15), e-mail przy .75. **Nic ze stopki nie pojawia się, zanim formularz zgaśnie** |

### Telefon i tablet (do 1024 px; zmierzone w oryginale przy 375×812, 1rem = 14,5 px)

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

## 6. Jak budować profesjonalne strony z ruchem (przewodnik)

### 6.1 Zasady, które robią różnicę
1. **Najpierw skala i proporcje, dopiero potem ruch.** Złe rozmiary psują stronę bardziej niż słaba animacja. Tekst ma swoje proporcje, np. manifest ma ok. 3,2% szerokości ekranu i mieści się w 2 liniach.
2. **Jeden motyw prowadzący.** Jedna bryła (spirala), jeden akcent kolorystyczny i spójny zestaw krzywych ruchu: quad i quart, in-out albo out.
3. **Rytm z pauzami.** Treść musi chwilę postać, zanim zniknie. Ruch rozkłada się na kilka ekranów przewijania.
4. **Ciągłość.** Nic się nie podmienia między stanami. To, co rośnie, to ten sam obiekt, a jedna bryła przechodzi przez wiele sekcji na stałej warstwie.
5. **Fale zamiast kolejki.** Wiele elementów rusza się naraz z małym przesunięciem (.035 s między literami, .1 s między liniami).
6. **Warstwy nie walczą.** Następna treść pojawia się dopiero, gdy poprzednia zniknęła, jak formularz i stopka. Tekst nigdy nie stoi na tle bez kontrastu.
7. **Strona prowadzi użytkownika.** Dociąganie i automatyczne przewijanie sprawiają, że nie da się „utknąć” w połowie przejścia (patrz 6.3).
8. **60 kl./s także na telefonie.** Rysujemy tylko to, co widać (IntersectionObserver), na dotyku stosujemy lżejsze efekty i natywne przewijanie.
9. **Wersja bez animacji też wygląda dobrze** (`prefers-reduced-motion`, klasa `html.motion`).
10. **Detale:** stany najechania, widoczny focus, Esc zamyka menu, linki działają z klawiatury.

### 6.2 Słownik ruchu (wartości z oryginału)
- **Litery dużych tytułów:** `rotateX -90° → 0`, `scaleY 1.5 → 1`, 1,1 s quart in-out (albo 0,9 s quart out w wersji „szybkiej”), co 0,035 s; perspektywa ok. 31,25 rem.
- **Linie tekstu:** te same obroty, 0,5 s quad in-out, co 0,1 s na linię; perspektywa równa szerokości elementu.
- **Obracanie w 3D bez rozjechania:** `translateZ(-1em) rotateX(var(--rx)) scaleY(var(--sy)) translateZ(1em)` i `backface-visibility:hidden`.
- **Wejście obrazu:** skala 0,5 → 1 i krycie w 0,65 s quad out, soczewka 5 → 0 w 0,75 s.
- **Okno otwierane od środka:** `clip-path`/maska z 50% do 0%, quart in-out.

### 6.3 Mechanizmy prowadzenia przewijania (z kodu cappen)
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

### 6.4 Wzorce kodu
- **Oś czasu znormalizowana do 1:** `tl.set({}, {}, 1)`. Pozycje elementów zapisujemy wtedy w procentach długości sekcji, a nie w sekundach.
- **Ruch przez zmienne CSS** (`--p`, `--rx`, `--sy`, `--mask`, `--start`, `--progress`). CSS liczy transformację, a GSAP przesuwa jedną liczbę.
- **Odczyty w `gsap.ticker`**, a nie w `onUpdate`. `ScrollTrigger.refresh()` potrafi pominąć callbacki, więc stan liczony co klatkę nigdy się nie „zawiesza”.
- **Kolor strony liczony co klatkę z żywego położenia sekcji** (`getBoundingClientRect`), a nie dwoma tweenami na jednej właściwości, bo te nadpisywały się przy odświeżeniu.
- **Pozycje triggerów się starzeją**, gdy coś powyżej zmienia wysokość (np. rozwinięty wiersz listy). Po takiej zmianie wywołujemy `ScrollTrigger.refresh()`, a rzeczy krytyczne liczymy z żywego układu.
- **Warstwy bez z-index:** `.talk` i `.footer` nie tworzą własnego kontekstu warstw, a ich treść ma z-index 5 nad stałą warstwą spirali (z-index 4).
- **Polskie znaki w wielkich tytułach** potrzebują interlinii ok. 0,9 zamiast 0,8, bo inaczej kropka nad „Ż” i ogonki zlewają się z linią wyżej.

## 7. Lekcje (objaw → przyczyna → rozwiązanie)

| Objaw | Przyczyna | Rozwiązanie |
|---|---|---|
| Lista projektów „zniknęła” (biały tekst na białym) | Dwa tweeny `fromTo` na `--room`; przy odświeżeniu późniejszy wpisał swój biały start | Jeden ticker liczący kolor z położenia sekcji |
| Spirala nie wraca po szybkim skoku w górę | Krycie płótna zostało na 0 z końca przejścia | `setDark(0)` w tickerze przywraca krycie i rozmiar |
| Napis stopki nachodzi na formularz | Tytuł stopki odpalany jednorazowo przy 60% ekranu | Oś stopki przewijana od jej górnej krawędzi (jak w oryginale) |
| Dociąganie klientów „waha się” na starcie | Prędkość liczona w px/s zamiast w px/klatkę Lenisa | `lenis.velocity` i progi 50/25 jak w oryginale |
| Okno klientów blednie w całości przy wyjściu | Krycie ustawiane na całym wrapperze | Gasną tylko słowa, okno odjeżdża w pełnym kryciu |
| Tło szarzeje pod listą na telefonie | Pozycje triggerów sprzed automatycznego rozwinięcia wiersza | Kolor z żywego `getBoundingClientRect` |
| Na telefonie tytuł stopki nachodzi na formularz | Wysokości z desktopu | Wartości z oryginału dla <1025 px: formularz 300svh, stopka −50svh |
| Słowa tytułu klientów rozjechane | Flex na kontenerze rozpychał słowa | Tekst w jednym `span` (`#clTt`) |
| Kropka nad „Ż” w linii wyżej | Interlinia 0,8 z angielskich wersalików | 0,9 dla polskich tytułów |
| Teksty po bokach spirali „podjeżdżają” przy gaśnięciu | Sticky puszczał za wcześnie | Osobny tor `.wi-track` 385svh |
| Skrypty w panelu wiszą, preloader oryginału stoi | Schowany panel przeglądarki zatrzymuje `requestAnimationFrame` | Panel na wierzchu przy pomiarach, nasza strona testowana w Playwright |
| Przejścia CSS „nie działają” w pomiarach | Ten sam powód (schowany panel) | Czytać wartości inline, nie obliczone style |
| Biały pasek 8 px wokół czarnych sekcji (Pages) | Brak `body{margin:0}` | Reset marginesu |
| Okno intro 20–40 px niżej niż jego miejsce, zasłania tekst | Font dochodzi później i zmienia wysokość grupy; `ScrollTrigger.refresh()` w spoczynku nie przerysowuje osi z `scrub` | `ResizeObserver` na tytule i tekście; w `onRefresh`: `invalidate()` i drobne przesunięcie `progress` |
| Litery tekstu intro w pionie, jedna pod drugą | `text-indent` dziedziczą elementy `inline-block` (słowa, litery) | `text-indent:0` na `.wd` i `.c` |
| Automatycznie rozwinięty wiersz listy cofa stronę | Przewijanie do wiersza bez sprawdzenia, czy lista jest widoczna (po włączeniu Lenisa na telefonie) | Przewijać tylko przy liście na ekranie i bez innej jazdy, jak w oryginale |
| Komentarz `//` na końcu linii zabił kod | Jedna linia zawierała dwie instrukcje | Komentarze w osobnej linii |
| Telefon „muli” przy przewijaniu | Pasek adresu wywołuje `resize` (zmienia się tylko wysokość), a `relayout` robił `ScrollTrigger.refresh()` w trakcie przewijania; do tego automatyczna jazda z `lock` walczyła z palcem | Na dotyku `resize` tylko przy zmianie szerokości; bez automatycznej jazdy na dotyku |
| Biały pasek pod intro na prawdziwym telefonie | Przypięte ekrany w `svh`, a po schowaniu paska adresu ekran jest wyższy | `height:100dvh` (z `svh` jako zapasem) dla intro, manifestu i stopki |
| Menu → Kontakt: szare tło i ciemna spirala | Skok na górę sekcji wypada w środku przejścia koloru strony | Skok do końca wjazdu formularza (`window.__contactY`) |
| Spirala kontaktu wystaje nad sekcję | Warstwa spirali jest stała i pokazuje się od 70% ekranu | `clip-path` warstwy przycięty do górnej krawędzi sekcji kontaktu |
| Menu na desktopie ucina „Kontakt” przy 620 px | Rozmiar liter tylko od szerokości | `min(9,5vw, (100svh − 230px)/4,7)` |

## 8. Lista kontrolna przed oddaniem sekcji

- [ ] Liczby (długość sekcji, progi, czasy, krzywe) wzięte z kodu oryginału albo zmierzone, nie zgadnięte.
- [ ] Przewinięte prawdziwym kółkiem: wolno, szybko, z zatrzymaniem w połowie przejścia, w górę i z powrotem.
- [ ] Nic nie nachodzi na tekst; kontrast w każdej klatce przejścia kolorów.
- [ ] Telefon 375×812: brak przewijania w poziomie, proporcje z oryginału dla <1025 px, brak nakładania warstw.
- [ ] 60 kl./s (średnio ok. 16,7 ms na klatkę), zero błędów w konsoli.
- [ ] Zatwierdzone odstępstwa (§2) nienaruszone.
- [ ] Commit, push, sprawdzenie na Pages z `?v=`, aktualizacja artefaktu, przywrócenie widoku „desktop”.
