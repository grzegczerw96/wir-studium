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
