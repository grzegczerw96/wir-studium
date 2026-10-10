# Wir Studio: studium animacji i przewodnik budowania stron z ruchem

Ten plik czyta Claude na początku każdej sesji w tym repozytorium. Jest też notatką dla Grzegorza: jak budujemy takie strony i co sprawia, że wyglądają profesjonalnie.
Stan na 10.10.2026: plik odchudzony do zasad i pętli; pomiary, lekcje, hero i szczegóły narzędzi są w osobnych plikach (§0). Następne zadanie: przeniesienie nowego hero na stronę główną (§5).

---

## 0. Gdzie co jest (czytać w razie potrzeby, nie zawsze)

| Plik | Kiedy czytać |
|---|---|
| `wiedza/pomiary.md` | praca nad daną sekcją: liczby z oryginału (desktop, telefon, tablet), mechanizmy dociągania |
| `wiedza/lekcje.md` | szukanie błędu: ok. 50 objawów z przyczyną i rozwiązaniem |
| `wiedza/hero.md` | praca nad hero: co wybrane, co jest w labie, wszystkie uwagi Grzegorza |
| `wiedza/marka.md`, `inspiracje.md`, `katalog-ruchu.md` | przed propozycjami dla sekcji, którą projektujemy (a nie odtwarzamy); dopisywać do katalogu po każdej decyzji |
| `tools/README.md` | instalacja narzędzi, ich opcje, znane fałszywe alarmy |

## 1. Czym jest ten projekt

- **Cel:** nauka budowania stron z dużą ilością animacji na przykładzie nagradzanego studia (cappen.com). Odtwarzamy **technikę i timing**, a nie treść.
- **Wir Studio** to fikcyjna marka. Teksty są po polsku i nasze, grafiki generowane w przeglądarce, a klienci i nagrody zmyśleni.
- **Bez prawdziwych marek, logo i tekstów** z oryginału. Formularz kontaktowy niczego nie wysyła.
- **Wierność:** piksel w piksel nie jest wymagany, ale **czasy, kolejność i styl ruchu** mają się zgadzać z oryginałem.
- **Repo** jest publiczne i ma GitHub Pages (`https://grzegczerw96.github.io/wir-studium/`). Usunie je Grzegorz, Claude nigdy tego nie robi.
- **Wersja w czacie** to artefakt „Wir Studio”: https://claude.ai/artifact/4yg4BkHAu3zKmq4fjC6dWC (ta sama strona bez nagłówka `<head>`: usunąć linie 1–5, `</head>`, `<body>`, `</body>`, `</html>`). Aktualizowany tylko przy oddawaniu sekcji.
- **Strony próbne** (warianty do wyboru) leżą w `lab/` i są na Pages, np. `https://grzegczerw96.github.io/wir-studium/lab/hero.html`. `lab/hero.html` jest zamrożony jako pokaz wariantów.
- **Słowniczek:** *preloader* = ekran ładowania oryginału („HUMAN THINKERS / DIGITAL MAKERS”); *hero* = pierwszy ekran z wielkim tytułem, oknem i notką; *wejście hero* = animacja pojawienia się po załadowaniu; *przewijanie intro* = okno rośnie do pełnego ekranu (200svh). Grzegorz mówi „intro” o całym początku do pojawienia się hero, więc dopytać, o którą część chodzi.

## 2. Jak Grzegorz lubi pracować

- **Wzorcem jest oryginał, a nie ocena Claude.** Najpierw pomiar (`probe.py`), potem budowa, a sprawdzanie głównie jako porównanie z oryginałem. Opis Grzegorza bywa nieprecyzyjny i sam to zaznacza, a liczy się źródło.
- **Kod oryginału** (`/wp-content/themes/cappen/js/main.js`) to najlepsze źródło liczb. Filmy Grzegorza pokazują to, czego kod nie mówi wprost, np. kolejność warstw albo to, co faktycznie widać.
- **Automatycznie sprawdzamy tylko rzeczy obiektywne i widoczne dla człowieka:** nachodzenie, tekst za ekranem, przeskoki, przerwy, przycięcia, krawędzie warstw, rozmiary okna. Rzeczy smakowe (np. w którą stronę leci dym) ocenia Grzegorz; nie budować dla nich reguł.
- **Budżet sprawdzania:** po zmianie szybka kontrola (kilka minut, tylko narzędzia pasujące do zmiany, §3a); pełna kontrola raz, przed oddaniem sekcji. Pół godziny do godziny na samo sprawdzanie jednej sekcji to za dużo, chyba że sekcja ma dużo ruchu na różnych szerokościach.
- **Jedna sekcja na raz.** Uwagi przychodzą ponumerowane („* …”). Każdą trzeba odhaczyć w odpowiedzi.
- **Najważniejsza jest czytelność.** Tekst nigdy nie może stać na tle, na którym go nie widać, ani nachodzić na inny tekst.
- **Reguły to pomoc, nie gorset** (Grzegorz, 10.10.2026). Jeśli jest sposób szybszy albo dokładniejszy, którego nie ma w tym pliku (nowe narzędzie, program do zainstalowania, agent, polecenie), zaproponuj go i użyj. Zasady czytelności i wierności oryginałowi zostają.
- **Odpowiedzi po polsku**, konkretne. Najpierw wynik, potem co zmieniono i dlaczego, a na końcu czego nie dało się sprawdzić.
- **Zatwierdzone odstępstwa od oryginału** (nie „naprawiać” ich z powrotem):
  - lista projektów zostaje dłużej na czarnym tle (przejście w biel startuje, gdy góra „O nas” jest na 55% ekranu, a nie przy dolnej krawędzi);
  - w kartach realizacji nie ma wybrzuszania obrazu po najechaniu ani wypływającego tekstu, tylko płynięcie obrazu z tekstem przy przewijaniu;
  - formularz kontaktowy wjeżdża później niż w cappen, dopiero gdy wielki napis prawie zniknął;
  - na telefonie tytuł stopki składa się szybciej niż w oryginale: oś stopki od góry stopki 10% nad ekranem przez jeden ekran (zamiast 2,5); litery ruszają przy ok. 0,3 ekranu, gdy formularz zszedł już z obszaru tytułu, całość gotowa przy ok. 0,6 (10.10.2026);
  - spirala przed kontaktem zaczyna się pojawiać od 45% wysokości ekranu, a nie od dolnej krawędzi (najpierw tło ma być ciemne);
  - powrót do czerni po nagrodach jest krótszy niż w oryginale: od ostatniej nazwy na 15% ekranu do góry kontaktu przy górze ekranu (telefon ok. 0,6 ekranu, desktop ok. 0,95), żeby lista schodziła na białym, a nie stała na szarym (10.10.2026);
  - brak kursora „DISCOVER” i brak dociągania w manifeście;
  - paski w intro na telefonie przylegają do dolnej krawędzi (w oryginale jest pod nimi 3,5rem bieli; 9.10.2026);
  - na ekranach dotykowych strona sama nie przewija (bez dociągania w intro i u klientów, bez przyciągania formularza i stopki), bo walczy to z palcem i pędem (9.10.2026);
  - „Kontakt” w menu prowadzi do gotowego formularza, a nie na górę sekcji (tam jest szare przejście koloru; 9.10.2026);
  - nowe hero (układ, krój, wejście z dymem): świadomie inne niż w oryginale, szczegóły w `wiedza/hero.md`.
- **Nasze dodatki, których oryginał nie ma** (zostawione celowo, do decyzji Grzegorza):
  - nagłówek chowa się przy przewijaniu w dół, bo inaczej tekst sekcji przejeżdża pod logo i przyciskiem;
  - na telefonie formularz kontaktowy startuje od położenia ogona wielkiego napisu (`tkMob()`), a nie od stałego progu; resztka napisu gaśnie tuż przed pierwszą ramką.
- **Fonty jak w oryginale:** Inter Tight w roli Helvetica Now Display; Instrument Serif w roli kroju szeryfowego; JetBrains Mono na drobne etykiety; szare nagłówki pomocnicze `#989a96`.

## 3. Sposób pracy (pętla)

1. **Zmierz w oryginale.** W przeglądarce aplikacji Claude otwórz `https://cappen.com/`, pobierz `main.js` przez `fetch()` w konsoli strony i szukaj po nazwach klas sekcji (np. `about__clients`, `talk__form`, `footer__title`, `snap`, `scrollTo`). Geometrię mierz przez `getBoundingClientRect()` w oknie **1280×620** (jak na filmach Grzegorza), albo `tools/probe.py`. Wcześniejsze pomiary: `wiedza/pomiary.md`.
   - Oryginał przewijaj przez `window.main.scroller.scrollTo(y,{immediate:true,force:true})`.
   - **Panel przeglądarki musi być widoczny.** Gdy jest schowany, `requestAnimationFrame` staje: preloader oryginału się nie kończy, a skrypty czekające na klatki wiszą.
   - W przeglądarce aplikacji system ma włączone ograniczanie ruchu: na naszej stronie trzeba ustawić `localStorage['wir-motion']='on'`.
2. **Zmień `index.html`.** Cała strona to jeden plik: HTML, CSS i JS razem. Nowy i przenoszony kod pisać w zwykłych, krótkich liniach; starego kodu nie przeformatowywać hurtem (duży diff, ryzyko cichego błędu), porządkować tylko to, czego się dotyka.
3. **Sprawdź składnię:** wytnij skrypt inline i uruchom `node --check`.
4. **Sprawdź jakość** według §3a.
5. **Commit** jako `grzegczerw96 <greg.wolwlod@gmail.com>`, z opisem po polsku. Push na `main`, GitHub Pages aktualizuje się po ok. 1 minucie. Przy sprawdzaniu dopisz do adresu `?v=<hash>`, żeby ominąć cache.
6. **Sprawdź na żywo** wersję z Pages. Artefakt aktualizuj tylko przy oddawaniu sekcji.
7. **Po testach przywróć widok przeglądarki** do ustawienia „desktop”.

Drobne pułapki środowiska:
- Skrypty z wieloma odwróconymi apostrofami (Markdown, JS) zapisuje się narzędziami do edycji plików, nie przez `bash -c "…"`: bash wykonuje tekst w odwróconych apostrofach jako polecenia.
- Materiały od Grzegorza: zrzuty z telefonu w `/sdcard/DCIM/Screenshots` (`adb pull` tylko dzisiejszych z Chrome); filmy (`.mp4`) rozkłada się na klatki przez `ffmpeg`. Nagrania cudzych stron w `wiedza/media/` (poza repo).

## 3a. Kontrola jakości

Narzędzia są w `tools/` (Python 3.8, `py -I`, biblioteki w `%LOCALAPPDATA%\wir-tools`, instalacja i opcje w `tools/README.md`). **Zasada:** szukać błędów automatycznie i tanio, a oczami oglądać tylko to, co narzędzie zgłosi. Każdą nową regułę narzędzia najpierw sprawdzić na wersji z błędem.

**Które narzędzie przy czym** (nie wszystkie zawsze; dobierać do tego, co się zmienia):

| Co budujemy albo zmieniamy | Narzędzia |
|---|---|
| Liczby z oryginału, porównanie naszej sekcji z cappen | `probe.py` |
| Układ sekcji w spoczynku, różne ekrany, paski, przewijanie w poziomie, ucięty tekst | `audit.py` (`--section`) |
| Czy układ trzyma się na każdym rozmiarze okna (grupy elementów nie wchodzą na siebie, nic nie wychodzi za ekran) | `sizes.py` (178 rozmiarów 320–1920 × 500–1080; grupy w `--groups`; lab: `?still=1`) |
| Przejścia przy przewijaniu między sekcjami, reguły „A zgasło, zanim weszło B”, zmiana kierunku | `paths.py` (+ `audit.py` w kilku pozycjach) |
| Coś ma stać w czymś (bryła w „O”, okno na tekście) | `center.py` (z pikseli; dziś tylko lab) |
| Każdy ruch, w którym elementy mogą na siebie wejść (wejścia, przejścia) | `overlap.py` (pudełka co klatkę; dziś tylko lab) |
| Wejścia po załadowaniu, efekty z maską, filtrem lub WebGL: przeskoki, krawędzie warstw, kolejność, przerwy (stall), przycięcia (jank) | `motion.py` (piksele co klatkę; `?dbg=` w stronie) |
| Ciężkie efekty, płynność, pasek adresu | `phone.py` na prawdziwym telefonie (dotykać tylko karty z naszą stroną) |

| Poziom | Kiedy | Co | Koszt |
|---|---|---|---|
| 1 | po każdej zmianie | `node --check`; pomiar zmienionego miejsca (`probe.py`, liczby); narzędzia z tabeli pasujące do zmiany, na `quick` (telefon, tablet, desktop) | kilka min |
| 2 | przed oddaniem sekcji | `audit.py --section '#id' --devices all`; narzędzia ruchu z tabeli; `phone.py` z płynnością tej sekcji | do ok. 15 min |
| 3 | przed oddaniem całości | `audit.py --devices all` (11 ekranów); `phone.py tools/phone-sections.json` dwa razy (zimny i rozgrzany przejazd); porównanie z oryginałem | ok. 20 min |

- **Pasek przewijania:** Playwright domyślnie go ukrywa, a u Grzegorza (Windows, Chrome, gęstość 1,25) ma 15 px. Narzędzia do położeń uruchamiać z `_env.launch(p, scrollbars=True)`.
- **Czego emulacja nie pokaże:** chowania paska adresu w Chrome na Androidzie i płynności. To sprawdza tylko prawdziwy telefon (Samsung Galaxy M15 5G, 360×649 z paskiem adresu, 90 Hz).

## 4. Technologia

- **GSAP 3.12.5 + ScrollTrigger** (cdnjs) do wszystkich animacji. Osie czasu są podpięte pod przewijanie (`scrub`).
- **Lenis 1.1.13** (`lerp: .1`) działa wszędzie, tak jak w oryginale: od 1025 px z płynnym kółkiem, poniżej z `smoothWheel:false` i `syncTouch:false`. Telefon przewija się natywnie; Lenis służy tam tylko do blokowania przewijania przy otwartym menu i skoków z menu. Instancja: `window.__lenis`.
- **Three.js r149** do spirali 3D (`GLCoil`, na stronie głównej ma być jedna implementacja):
  - geometria: `TubeGeometry` po helisie, materiał `MeshPhysicalMaterial`, otoczenie PMREM („ciemne studio z paskami softboxów”);
  - przyciemnianie od góry: shader `onBeforeCompile` z uniformami `uY`/`uW`/`uAmt`;
  - API: `draw`, `size`, `setDark(v)`, `setShade(amt,y)`, `setPose(tilt,scale)`, `setPos(px,py)`, `kick`;
  - trzy instancje: intro i manifest (stała warstwa), okno klientów, kontakt i stopka (stała warstwa `.stage3`).
- **Obrazy z efektem cieczy** (`Fluid`): mały quad WebGL z kadrowaniem typu cover (`uScale .75`), paralaksą w pionie i soczewką na wejściu (5 → 0).
- **Jednostka płynna `--r`** (na `:root`) odpowiada `rem` oryginału: `min(1.111vw, 2.556vh)` na desktopie; `2.083vw` na tablecie (600–1024 px); `3.865vw` na telefonie. Margines `--gut` = `1.25 × --r`. W JS: `remPx()`. Progi jak w oryginale: telefon do 599 px, tablet 600–1024 px, desktop od 1025 px. **`--r` nie zmieniać globalnie** (ruszyłoby wszystkie zmierzone sekcje); ograniczenie wysokością stosować lokalnie (§6.3).
- **Wysokości sekcji** w `svh` („ile ekranów przewijania”), sekcje przypinane przez `position:sticky`, bez pinów GSAP.
- **Start strony:** mały skrypt w `<head>` ustala klasy `motion` i `wait` przed pierwszym malowaniem; strona pusta do gotowości (jak `root.hide` w oryginale).

## 5. Sekcje i zadania

| Sekcja | Stan | Co zostało |
|---|---|---|
| Nagłówek i menu | zbudowane wg pomiarów | etap końcowy |
| Hero / intro | **w trakcie**: na stronie stary układ; nowy wybrany w `lab/hero.html` | przeniesienie (zadanie 1) |
| Manifest | zbudowany wg pomiarów | pierwszy przejazd na telefonie ok. 45 kl./s |
| Wybrane realizacje (przejście) | zbudowane | etap końcowy |
| Karty realizacji | zbudowane | etap końcowy |
| Lista projektów | zbudowana | etap końcowy |
| O nas | zbudowane | pierwszy przejazd na telefonie ok. 45 kl./s |
| Klienci | zbudowani | telefon: szarpnięcia do ok. 90 ms przy otwieraniu okna (`clip-path` co klatkę) |
| Nagrody | zbudowane | pierwszy przejazd na telefonie ok. 45 kl./s |
| Kontakt (napis, formularz) | zbudowany | spirala kontaktu liczy środek z `innerWidth/2` (`cX`): z paskiem przewijania ok. 7 px w prawo (zadanie 2) |
| Stopka | zbudowana | etap końcowy |

**Zadania po kolei:**
1. **Przeniesienie hero na stronę główną** (`wiedza/hero.md`): układ 2, krój A, wejście C, tytuł d3, wyjście przez rozmycie; wersja 5 jako kandydat na telefony. Przy tym:
   - jedna implementacja `GLCoil` na stronie głównej (kopia w zamrożonym labie zostaje);
   - start zawsze na górze (`history.scrollRestoration='manual'`, `scrollTo(0,0)`), jak w oryginale i w labie;
   - `overlap.py` (i `center.py`) przepięte na stronę główną, z grupami podawanymi w wywołaniu, jak w `sizes.py`;
   - nowe narzędzie **porównania obok siebie**: zrzuty oryginału i naszej strony w tych samych miejscach sekcji ułożone w pary w jednym obrazku, plus wykres przebiegu kluczowych wartości (jasność tła, położenie tytułu) w funkcji przewijania. Tak znaleźliśmy przejście do czerni przesunięte o 0,8 ekranu: z liczb, nie z wrażenia. Grzegorz ocenia efekt, Claude dostaje dokładną różnicę.
2. **Przegląd `innerWidth`/`innerHeight` w `index.html`** (42 użycia: 17 szerokość, 25 wysokość) według §6.3: szerokość liczona z paskiem przewijania to błąd, wysokość bywa w porządku. Przejrzeć, a nie zamieniać hurtem.
3. **`audit.py` i `paths.py` z prawdziwym paskiem przewijania** (`scrollbars=True`).
4. **Etap końcowy: gotowość na wszystkich ekranach** (poziom 3, uzgodnione 10.10.2026):
   - telefon w poziomie (844×390): brak układu na niskie ekrany; w intro okno nachodzi na paski i nie mieści się tekst, w manifeście tekst i kwadraty nachodzą na spiralę;
   - płynność na telefonie (klienci, pierwszy przejazd);
   - Safari/iPhone: niesprawdzone.

## 6. Jak budować profesjonalne strony z ruchem (przewodnik)

### 6.1 Zasady, które robią różnicę
1. **Najpierw skala i proporcje, dopiero potem ruch.** Złe rozmiary psują stronę bardziej niż słaba animacja.
2. **Jeden motyw prowadzący.** Jedna bryła (spirala), jeden akcent kolorystyczny i spójny zestaw krzywych ruchu: quad i quart, in-out albo out.
3. **Rytm z pauzami.** Treść musi chwilę postać, zanim zniknie. Ruch rozkłada się na kilka ekranów przewijania.
4. **Ciągłość.** Nic się nie podmienia między stanami. To, co rośnie, to ten sam obiekt, a jedna bryła przechodzi przez wiele sekcji na stałej warstwie.
5. **Fale zamiast kolejki.** Wiele elementów rusza się naraz z małym przesunięciem (.035 s między literami, .1 s między liniami).
6. **Warstwy nie walczą.** Następna treść pojawia się dopiero, gdy poprzednia zniknęła. Tekst nigdy nie stoi na tle bez kontrastu.
7. **Strona prowadzi użytkownika.** Dociąganie i automatyczne przewijanie sprawiają, że nie da się „utknąć” w połowie przejścia (liczby: `wiedza/pomiary.md`). U nas tylko z myszą lub gładzikiem.
8. **60 kl./s także na telefonie.** Rysujemy tylko to, co widać (IntersectionObserver), na dotyku lżejsze efekty i natywne przewijanie.
9. **Wersja bez animacji też wygląda dobrze** (`prefers-reduced-motion`, klasa `html.motion`).
10. **Detale:** stany najechania, widoczny focus, Esc zamyka menu, linki działają z klawiatury.

### 6.2 Słownik ruchu (wartości z oryginału)
- **Litery dużych tytułów:** `rotateX -90° → 0`, `scaleY 1.5 → 1`, 1,1 s quart in-out (albo 0,9 s quart out w wersji „szybkiej”), co 0,035 s; perspektywa ok. 31,25 rem.
- **Linie tekstu:** te same obroty, 0,5 s quad in-out, co 0,1 s na linię; perspektywa równa szerokości elementu.
- **Obracanie w 3D bez rozjechania:** `translateZ(-1em) rotateX(var(--rx)) scaleY(var(--sy)) translateZ(1em)` i `backface-visibility:hidden`.
- **Wejście obrazu:** skala 0,5 → 1 i krycie w 0,65 s quad out, soczewka 5 → 0 w 0,75 s.
- **Okno otwierane od środka:** `clip-path`/maska z 50% do 0%, quart in-out.

### 6.3 Wzorce kodu
- **Oś czasu znormalizowana do 1:** `tl.set({}, {}, 1)`. Pozycje elementów w procentach długości sekcji, a nie w sekundach.
- **Ruch przez zmienne CSS** (`--p`, `--rx`, `--sy`, `--mask`, `--start`, `--progress`). CSS liczy transformację, a GSAP przesuwa jedną liczbę.
- **Odczyty w `gsap.ticker`**, a nie w `onUpdate`. `ScrollTrigger.refresh()` potrafi pominąć callbacki, więc stan liczony co klatkę nigdy się nie „zawiesza”.
- **Kolor strony liczony co klatkę z żywego położenia sekcji** (`getBoundingClientRect`), a nie dwoma tweenami na jednej właściwości.
- **Pozycje triggerów się starzeją**, gdy coś powyżej zmienia wysokość. Po takiej zmianie `ScrollTrigger.refresh()`, a rzeczy krytyczne liczymy z żywego układu.
- **Warstwy bez z-index:** `.talk` i `.footer` nie tworzą własnego kontekstu warstw, a ich treść ma z-index 5 nad stałą warstwą spirali (z-index 4).
- **Polskie znaki w wielkich tytułach** potrzebują interlinii ok. 0,9 zamiast 0,8 (kropka nad „Ż”, ogonki).
- **Architektura odporna na rozmiar okna** (uzgodnione 10.10.2026):
  1. Gdzie co stoi, decyduje tylko CSS: flex/grid, jednostki `--r` i `em`, rozmiary liczone z kroju. JS nie wpisuje pozycji w px.
  2. JS tylko czyta gotowe pudełka (`getBoundingClientRect`) i zawsze w układzie elementu, na którym rysuje (warstwa z `clip-path`, płótno spirali). Nigdy `innerWidth` jako szerokość ekranu: liczy pasek przewijania (15 px na Windows). Środek ekranu: `document.documentElement.clientWidth / 2`. `innerHeight` zmienia się na telefonie z paskiem adresu.
  3. Mierzyć od nowa, gdy coś się zmienia (`ResizeObserver` na elementach, doczytane fonty), nie tylko przy `resize` okna.
  4. Każde nowe położenie sprawdzać narzędziem na wielu szerokościach i gęstościach, z prawdziwym paskiem przewijania (wzór: `tools/center.py`), a nie wzrokiem na jednym zrzucie.
  5. **Tekst, który z założenia nie wychodzi** (taniej niż sprawdzanie; `sizes.py` ma tylko potwierdzać):
     - duże tytuły mają wielkość ograniczoną i szerokością, i wysokością (`min(…vw, …vh)` albo `clamp`), lokalnie w danym tytule, bez zmiany globalnego `--r`;
     - teksty w układzie flex/grid z odstępami, a nie w pozycjach absolutnych obok innych elementów;
     - wielkość liczona względem pudełka, w którym tekst stoi (jednostki kontenera `cqi`/`cqh`), a nie całego okna.

### 6.4 Sposoby, które rodzą błędy (pamiętać przy pisaniu kodu; pełne przypadki w `wiedza/lekcje.md`)
1. **Ten sam element sterowany dwa razy.** Przejście CSS i GSAP na jednej właściwości, dwa tweeny na jednej zmiennej. Jedno źródło prawdy dla każdej wartości.
2. **Tween napisu złożonego** (`clip-path`, `transform` jako tekst). Przeglądarka skraca zapis i liczby się przesuwają. Tweenować liczby w obiekcie, a napis składać w `onUpdate`.
3. **Wartości policzone raz, a układ się zmienia** (fonty, pasek adresu, rozwinięty wiersz). Mierzyć na żywo albo przeliczać przy zmianie rozmiaru; po `refresh` w spoczynku wymusić przerysowanie.
4. **Animowanie właściwości układu** (`width`, `height`, `top`, zmienna na `<html>`). Przeliczają całą stronę. Lepiej `transform`, `opacity` i zmienne na samym elemencie.
5. **Duży element przesuwany bez własnej warstwy** (obraz z paralaksą, długi napis). Telefon przerysowuje go co klatkę. Dodać `will-change`.
6. **Opóźnienie `scrub` w jednym z dwóch elementów**, które muszą się mijać: przy szybkim przewijaniu jeden zostaje w tyle. Elementy zależne od siebie bez opóźnienia albo z tym samym.
7. **Jednostki ekranu na telefonie:** `svh`, `dvh` i `lvh` różnią się o pasek adresu. Stałe warstwy `lvh`, przypięte ekrany `svh`; `dvh` tylko tam, gdzie nic nie jest liczone z wysokości.
8. **Progi dobrane do jednego ekranu** (`min-height:600px`, rozmiary z desktopu na tablecie). Każdą stałą w px sprawdzić na 320 px i na 1024 px.
9. **Ciężkie filtry na wielu elementach** (`filter: blur` na kilkudziesięciu słowach) i kompilacja shaderów przy pierwszym rysowaniu dają szarpnięcia 50–100 ms. Filtr na jednym elemencie albo w WebGL; `renderer.compile` przy ładowaniu.

## 7. Lista kontrolna przed oddaniem sekcji

- [ ] Liczby (długość sekcji, progi, czasy, krzywe) wzięte z kodu oryginału albo zmierzone, nie zgadnięte; nowe pomiary dopisane do `wiedza/pomiary.md`.
- [ ] Porównanie z oryginałem w tych samych miejscach sekcji (liczby, a od zadania 1 także obraz obok siebie).
- [ ] Przewinięte prawdziwym kółkiem: wolno, szybko, z zatrzymaniem w połowie przejścia, w górę i z powrotem.
- [ ] Nic nie nachodzi na tekst; kontrast w każdej klatce przejścia kolorów.
- [ ] Ruch sprawdzony narzędziem co klatkę (`overlap.py`, `motion.py`), na telefonach, tablecie i desktopach z paskiem przewijania; w spoczynku to za mało.
- [ ] Telefon 375×812: brak przewijania w poziomie, proporcje z oryginału dla <1025 px, brak nakładania warstw.
- [ ] 60 kl./s (średnio ok. 16,7 ms na klatkę), zero błędów w konsoli.
- [ ] Zatwierdzone odstępstwa (§2) nienaruszone.
- [ ] Nowy błąd, który kosztował rundę pracy, dopisany do `wiedza/lekcje.md`; stan sekcji w §5 zaktualizowany.
- [ ] Commit, push, sprawdzenie na Pages z `?v=`, aktualizacja artefaktu, przywrócenie widoku „desktop”.
