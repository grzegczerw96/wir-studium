# Lekcje (objaw → przyczyna → rozwiązanie)

Przeniesione z CLAUDE.md (§7) 10.10.2026. Czytać przy szukaniu błędu: najpierw tu, czy objaw już był. Każdy nowy błąd, który kosztował rundę pracy, dopisać jako wiersz. Skrót najczęstszych przyczyn jest w CLAUDE.md („Sposoby, które rodzą błędy”).


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
| Przewracająca się litera „R” przelatuje przez otwarte już „O” (wejścia B i C) | Litera wchodzi z obrotu wokół osi .85em za nią, więc startuje .85em pod swoim miejscem i przelatuje przez wiersz niżej | Wiersze nad „O” wchodzą od góry (`--rx` +90°), pozostałe od dołu; sprawdzać `tools/overlap.py` co klatkę, nie tylko w spoczynku |
| Na tablecie pierwsza linia notki pod przewracającymi się literami „MATERIAŁ” | W połowie obrotu litera jest 1,5× wyższa i wychylona; notka startowała równolegle 3rem niżej | Na telefonie i tablecie notka rusza, gdy litery tytułu są prawie płaskie (.25 s przed ostatnią) |
| W wersji 5 na końcu przeskok na prawej krawędzi „Ł” (zgłaszany dwa razy, poprawiany „na oko”) | Maska maluje tylko w pudełku elementu; przez −.04em odstępu ostatnia litera wystaje poza pudełko tytułu o ok. .04em, ten skrawek był cały czas ucięty i wskakiwał po zdjęciu maski | Na czas maski `padding: 0 .2em` i `margin: 0 -.2em` (układ bez zmian); wykrywać przeskoki narzędziem (`tools/motion.py`), nie wzrokiem |
| Dym w ramce z widocznymi granicami; tekst czasem przed dymem | Warstwa WebGL bez wygaszenia przy krawędziach; brzeg odsłaniania i dym liczone z różnych miejsc (gdzie szum rzadki, tekst wychodził przed dym) | Dym rzednie ku krawędziom warstwy (winieta), warstwa większa i przycięta tak, by nie wchodziła na notkę; dym budowany wokół tego samego brzegu, który odsłania tekst |
| Przy przejściu z napisu rysowanego na tekst strony szary „dołek” albo cień | Przenikanie obu warstw naraz | Tekst strony wchodzi na wierzch identycznego rysunku, potem warstwa znika |
| „Elipsa dolatuje, przerwa, kłąb dymu, przerwa, dym” | Dym startował po wylądowaniu elipsy, czoło z wolnym startem (sine in-out), kłąb i pierścień jako osobne fazy | Start dymu w trakcie lądowania elipsy, czoło sine out, źródło dymi aż do pierścienia; mierzyć `motion.py` (stall) |
| Notka wchodzi na paski na niskim oknie szerokości tabletu (zrzut Grzegorza ~1000×700) | Tytuł dobierany tylko do szerokości; narzędzia sprawdzały 6 stałych rozmiarów | Tytuł mieści się też w wysokości; `tools/sizes.py` przechodzi przez 178 rozmiarów (na starej wersji: 20 złych) |
| Na końcu dymu cały napis „wyostrza się” (telefon) albo krawędzie liter drgają | Rysowany napis w warstwie (75% rozdzielczości na telefonie, ułamkowa pozycja) różnił się od tekstu strony i był podmieniany naraz | Warstwa na pełnych pikselach i pod tekstem; litera strony wchodzi, gdy dym ją minie, a rysowana pod nią znika z warstwy |
| Szarpnięcia 50–100 ms w chwili pojawiania się notki | Rozmycie (`filter: blur`) na ~20 słowach naraz | Same zanikanie słów; ciężkie filtry tylko na jednym elemencie albo w WebGL |
| Spirala 7 px na prawo od środka „O” u Grzegorza, a w narzędziach na środku; „O” o 13 px węższe | Wycięcie okna liczone od `innerWidth`, który zawiera pasek przewijania (15 px), a warstwa z `clip-path` go nie zawiera; narzędzia ukrywały pasek, więc tego nie widziały | Wszystko w układzie warstwy (`stage.getBoundingClientRect()`), środek ekranu z `clientWidth`; testy z prawdziwym paskiem i gęstością 1,25 (`tools/center.py`) |
| Spirala „nie na środku” litery O, choć liczby się zgadzały | Ocena na oko: światło z lewej góry przesuwa jasną masę, a rozciągnięty pierścień 2D wygląda płasko | Mierzyć pikselami w obrębie elipsy (jasne piksele kontra obrys, wynik w px, `window.__o` w `lab/hero.html`); do oceny używać prawdziwej spirali 3D, nie uproszczonej |
| Telefon: szarpnięcie przy pierwszym pojawieniu się spirali | Kompilacja shaderów przy pierwszym rysowaniu; spirale rysowane także przy kryciu 0 | `renderer.compile` przy ładowaniu; rysowanie tylko widocznych (`coil.on`) |

