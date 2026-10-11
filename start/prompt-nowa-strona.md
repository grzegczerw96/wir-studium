# Prompt: nowa strona do odwzorowania (nowy folder)

Wkleić w pierwszej wiadomości do agenta w nowym, pustym folderze. Uzupełnić [nawiasy].

---

Zaczynamy nowy projekt: odwzorowanie strony [URL ORYGINAŁU] w tym folderze. Odtwarzamy technikę, ruch i timing, nie treść:
fikcyjna marka [NAZWA], teksty po polsku i nasze, bez logo i tekstów oryginału.

Mam już doświadczenie z podobnym projektem; zestaw startowy jest w `C:\Projekty\wir-studium\start\` (w sieci:
https://github.com/grzegczerw96/wir-studium/tree/main/start). Zrób na początek:

1. Przeczytaj `start/README.md`, `start/zasady-ogolne.md` i `start/CLAUDE-szablon.md`.
2. Załóż w tym folderze: `CLAUDE.md` z szablonu (uzupełnij, co wiesz z tej wiadomości; czego nie wiesz, zapytaj mnie
   jednym zestawem pytań), `wiedza/zasady-ogolne.md` (kopia), `wiedza/pomiary.md`, `wiedza/lekcje.md` (puste nagłówki),
   `tools/` z narzędziami uniwersalnymi z `C:\Projekty\wir-studium\tools\` (`_env.py`, `probe.py`, `audit.py`,
   `sizes.py`, `paths.py`, `phone.py`, `phone_load.py`), z selektorami przepisanymi na nową stronę dopiero wtedy, gdy
   będą potrzebne. Narzędzi pod konkretne efekty (`motion.py`, `coil.py`) nie kopiuj, dopóki nie pojawi się podobny efekt.
3. Inwentaryzacja oryginału: lista sekcji od góry do dołu (nazwy klas, długość w ekranach przewijania, co się dzieje),
   biblioteki i ich wersje, jednostki i progi responsywności (desktop, tablet, telefon). Zapisz w `wiedza/pomiary.md`
   i jako tabelę sekcji w `CLAUDE.md` §5. Bez budowania.
4. Pokaż mi tabelę sekcji i zaproponuj kolejność pracy. Potem pracujemy jedną sekcją na raz, ścieżką A (odtwarzanie),
   chyba że powiem, że sekcję chcę zrobić po swojemu (ścieżka B).

Zasady, których trzymaj się od początku:
- liczby bierz z kodu i pomiaru oryginału, nie z wrażenia;
- sprawdzanie dobieraj do ryzyka (trzy pytania z `zasady-ogolne.md` §1); zwykła sekcja to kilka minut testów,
  nie komplet; pełna responsywność raz, na końcu;
- jeśli znasz sposób prostszy albo dokładniejszy niż w zasadach, powiedz krótko, co zyskujemy, i użyj go, gdy jest darmowy
  i lokalny; płatne usługi i konta tylko po mojej zgodzie;
- telefon traktuj jak pełnoprawny ekran (przewijanie palcem ma być lekkie);
- odpowiadaj po polsku: najpierw wynik, potem co i dlaczego, na końcu czego nie sprawdziłeś.
