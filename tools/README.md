# Narzędzia kontroli jakości (szczegóły)

Kiedy którego użyć: tabela w CLAUDE.md („Kontrola jakości”). Tu: instalacja, opcje, co dokładnie sprawdzają, znane fałszywe alarmy.

## Instalacja

Narzędzia są w `tools/` (Python 3.8, uruchamiane przez `py -I`). Biblioteki leżą poza repo w `%LOCALAPPDATA%\wir-tools`:
- `pw/`: `py -m pip install --target %LOCALAPPDATA%\wir-tools\pw playwright==1.47.0 pillow==10.4.0`;
- `lib/`: lokalne kopie gsap 3.12.5, ScrollTrigger, lenis 1.1.13 i three r149 (pobrane z tych samych adresów CDN co strona);
- `out/`: zrzuty i raporty.

Pobrany Chromium Playwrighta nie startuje na tym Windowsie (błąd „konfiguracja równoczesna”), więc narzędzia uruchamiają zainstalowany Chrome (`channel='chrome'`). Gdy brakuje `wir-tools`, odtwarza się go powyższymi poleceniami.


## Narzędzia

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
- **`tools/overlap.py`:** nachodzenie elementów **w ruchu** w `lab/hero.html`: co ok. 40 ms każdego wejścia (A/B/C) i w 21 pozycjach przewijania czyta żywe pudełka (litery i linie notki tylko widoczne: obrót < 75°, krycie > .3) i zgłasza: okno na literze, notka na tytule, tekst na paskach, nagłówek na tekście, okno na notce, tekst za krawędzią. 6 ekranów (2 telefony, tablet, 3 desktopy) z paskiem przewijania; `--shots` zapisuje pierwszą klatkę każdego zgłoszenia. Sprawdzone na wersji z błędami (litera „R” przelatująca przez „O”, notka pod przewracającym się „MATERIAŁ” na tablecie).
- **`tools/motion.py`:** ruch z pikseli: nagrywa wejście klatka po klatce (screencast CDP, PNG) i zgłasza **przeskok** (kafelek 16 px zmienia się nagle, a przed i po nim on i 8 sąsiadów stoją; zmiana liczona na 16 ms, bo nagranie gubi klatki), **ramkę** warstwy efektu (krawędź `.smoke` widoczna jako różnica pikseli w środku i na zewnątrz) i **kolejność** (z `?dbg=smoke`: dym czerwony, scena granatowa; litera pokazuje tusz, zanim był w niej dym). Sprawdzone na starej wersji: łapie przeskok „Ł” w 5, ramkę i kolejność w dymie, przeskok przy przejściu na tekst strony; fałszywe alarmy (zanik logo przy rzadkich klatkach, krawędź jadącej elipsy, elipsa brana za tusz) usunięte.
- **`motion.py`, stall i jank:** stall = obraz stoi ≥ 0,2 s w trakcie animacji (zmiana < 0,35 na 0,1 s, od pierwszego ruchu do ¾ drogi do ostatniego; spokojna końcówka dozwolona); jank = klatki > 50 ms po starcie (czasy `requestAnimationFrame` w stronie) z ciężkimi operacjami w tej klatce (kompilacja WebGL, wysyłanie tekstur, `getImageData`, długie zadania). Sprawdzone na wersji z przerwami, które widział Grzegorz (stall 1,6–3,0 s, klatki 66–100 ms przy notce).
- **`motion.py --origin=SELEKTOR`:** efekt (w trybie testowym czerwony) musi się narodzić wewnątrz wskazanego elementu i rosnąć z niego; zgłasza narodziny poza nim i piksele efektu dalej niż czoło poprzedniej klatki (+60 px + 600 px/s). Zawsze wypisuje, gdzie efekt się narodził. Sprawdzone na wersji, którą Grzegorz oglądał (`0379ade`: dym rodził się 79 px od środka „O” o promieniu 52).
- **Pasek przewijania w narzędziach:** Playwright domyślnie go ukrywa (`--hide-scrollbars`), a u Grzegorza (Windows, Chrome, gęstość 1,25) ma 15 px. `_env.launch(p, scrollbars=True)` go pokazuje. `audit.py` i `paths.py` jeszcze działają bez paska; przy przenoszeniu hero na stronę główną przestawić je na pasek.
- **`tools/probe.py`:** pomiar oryginału albo naszej strony w wybranych miejscach. W cappen przed pomiarem `window.main.scroller.stop()` (jego przyciąganie zwraca wtedy bieżącą pozycję), u nas przyciąganie wyłączone. Litery oryginału mają `--rotateX` w `style`, nasze `--rx`. Liczby porównuje się w ekranach od początku sekcji.
- **`tools/phone.py` na prawdziwym telefonie** (Samsung Galaxy M15 5G, Chrome, 360×649 z paskiem adresu, 705 bez niego, 90 Hz):
  - przygotowanie: kabel USB, debugowanie USB, `adb` z `Google.PlatformTools`; na telefonie otwarta nasza strona;
  - **dotykać tylko karty z naszą stroną**, inne karty to prywatne karty Grzegorza;
  - gest palca `Input.synthesizeScrollGesture` (z chowaniem paska adresu), zrzut całego ekranu przez `adb`, czasy klatek;
  - `--local` podaje telefonowi niewypchniętą wersję z tego komputera.
- **Szukanie szarpnięć na telefonie:** zwykła strona z samym tekstem daje na nim równe 11 ms, więc wszystko powyżej to nasz koszt. Mierzyć sekcjami, zimny i rozgrzany przejazd. Winowajcę zawężać wyłączaniem: `ScrollTrigger.getAll()[i].disable()` grupami, ukrywanie elementów. Oryginał na tym telefonie: 40–175 ms na klatkę.

## Strona główna i lab

`center.py`, `overlap.py`, `motion.py` i `sizes.py` sprawdzają domyślnie stronę główną (lokalny `index.html` z lokalnymi bibliotekami). Pierwszy argument `lab` przełącza na `lab/hero.html`, a adres URL wybiera profil po ścieżce. Profile (`_env.PAGES`) podają identyfikatory tytułu, notki i sceny, czas ustalania się przewijania (na stronie głównej `scrub .6`, więc 800 ms), wyłączenie dociągania i parametry wejścia. JS narzędzi jest pisany z identyfikatorami labu, a `_env.adapt()` podmienia je na identyfikatory strony.

`phone.py` ma krok `{"open":"fx=5"}`: wczytuje stronę z parametrem i liczy klatki od jej pierwszej chwili (wejście), do najbliższego `{"fps":"stop"}`. Kroki dla hero: `tools/phone-hero.json`.
