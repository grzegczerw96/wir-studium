# Baza wiedzy Wir Studio

Miejsce, z którego Claude czerpie, kiedy ma sam dobierać i wymyślać ruch, styl i opowieść strony. CLAUDE.md mówi **jak** pracujemy; ten folder mówi **z czego** wybieramy.

## Co tu jest

| Plik | Co zawiera | Kto dopisuje |
|---|---|---|
| `marka.md` | Historia Wir Studio, ton tekstów, słowa-klucze, czego unikamy | Grzegorz (Claude pomaga ułożyć) |
| `inspiracje.md` | Strony i ruchy, które się podobają, z jednym zdaniem „dlaczego” | Grzegorz wkleja link i zdanie, Claude dopisuje pomiary |
| `katalog-ruchu.md` | Słownik ruchów: co robią, kiedy pasują, liczby, gdzie już użyte | Claude po każdej próbie; Grzegorz ocenia |
| `pomiary.md` | Liczby zmierzone w oryginale (cappen) dla każdej sekcji, desktop i telefon; mechanizmy dociągania | Claude po każdym pomiarze |
| `lekcje.md` | Błędy, które już były: objaw → przyczyna → rozwiązanie | Claude po każdym błędzie, który kosztował rundę pracy |
| `hero.md` | Hero: co wybrane, co jest w `lab/hero.html`, uwagi Grzegorza | Claude po każdej decyzji o hero |
| `media/` | Nagrania i zrzuty cudzych stron, szkice, zdjęcia z telefonu | Grzegorz; **nie trafia do repo** (repo jest publiczne) |

## Jak dodawać (najprościej)

- **Strona, która się podoba:** w `inspiracje.md` jeden wiersz: link, co dokładnie się podoba (np. „jak litery wpadają po załadowaniu”), do której naszej sekcji by pasowało. Wystarczy też napisać to w czacie, Claude przepisze.
- **Nagranie ekranu** (`.mp4`, jak film z cappen): do `wiedza/media/`. Claude rozkłada je na klatki (`ffmpeg`), mierzy czasy i kolejność i dopisuje wnioski do `inspiracje.md`.
- **Zrzut z telefonu:** może zostać w telefonie; Claude pobiera dzisiejsze przez `adb`, jak dotąd.
- **Szkic na kartce albo w Figmie:** zdjęcie do `media/` albo link do Figmy.
- **Słowa o marce:** cokolwiek przyjdzie do głowy (skojarzenia, nastrój, czego nie chcemy) do `marka.md`, bez porządkowania.

## Jak Claude z tego korzysta

1. Na początku pracy nad sekcją czyta `marka.md`, `inspiracje.md` i `katalog-ruchu.md`.
2. Proponuje warianty, które łączą historię marki z ruchem z katalogu albo z inspiracji (z nazwą źródła).
3. Każdy wariant sprawdza narzędziami (`tools/overlap.py`, `tools/center.py`, `tools/audit.py`), zanim go pokaże.
4. Po decyzji dopisuje do katalogu: co wybrano, co odrzucono i dlaczego. Następne propozycje uczą się z tego.

Claude może też sam poszerzać bazę, gdy Grzegorz o to poprosi: przegląd stron nagradzanych (np. Awwwards, FWA), samouczków (Codrops) i dokumentacji GSAP, z pomiarem tak jak cappen.
