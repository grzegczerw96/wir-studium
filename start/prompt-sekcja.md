# Prompt: dodanie albo zmiana sekcji na istniejącej stronie

Wkleić w pierwszej wiadomości do agenta w folderze strony, która ma już `CLAUDE.md` (np. wir-studium). Uzupełnić [nawiasy]
i wybrać jeden wariant w punkcie 1.

---

Pracujemy nad sekcją [NAZWA / id, np. #about].

1. Co robimy (jeden wariant):
   - **odtwarzamy ją wierniej z oryginału** [co się nie zgadza, jeśli wiem] → ścieżka A;
   - **robimy ją po swojemu / przerabiamy** [co mi się nie podoba, co chcę uzyskać, inspiracje] → ścieżka B:
     najpierw 2–4 warianty w `lab/`, ja wybieram;
   - **dodajemy nową sekcję** [gdzie: między X a Y, po co] → ścieżka B.
2. Przeczytaj `CLAUDE.md` §0a i dalej tylko to, co do tej ścieżki potrzebne (pomiary tej sekcji albo `wiedza/` z marką
   i katalogiem ruchu). Nie czytaj całego `index.html`: szukaj po klasach tej sekcji i jej sąsiadów.
3. Zanim zaczniesz budować, napisz w kilku punktach:
   - co zmieniasz i co tej zmiany dotknie poza sekcją (kolor strony, wspólne warstwy, długość strony, przewijanie na
     telefonie, sąsiednie sekcje);
   - jakie sprawdzanie przewidujesz i dlaczego (trzy pytania o ryzyko). Bez kompletu testów „na wszelki wypadek”.
4. Przy ścieżce B, po moim wyborze wariantu: tabela reguł (do czego przyczepione, jak rośnie, czego nie może dotknąć),
   reguły od razu w CSS; dopiero potem przeniesienie na stronę.
5. Nie zmieniaj innych sekcji ani zatwierdzonych odstępstw bez pytania. Jeśli zauważysz w nich błąd, zapisz go w `CLAUDE.md`
   §5 i powiedz mi; nie naprawiaj przy okazji.

Jeśli znasz prostszy albo dokładniejszy sposób niż w `CLAUDE.md`, zaproponuj go krótko i użyj, gdy jest darmowy i lokalny.
Na koniec: stan sekcji w `CLAUDE.md` §5, nowy błąd do `wiedza/lekcje.md` tylko wtedy, gdy kosztował rundę pracy,
commit i push.
