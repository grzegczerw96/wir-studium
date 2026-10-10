# Wir Studio: studium animacji i przewodnik budowania stron z ruchem

Ten plik czyta Claude na początku każdej sesji w tym repozytorium. Jest też notatką dla Grzegorza: jak budujemy takie strony i co sprawia, że wyglądają profesjonalnie.
Stan na 10.10.2026, ostatnie zmiany: start bez mignięcia innego układu (strona pusta do gotowości, jak `root.hide` w oryginale); próby nowego hero w `lab/hero.html`.

---

## 1. Czym jest ten projekt

- **Cel:** nauka budowania stron z dużą ilością animacji na przykładzie nagradzanego studia (cappen.com). Odtwarzamy **technikę i timing**, a nie treść.
- **Wir Studio** to fikcyjna marka. Teksty są po polsku i nasze, grafiki generowane w przeglądarce, a klienci i nagrody zmyśleni.
- **Bez prawdziwych marek, logo i tekstów** z oryginału. Formularz kontaktowy niczego nie wysyła.
- **Wierność:** piksel w piksel nie jest wymagany, ale **czasy, kolejność i styl ruchu** mają się zgadzać z oryginałem.
- **Repo** jest publiczne i ma GitHub Pages (`https://grzegczerw96.github.io/wir-studium/`). Usunie je Grzegorz, Claude nigdy tego nie robi.
- **Wersja w czacie** to artefakt „Wir Studio”: https://claude.ai/artifact/4yg4BkHAu3zKmq4fjC6dWC (ta sama strona bez nagłówka `<head>`: usunąć linie 1–5, `</head>`, `<body>`, `</body>`, `</html>`).
- **Słowniczek (żeby się nie mylić):** *preloader* = ekran ładowania oryginału („HUMAN THINKERS / DIGITAL MAKERS”, zmieniające się obrazki, potem odlatują); *hero* = pierwszy ekran z wielkim tytułem, oknem i notką; *wejście hero* = animacja pojawienia się po załadowaniu; *przewijanie intro* = okno rośnie do pełnego ekranu (200svh). Grzegorz mówi „intro” o całym początku do pojawienia się hero, więc dopytać, o którą część chodzi.
- **Strony próbne** (warianty do wyboru, przełącznik 1–4 / A–D) leżą w `lab/` i są na Pages, np. `https://grzegczerw96.github.io/wir-studium/lab/hero.html`.

## 2. Jak Grzegorz lubi pracować

- **„Zmierz w oryginale”.** Opieramy się wyłącznie na tym, co da się zaobserwować lub odczytać z kodu oryginału. Opis Grzegorza bywa nieprecyzyjny i sam to zaznacza, a liczy się źródło.
- **Kod oryginału** (`/wp-content/themes/cappen/js/main.js`) to najlepsze źródło liczb. Filmy Grzegorza pokazują to, czego kod nie mówi wprost, np. kolejność warstw albo to, co faktycznie widać.
- **Jedna sekcja na raz.** Uwagi przychodzą ponumerowane („* …”). Każdą trzeba odhaczyć w odpowiedzi.
- **Najważniejsza jest czytelność.** Tekst nigdy nie może stać na tle, na którym go nie widać, ani nachodzić na inny tekst.
- **Reguły to pomoc, nie gorset** (Grzegorz, 10.10.2026). Jeśli jest sposób szybszy albo dokładniejszy, którego nie ma w tym pliku (nowe narzędzie, program do zainstalowania, agent, polecenie), zaproponuj go i użyj. Technologia się zmienia; cel to ułatwiać pracę i trafiać w efekt bez jego ingerencji. Zasady czytelności i wierności oryginałowi zostają.
- **Odpowiedzi po polsku**, konkretne. Najpierw wynik, potem co zmieniono i dlaczego, a na końcu czego nie dało się sprawdzić.
- **Zatwierdzone odstępstwa od oryginału** (nie „naprawiać” ich z powrotem):
  - lista projektów zostaje dłużej na czarnym tle (przejście w biel startuje, gdy góra „O nas” jest na 55% ekranu, a nie przy dolnej krawędzi);
  - w kartach realizacji nie ma wybrzuszania obrazu po najechaniu ani wypływającego tekstu, tylko płynięcie obrazu z tekstem przy przewijaniu;
  - formularz kontaktowy wjeżdża później niż w cappen, dopiero gdy wielki napis prawie zniknął;
  - na telefonie tytuł stopki składa się szybciej niż w oryginale: oś stopki od góry stopki 10% nad ekranem przez jeden ekran (zamiast 2,5); litery ruszają przy ok. 0,3 ekranu, gdy formularz zszedł już z obszaru tytułu, całość gotowa przy ok. 0,6 (10.10.2026);
  - spirala przed kontaktem zaczyna się pojawiać od 45% wysokości ekranu, a nie od dolnej krawędzi (najpierw tło ma być ciemne);
  - powrót do czerni po nagrodach jest krótszy niż w oryginale: od ostatniej nazwy na 15% ekranu do góry kontaktu przy górze ekranu (telefon ok. 0,6 ekranu, desktop ok. 0,95), żeby lista schodziła na białym, a nie stała na szarym (10.10.2026);
  - brak kursora „DISCOVER” i brak dociągania w manifeście.
- **Nasze dodatki, których oryginał nie ma** (zostawione celowo, do decyzji Grzegorza):
  - nagłówek chowa się przy przewijaniu w dół, bo inaczej tekst sekcji przejeżdża pod logo i przyciskiem;
  - na telefonie formularz kontaktowy startuje od położenia ogona wielkiego napisu (patrz §5), a nie od stałego progu; resztka napisu gaśnie tuż przed pierwszą ramką.
- **Zmiany po uwagach Grzegorza z 9.10.2026** (odstępstwa od oryginału wynikające z jego uwag; nie cofać bez pytania):
  - paski w intro na telefonie przylegają do dolnej krawędzi (w oryginale jest pod nimi 3,5rem bieli);
  - na ekranach dotykowych strona sama nie przewija (bez dociągania w intro i u klientów, bez przyciągania formularza i stopki), bo walczy to z palcem i pędem;
  - „Kontakt” w menu prowadzi do gotowego formularza, a nie na górę sekcji (tam jest szare przejście koloru).
- **Uwagi Grzegorza z 10.10.2026 (hero, w trakcie):**
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
  - `lab/hero.html` ma tryb „przesuń”: Grzegorz sam przesuwa tytuł i notkę, przesunięcia (w rem) są w adresie (`&t=x,y&n=x,y`) i do skopiowania.
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
4. **Sprawdź jakość** metodą z §3a: po każdej zmianie poziom 1, po skończonej sekcji poziom 2, przed oddaniem całości poziom 3.
5. **Commit** jako `grzegczerw96 <greg.wolwlod@gmail.com>`, z opisem po polsku. Push na `main`, GitHub Pages aktualizuje się po ok. 1 minucie. Przy sprawdzaniu dopisz do adresu `?v=<hash>`, żeby ominąć cache.
6. **Sprawdź na żywo** wersję z Pages, potem zaktualizuj artefakt.
7. **Po testach przywróć widok przeglądarki** do ustawienia „desktop”.

## 3a. Kontrola jakości (metoda)

Narzędzia są w `tools/` (Python 3.8, uruchamiane przez `py -I`). Biblioteki leżą poza repo w `%LOCALAPPDATA%\wir-tools`:
- `pw/`: `py -m pip install --target %LOCALAPPDATA%\wir-tools\pw playwright==1.47.0 pillow==10.4.0`;
- `lib/`: lokalne kopie gsap 3.12.5, ScrollTrigger, lenis 1.1.13 i three r149 (pobrane z tych samych adresów CDN co strona);
- `out/`: zrzuty i raporty.

Pobrany Chromium Playwrighta nie startuje na tym Windowsie (błąd „konfiguracja równoczesna”), więc narzędzia uruchamiają zainstalowany Chrome (`channel='chrome'`). Gdy brakuje `wir-tools`, odtwarza się go powyższymi poleceniami.

**Zasada:** szukać błędów automatycznie i tanio, a oczami oglądać tylko to, co narzędzie zgłosi. Zrzuty ekranu są najdroższą częścią pracy, dlatego przegląd składa zgłoszone kadry w jeden arkusz (`out/audit_sheet_<urządzenie>.png`).

| Poziom | Kiedy | Co | Koszt |
|---|---|---|---|
| 1 | po każdej zmianie | `node --check` skryptu; pomiar zmienionego miejsca przez `tools/probe.py` (liczby, bez zrzutów); `tools/audit.py --section '#id'` (3 urządzenia: telefon, tablet, desktop) | ok. 1 min |
| 2 | po skończonej sekcji | `tools/audit.py --section '#id' --devices all`; na telefonie Grzegorza `tools/phone.py` z płynnością tej sekcji i zrzutami ekranu | kilka min |
| 3 | przed oddaniem całości | `tools/audit.py --devices all` (cała strona, 11 ekranów); `tools/phone.py tools/phone-sections.json` dwa razy (zimny i rozgrzany przejazd); porównanie z oryginałem przez `tools/probe.py` | ok. 20 min |

- **`tools/audit.py`:**
  - urządzenia: `quick` (domyślnie: 360×649, 768×1024, 1280×620), `phones` (320–412 px) albo `all` (11 rozmiarów, z telefonem w poziomie 844×390, tabletami do 1024×1366 i desktopami do 1920×1080);
  - zakres: `--section '#id'`, albo `--from` i `--to` w ekranach; `--src plik` sprawdza inną wersję strony;
  - co sprawdza: przewijanie w poziomie przez prawdziwy element, jasny pasek przy jednej krawędzi przy ciemnym kadrze (piksele), nachodzący tekst z różnych bloków, tekst ucięty przez krawędź ekranu, obrazy ucięte przez krawędź kontenera w środku ekranu;
  - na telefonach dodatkowo udaje schowanie paska adresu;
  - w intro sprawdza 5× gęściej, bo tam zmiany są szybkie.
- **Narzędzie sprawdzone na wersji z błędami:** na `0b79250` (`git show 0b79250:index.html`) znajduje oba błędy ze zrzutów Grzegorza z 10.10.2026 (prześwit przy 0,8 intro, przycięte kwadraty manifestu). Po każdej zmianie narzędzia trzeba je znowu sprawdzić na starej wersji z błędem.
- **Znane fałszywe alarmy:**
  - 4 px paska przewijania emulatora na tabletach (prawy margines okna intro);
  - biały margines strony pod oknem klientów;
  - nagłówek w trakcie chowania;
  - litery intro zasłonięte czarnym oknem.
- **Czego emulacja nie pokaże:** chowania paska adresu w Chrome na Androidzie (w emulacji zmienia się też `svh`) i płynności. To sprawdza tylko prawdziwy telefon.
- **`tools/paths.py` (reguły bez zrzutów):** w stronie działa rejestrator, który w każdej klatce zapisuje stan (krycie formularza, postęp liter stopki, położenie napisu kontaktu, kontrast tekstu do tła), a kółko przewija w dół, w górę i znowu w dół. Każdą klatkę sprawdzają reguły z CLAUDE.md, np. „litery stopki widoczne ⇒ formularz wygaszony”. Wyłapuje błędy, które wychodzą dopiero po zmianie kierunku albo przy szybkim przewijaniu, i jest tańsze niż zrzuty. Nowe zasady dopisuje się jako reguły w `RULES`.
- **`tools/center.py`:** czy spirala stoi na środku „O” w `lab/hero.html`, mierzone tylko z pikseli (obrys „O” z ciemnych przebiegów, bryła z jasnych pikseli), na 5 desktopach × gęstości 1/1,25/1,5 z prawdziwym paskiem przewijania i myszą w rogu, plus tablet i 2 telefony. Próg 1% szerokości „O” (cień metalu po prawej daje stałe ok. −0,8%). Sprawdzone na wersji z błędem: 15 z 15 desktopów źle.
- **Pasek przewijania w narzędziach:** Playwright domyślnie go ukrywa (`--hide-scrollbars`), a u Grzegorza (Windows, Chrome, gęstość 1,25) ma 15 px. `_env.launch(p, scrollbars=True)` go pokazuje. `audit.py` i `paths.py` jeszcze działają bez paska; przy przenoszeniu hero na stronę główną przestawić je na pasek.
- **`tools/probe.py`:** pomiar oryginału albo naszej strony w wybranych miejscach. W cappen przed pomiarem `window.main.scroller.stop()` (jego przyciąganie zwraca wtedy bieżącą pozycję), u nas przyciąganie wyłączone. Litery oryginału mają `--rotateX` w `style`, nasze `--rx`. Liczby porównuje się w ekranach od początku sekcji.
- **`tools/phone.py` na prawdziwym telefonie** (Samsung Galaxy M15 5G, Chrome, 360×649 z paskiem adresu, 705 bez niego, 90 Hz):
  - przygotowanie: kabel USB, debugowanie USB, `adb` z `Google.PlatformTools`; na telefonie otwarta nasza strona;
  - **dotykać tylko karty z naszą stroną**, inne karty to prywatne karty Grzegorza;
  - gest palca `Input.synthesizeScrollGesture` (z chowaniem paska adresu), zrzut całego ekranu przez `adb`, czasy klatek;
  - `--local` podaje telefonowi niewypchniętą wersję z tego komputera.
- **Szukanie szarpnięć na telefonie:** zwykła strona z samym tekstem daje na nim równe 11 ms, więc wszystko powyżej to nasz koszt. Mierzyć sekcjami, zimny i rozgrzany przejazd. Winowajcę zawężać wyłączaniem: `ScrollTrigger.getAll()[i].disable()` grupami, ukrywanie elementów. Oryginał na tym telefonie: 40–175 ms na klatkę.
- **Materiały od Grzegorza:** zrzuty ekranu z telefonu są w `/sdcard/DCIM/Screenshots` (`adb pull` tylko dzisiejszych z Chrome). Filmy (`.mp4`) rozkłada się na klatki przez `ffmpeg` (zainstalowany przez winget).
- **W przeglądarce aplikacji** system ma włączone ograniczanie ruchu: na naszej stronie trzeba ustawić `localStorage['wir-motion']='on'`.
- **Skrypty z wieloma odwróconymi apostrofami** (Markdown, JS) zapisuje się narzędziami do edycji plików, nie przez `bash -c "…"`: bash wykonuje tekst w odwróconych apostrofach jako polecenia.

### Na koniec: gotowość na wszystkich rozdzielczościach
Uzgodnione 10.10.2026: na razie budujemy i dopracowujemy sekcje, a pełna gotowość na wszystkie ekrany to osobny etap na końcu (poziom 3). Lista znanych spraw do tego etapu:
- **Telefon w poziomie (844×390):** brak układu na niskie ekrany. W intro okno nachodzi na paski i nie mieści się tekst, w manifeście tekst i kwadraty nachodzą na spiralę.
- **Okno klientów na telefonie:** kilka szarpnięć do ok. 90 ms przy otwieraniu (`clip-path` przerysowywany co klatkę).
- **Pierwszy przejazd po załadowaniu na telefonie:** manifest, okolice „O nas” i nagrody ok. 45 kl./s (rozgrzany: 90).
- **Safari/iPhone:** niesprawdzone.
- **Pasek przewijania na stronie głównej:** spirala kontaktu liczy środek jako `innerWidth/2` (`cX`), więc na desktopie z paskiem stoi ok. 7 px w prawo; przejrzeć wszystkie `innerWidth`/`innerHeight` według zasad z §6.4 i sprawdzać z paskiem.

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
| Preloader (oryginał) | – | Treść w `.root.hide` (`display:none`), tło i tekst `#fcfcfc`; preloader czeka na fonty i zasoby, potem `finishIntro()`: słowa gasną (.35/1.25/1.55 s), obrazki odlatują, po 1,5 s treść odsłonięta. U nas: bez preloadera, strona pusta do gotowości |
| Hero (oryginał) | – | Tytuł Helvetica Now Display Black 900, normalna szerokość, −.04em, interlinia .8, 4rem / 7,5rem / 8,75rem; desktop: wiersze od lewej, 2. i 3. wcięte o 1,94/1,93em, okno 1,8571em (260/160) w przerwie 1,97em ostatniego wiersza („FOR ▢ TODAY”), „O” w FOR to znak-ikona; telefon: wiersze wyśrodkowane, okno pod tytułem. Wejście: litery `rotateX −90→0`, `scaleY 1.5→1`, 1,1 s quart in-out co .035 s; notka liniami od .35 s. Przewijanie: okno quad out przez 75%, rogi w ostatnich 25%, spirala obraca się (X −45°→0, Z 9°→−180°, quart out) i skaluje do .75 (tablet .5), tytuł, notka i paski gasną w pierwszej połowie (`--o` 1→0, quad out) |
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
| Stopka | 350svh, margin −160svh (telefon −50svh) | Jedna oś przewijana od „góra przy górze” do „dół przy dole”, zmierzona klatka po klatce w Playwright (pozycja w ekranach od góry stopki): litery ruszają od .2, pierwsza gotowa przy .6, każda następna ok. .03 później; copyright .35–.75, social .42–1.5, tagi .5–1.6, e-mail 1.0–1.4, potem nic do 2.5. Jednostka osi = 1,2 ekranu, więc oś ustalona na 2,08 (litera .69 co .025, linie .35). Dawne „1,1 s co .035” dawało litery 2× za wolne, copyright przy .25, social przy .3+i/10, tagi na środku przy .2 (quart in-out, co .15), e-mail przy .75. **Nic ze stopki nie pojawia się, zanim formularz zgaśnie** |

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
- **Architektura odporna na rozmiar okna** (uzgodnione 10.10.2026, po spirali przesuniętej o 7 px przez pasek przewijania):
  1. Gdzie co stoi, decyduje tylko CSS: flex/grid, jednostki `--r` i `em`, rozmiary liczone z kroju. JS nie wpisuje pozycji w px.
  2. JS tylko czyta gotowe pudełka (`getBoundingClientRect`) i zawsze w układzie elementu, na którym rysuje (warstwa z `clip-path`, płótno spirali). Nigdy `innerWidth`/`innerHeight` jako „ekran”: liczą pasek przewijania (15 px na Windows), a na telefonie zmieniają się z paskiem adresu. Środek ekranu: `document.documentElement.clientWidth / 2`.
  3. Mierzyć od nowa, gdy coś się zmienia (`ResizeObserver` na elementach, doczytane fonty), nie tylko przy `resize` okna.
  4. Każde nowe położenie sprawdzać narzędziem na wielu szerokościach i gęstościach, z prawdziwym paskiem przewijania (`_env.launch(p, scrollbars=True)`, wzór: `tools/center.py`), a nie wzrokiem na jednym zrzucie.

### 6.5 Sposoby, które rodzą błędy (do sprawdzenia, gdy coś „przecina” albo szarpie)
1. **Ten sam element sterowany dwa razy.** Przejście CSS i GSAP na jednej właściwości, dwa tweeny na jednej zmiennej. Jedno źródło prawdy dla każdej wartości.
2. **Tween napisu złożonego** (`clip-path`, `transform` jako tekst). Przeglądarka skraca zapis i liczby się przesuwają. Tweenować liczby w obiekcie, a napis składać w `onUpdate`.
3. **Wartości policzone raz, a układ się zmienia** (fonty, pasek adresu, rozwinięty wiersz). Mierzyć na żywo albo przeliczać przy zmianie rozmiaru; po `refresh` w spoczynku wymusić przerysowanie.
4. **Animowanie właściwości układu** (`width`, `height`, `top`, zmienna na `<html>`). Przeliczają całą stronę. Lepiej `transform`, `opacity` i zmienne na samym elemencie.
5. **Duży element przesuwany bez własnej warstwy** (obraz z paralaksą, długi napis). Telefon przerysowuje go co klatkę. Dodać `will-change`.
6. **Opóźnienie `scrub` w jednym z dwóch elementów**, które muszą się mijać: przy szybkim przewijaniu jeden zostaje w tyle. Elementy zależne od siebie bez opóźnienia albo z tym samym.
7. **Jednostki ekranu na telefonie:** `svh`, `dvh` i `lvh` różnią się o pasek adresu. Stałe warstwy `lvh`, przypięte ekrany `svh`; `dvh` tylko tam, gdzie nic nie jest liczone z wysokości.
8. **Progi dobrane do jednego ekranu** (`min-height:600px`, rozmiary z desktopu na tablecie). Każdą stałą w px sprawdzić na 320 px i na 1024 px.

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
| Biały pasek na dole na prawdziwym telefonie | Po schowaniu paska adresu ekran jest o 56 px wyższy, a stała warstwa `inset:0` nie zawsze nadąża | Czarna scena i warstwa spirali kontaktu `height:100lvh`; spirala intro w `100dvh` |
| Przycięte kwadraty manifestu w połowie ekranu (telefon) | Manifest w `dvh` rósł przy chowaniu paska, kwadraty przyklejone do dołu zjeżdżały, a ich ukryta pozycja startowa była policzona wcześniej | Przypięte ekrany intro i manifestu zostają w `svh`; paski intro dosuwa `bottom:min(0px, 100svh − 100dvh)` |
| Mały telefon (568 px): przycięte kwadraty na końcu manifestu | `min-height:600px` przypiętych ekranów większe niż ekran | Minimum 600 px tylko od 1025 px |
| Tablet: prawe zdjęcie „O nas” ucięte przy krawędzi | Boczne zdjęcia w rozmiarze z desktopu (20rem), trzy razem 928 px przy 768 | Rozmiar oryginału dla tabletów: 12 × 8,25rem |
| Desktop: litery „Kręcimy” nad resztką formularza przy szybkim przewijaniu | Wygaszanie formularza z `scrub .5` zostawało w tyle | `scrub:true` i litery od .1 osi |
| „Kręcimy się” nad pełnym formularzem przy przewijaniu w tę i z powrotem | CSS `transition:opacity .35s` na formularzu, a GSAP zmienia krycie co klatkę: przejście goni wartość i formularz zostaje ok. 90% widoczny | Bez przejścia CSS na elementach sterowanych przez GSAP (`html.motion .tk-form{transition:none}`) |
| Blada spirala i napis „Pogadajmy” na szarym tle | Powrót do czerni liczony od dołu „O nas”, a nie od kontaktu: 0,8 ekranu za późno | Pomiar oryginału: ciemnienie od „góra kontaktu 1,4 ekranu pod górą ekranu” do „góra kontaktu przy górze ekranu”; po nagrodach 60svh odstępu |
| Pierwsza litera napisu kontaktu wystaje 18 px od początku | Start `100vw − gut` | Start `100vw` (jak w oryginale) |
| Biały pasek po prawej przy końcu otwierania okna | Tweenowany napis `clip-path`: przeglądarka skraca `inset(0px 0px 0px 0px round 4px)` do `inset(0px round 4px)` i GSAP wpisywał promień w prawy margines | Krawędzie i promień jako liczby w obiekcie, `clip-path` składany w `onUpdate` |
| Menu → Kontakt: szare tło i ciemna spirala | Skok na górę sekcji wypada w środku przejścia koloru strony | Skok do końca wjazdu formularza (`window.__contactY`) |
| Spirala kontaktu wystaje nad sekcję | Warstwa spirali jest stała i pokazuje się od 70% ekranu | `clip-path` warstwy przycięty do górnej krawędzi sekcji kontaktu |
| Menu na desktopie ucina „Kontakt” przy 620 px | Rozmiar liter tylko od szerokości | `min(9,5vw, (100svh − 230px)/4,7)` |
| Telefon: 22 ms na klatkę przy przewijaniu kart i listy | Kreski wierszy rosły przez `width` (układ strony w każdej klatce), obraz karty z paralaksą nie był osobną warstwą (przerysowanie) | Kreski przez `transform: scaleX`, obraz z `will-change:transform` → 11 ms |
| Telefon: kontakt 22 ms na klatkę | Napis 7,5rem (ok. 1500 px) przesuwany co klatkę bez własnej warstwy | `will-change:translate` → 11 ms |
| Telefon: duże koszty stylów przy zmianie koloru strony | Zmienna `--room` na `<html>` dziedziczy się do każdego elementu | Kolor ustawiany na 4 sekcjach |
| Po załadowaniu przez kilka sekund inny układ (czarny prostokąt na środku, grube paski, tekst w zastępczym foncie), potem przeskok | Klasa `motion` (od niej zależy układ) dodawana dopiero przez skrypt na końcu strony, który czeka na GSAP i Three z CDN; wejście startowało niezależnie od tego, czy coś widać | Mały skrypt w `<head>` ustala `motion` i `wait` przed pierwszym malowaniem; `html.wait .hd, main` ukryte; główny skrypt czeka na fonty pierwszego ekranu (max 2,5 s), mierzy, odsłania i dopiero wtedy gra oś `enter`. Awaryjnie CSS odsłania po 15 s. Sprawdzać nagraniem ładowania z wolną siecią (screencast CDP + `Network.emulateNetworkConditions`) |
| Spirala 7 px na prawo od środka „O” u Grzegorza, a w narzędziach na środku; „O” o 13 px węższe | Wycięcie okna liczone od `innerWidth`, który zawiera pasek przewijania (15 px), a warstwa z `clip-path` go nie zawiera; narzędzia ukrywały pasek, więc tego nie widziały | Wszystko w układzie warstwy (`stage.getBoundingClientRect()`), środek ekranu z `clientWidth`; testy z prawdziwym paskiem i gęstością 1,25 (`tools/center.py`) |
| Spirala „nie na środku” litery O, choć liczby się zgadzały | Ocena na oko: światło z lewej góry przesuwa jasną masę, a rozciągnięty pierścień 2D wygląda płasko | Mierzyć pikselami w obrębie elipsy (jasne piksele kontra obrys, wynik w px, `window.__o` w `lab/hero.html`); do oceny używać prawdziwej spirali 3D, nie uproszczonej |
| Telefon: szarpnięcie przy pierwszym pojawieniu się spirali | Kompilacja shaderów przy pierwszym rysowaniu; spirale rysowane także przy kryciu 0 | `renderer.compile` przy ładowaniu; rysowanie tylko widocznych (`coil.on`) |

## 8. Lista kontrolna przed oddaniem sekcji

- [ ] Liczby (długość sekcji, progi, czasy, krzywe) wzięte z kodu oryginału albo zmierzone, nie zgadnięte.
- [ ] Przewinięte prawdziwym kółkiem: wolno, szybko, z zatrzymaniem w połowie przejścia, w górę i z powrotem.
- [ ] Nic nie nachodzi na tekst; kontrast w każdej klatce przejścia kolorów.
- [ ] Telefon 375×812: brak przewijania w poziomie, proporcje z oryginału dla <1025 px, brak nakładania warstw.
- [ ] 60 kl./s (średnio ok. 16,7 ms na klatkę), zero błędów w konsoli.
- [ ] Zatwierdzone odstępstwa (§2) nienaruszone.
- [ ] Commit, push, sprawdzenie na Pages z `?v=`, aktualizacja artefaktu, przywrócenie widoku „desktop”.
