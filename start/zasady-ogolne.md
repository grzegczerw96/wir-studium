# Zasady ogólne: strony z ruchem (wnioski z Wir Studio, 8–11.10.2026)

Przenośne na każdą stronę z dużą ilością animacji. Każda zasada wzięła się z błędu, który kosztował rundę pracy
albo dotarł do Grzegorza. Szczegóły i przypadki: `wiedza/lekcje.md` w repo wir-studium.

## 1. Jak pracujemy

- **Dwie ścieżki.**
  - *Odtwarzanie* (wzorzec to oryginał): najpierw pomiar (kod oryginału, `getBoundingClientRect`, piksele), potem budowa, a sprawdzanie to porównanie z oryginałem w tych samych miejscach. Progi responsywności przepisujemy z oryginału.
  - *Własna sekcja* (wzorzec to zatwierdzony wariant w `lab/`): warianty ocenia Grzegorz okiem. Po wyborze powstaje tabela reguł, potem przeniesienie na stronę.
- **Liczba testów wynika z ryzyka.** Trzy pytania:
  1. Czy technika jest nowa lub krucha? (WebGL, płótno → DOM, stałe warstwy, zależność od wysokości ekranu.)
  2. Ile stanów dotyka? (Kierunek przewijania, pasek adresu, ładowanie, sąsiednie sekcje.)
  3. Czy oko zdąży to zobaczyć?

  Zwykła sekcja to kilka minut sprawdzania. Komplet tylko przy nowej technice, raz, przy przeniesieniu. Pełna responsywność raz, na końcu całości.
- **Najpierw: czy człowiek to zobaczy?** Zgłoszenie niestabilne („1 na 3 przebiegi”): najpierw jedno zwolnione nagranie, kolejne przebiegi dopiero, gdy na nim coś widać.
- **Zgłoszenie najpierw porównać z poprzednią wersją** (commit). Stary błąd w trakcie nowej pracy zapisać, nie badać.
- **Nowe narzędzie tylko dla błędu, który wróci w innych sekcjach.** Każdy nowy test najpierw musi złapać błąd na starej wersji. Błąd, który dotarł do Grzegorza, dostaje swój test. Test, który przez 3 sekcje nic nie znalazł, schodzi na koniec całości. Jednorazowe skrypty nie trafiają do repo.
- **Bez reguł dla rzeczy smakowych** (np. kierunek dymu): to ocenia człowiek.
- **Nowy czat na każdy etap.** Długa rozmowa drożeje z każdą rundą, a wszystko ważne ma być w repo.
- **Koszty:** samo uruchomienie narzędzia jest tanie. Drogie są: badanie zgłoszeń, rundy „zmiana, test, obrazek, wniosek”, oglądanie zrzutów, czytanie dużych plików (szukać po nazwach klas, nie czytać całości).

## 2. Telefon (Chrome na Androidzie): co trzeba wiedzieć

- **Wysokości ekranu:**
  - `svh` = ekran z paskiem adresu, `lvh` = bez paska, `dvh` = bieżący.
  - Przypięte ekrany (sticky) w `svh`, bo wysokość zmieniana w trakcie przewijania przesuwa treść przyklejoną do dołu.
  - Stałe warstwy (fixed, tło sceny) w `lvh`, żeby po schowaniu paska nie było białego pasa.
- **Treść przyczepiona do dołu ekranu:**
  - `position:fixed; bottom` → Chrome przesuwa ją razem z paskiem adresu, bez opóźnienia.
  - Elementy w `dvh` lub w przypiętym ekranie Chrome przelicza dopiero po skończonym geście. Do tego czasu pod nimi widać pas ok. 56 px (otwarta sprawa w stopce Wir).
- **`resize` na dotyku** przychodzi przy każdej zmianie paska adresu (zmienia się tylko wysokość). Przeliczać układ tylko przy zmianie szerokości; `ScrollTrigger.config({ignoreMobileResize:true})`. Odświeżanie w trakcie przewijania daje szarpanie.
- **Przewijanie natywne na dotyku.** Bez wygładzania (Lenis: `smoothWheel:false`, `syncTouch:false`), bez blokady przewijania (`lock`), gdy palec jest na ekranie; programowe przewijanie walczące z palcem odczuwa się jako opór i szarpanie.
- **Pierwsze malowanie:**
  - Ciężka praca w skrypcie przed pierwszym malowaniem = pusty ekran (na telefonie 2–3 s).
  - Główny skrypt uruchamiać po `DOMContentLoaded` i dwóch klatkach; to, czego nie widać na pierwszym ekranie, liczyć później albo w Web Workerze (`OffscreenCanvas`).
  - Mierzyć pierwsze wejście przez `about:blank`: przeładowanie z tej samej strony trzyma stary obraz („paint holding”) i myli pomiar.
- **Długie klatki:**
  - GSAP z Lenisem ma `lagSmoothing(0)`, więc po długiej klatce animacja przeskakuje. Animację wejścia startować klatkę po odsłonięciu strony.
  - Shadery kompilować przy ładowaniu (`renderer.compile`), nie przy pierwszym rysowaniu.
  - Ciężką pracę w tle (rysowanie obrazów) robić po wejściu, nie w trakcie efektu, nawet w osobnym wątku.
- **Koszty rysowania:**
  - `filter: blur` na kilkudziesięciu elementach naraz = klatki 50–100 ms. Filtr na jednym elemencie albo w WebGL.
  - Duży element przesuwany co klatkę potrzebuje własnej warstwy (`will-change`).
  - Nie animować `width`, `height`, `top` ani zmiennych na `<html>` (przeliczają całą stronę); zmienne CSS ustawiać na sekcji.
- **Emulacja nie pokaże paska adresu ani płynności.** To sprawdza prawdziwy telefon: klatki z `requestAnimationFrame` (90 Hz = 11 ms na klatkę jako punkt odniesienia), nagranie ekranu klatka po klatce (screencast CDP), zrzuty przez `adb`.

## 3. Ułatwianie przewijania (strona prowadzi użytkownika)

- **Dociąganie w miejscach przejść,** gdzie można utknąć w połowie (okno rosnące do pełnego ekranu, wejście formularza, koniec strony). Liczby z oryginału, np. „>10% → do końca, 0,25–2 s, quad in-out”.
- **Na dotyku tylko po zdjęciu palca:**
  - 0,25 s bez ruchu, kierunek liczony od miejsca dotknięcia;
  - jedno dociągnięcie na jeden gest: po starcie jazdy liczyć kierunek od celu, inaczej zmiana wysokości strony przez pasek adresu odpali je drugi raz;
  - dotknięcie przerywa jazdę.
- **Bez martwego przewijania:** gdy animacja sekcji się skończyła, sekcja nie powinna ciągnąć się dalej o ekran, który trzeba potem przewinąć z powrotem (na telefonie szczególnie).
- **Skoki z menu do sekcji** lądują w stanie gotowym (np. formularz już wjechany), nie w środku przejścia koloru.

## 4. Przejścia kolorów i warstwy

- **Kolor strony liczony co klatkę z żywego położenia sekcji** (`getBoundingClientRect`), nie dwoma tweenami na jednej właściwości (nadpisywały się przy odświeżeniu, tekst znikał biały na białym).
- **Jedno źródło prawdy dla każdej wartości.** Przejście CSS i GSAP na tej samej właściwości gonią się nawzajem.
- **Tekst nigdy na tle bez kontrastu:**
  - przejście koloru startuje, gdy treść już zeszła albo tło jest już ciemne;
  - lista nie stoi na szarym środku przejścia.
- **Bryła 3D lub obraz za tekstem:** położenie przy tekście liczyć z żywego układu (wolny pas między blokami tekstu), nie stałym procentem ekranu. Reguła w teście: pudełko bryły nie wchodzi pod widoczny tekst.
- **Stała warstwa wspólna dla wielu sekcji** (fixed): przycięta do swojej sekcji (`clip-path`), wyłączona, gdy jej nie widać, `z-index` opisany (która treść jest nad nią).
- **Stan liczony w tickerze** (`gsap.ticker`), nie w `onUpdate`: `ScrollTrigger.refresh()` potrafi pominąć callbacki i stan „wisi”.

## 5. Responsywność u źródła (reguły, nie sprawdzanie)

- **Gdzie co stoi, decyduje CSS** (flex/grid, odstępy, jednostki z kroju, `min(vw, svh)`, `clamp`, `aspect-ratio`, jednostki kontenera). JS nie wpisuje pozycji w px, tylko czyta gotowe pudełka.
- **JS czyta w układzie warstwy, na której rysuje** (płótno, warstwa z `clip-path`). Nigdy `innerWidth` jako szerokość ekranu: liczy pasek przewijania (15 px na Windows); środek to `document.documentElement.clientWidth / 2`.
- **Tabela reguł po wyborze projektu.** Dla każdego elementu: do czego przyczepiony, jak rośnie, czego nie może dotknąć. Człowiek decyduje, co ustępuje na skrajnych ekranach. Reguły od razu w CSS, tak żeby nie dało się ich złamać.
- **W każdym przedziale szerokości wielkości zmieniają się liniowo,** więc sprawdza się rozmiary krytyczne: rogi przedziałów, linie przełączenia `min()` i miejsca skoków (zawijanie tekstu, progi w JS). Pełna siatka (np. 178 rozmiarów) raz, na końcu.
- **Testy położeń z prawdziwym paskiem przewijania i gęstością 1,25** (typowy Windows), bo Playwright domyślnie pasek ukrywa.
- **Każdą stałą w px sprawdzić na 320 i 1024 px.** Progi dobrane do jednego ekranu (`min-height:600px`) psują mały telefon i tablet.
- **Polskie znaki w wielkich tytułach:** interlinia ok. 0,9 (kropka nad „Ż”, ogonki).

## 6. Efekty: płótno lub WebGL przekazujące obraz do tekstu strony

- **Pozycje liter mierzyć płasko** (`transform:none` na czas pomiaru). Obrócona litera w perspektywie ma pudełko obok swojego miejsca.
- **Przekazanie litera po literze,** gdy efekt minie najdalszy róg litery (z zapasem na poszarpany brzeg). Litera strony wchodzi na wierzch; rysowana pod nią gaśnie dopiero potem (0,35 s). Przenikanie obu naraz daje szary dołek, zniknięcie naraz daje „wskakiwanie”.
- **Warstwa efektu na pełnych pikselach,** z wygaszeniem przy krawędziach (winieta), przycięta tak, by nie wchodziła na inny tekst.
- **Falowanie lub zniekształcenie tylko tam, gdzie efekt jeszcze odsłania;** na odsłoniętej części znikało w kilku klatkach i wyglądało na skok.
- **Maska** maluje tylko w pudełku elementu; ostatnia litera z ujemnym odstępem wystaje poza pudełko (dodać `padding` i ujemny `margin`).

## 7. Jak nie psuć innych sekcji

- **Sekcja ma własny zakres:** klasy z prefiksem, zmienne na sekcji, nasłuchy z warunkiem „ta sekcja jest na ekranie”.
- **Bez nazw globalnych** (np. `main()` na `window` pomyliło narzędzia z oryginałem, który ma `window.main`). Skrypt w funkcji anonimowej; do narzędzi wystawiać jawnie `window.__nazwa`.
- **Pozycje triggerów się starzeją,** gdy coś powyżej zmienia wysokość: po takiej zmianie `ScrollTrigger.refresh()`, a rzeczy krytyczne liczyć z żywego układu.
- **Wspólne flagi** (np. „trwa programowe przewijanie”) sprawdzać wszędzie, gdzie strona sama przewija.
- **Styki sekcji to miejsce większości błędów** (szare tło pod listą, napis nad formularzem, ucięta bryła): po zmianie sekcji, która zmienia kolor strony albo dzieli warstwę z sąsiadem, test przejść przy prawdziwym kółku, w obie strony (`paths.py`).
- **Zmiana długości sekcji przesuwa wszystko pod nią:** sprawdzić osie zależne od niej (np. bryła w stopce liczona od dołu stopki).

## 8. Narzędzia (z repo wir-studium, `tools/`)

**Uniwersalne** (przenośne, po podmianie selektorów):
- `probe.py`: liczby oryginału i naszej strony w tych samych miejscach;
- `audit.py`: nachodzenie, ucięty tekst, przewijanie w bok, prześwit przy krawędzi; 3 ekrany ok. 1 min;
- `paths.py`: przejścia przy kółku, reguły dopisywane w `RULES`;
- `sizes.py`: grupy elementów na wielu rozmiarach (`--groups`, `--sizes`);
- `phone.py`, `phone_load.py`: prawdziwy telefon (klatki, gesty, nagranie ładowania, skoki liter efektu).

**Pod konkretny element lub efekt** (wzór do skopiowania, gdy nowa strona ma podobny element):
- `motion.py`: przeskoki, przerwy, krawędzie warstwy efektu z pikseli;
- `coil.py`: rozmiar i położenie bryły 3D w oryginale i u nas.

Biblioteki narzędzi poza repo (`%LOCALAPPDATA%\wir-tools`: Playwright 1.47, Pillow, lokalne kopie bibliotek strony). Pobrany Chromium nie startuje na tym Windowsie, więc narzędzia uruchamiają zainstalowany Chrome (`channel='chrome'`).
