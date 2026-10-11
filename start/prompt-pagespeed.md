# Prompt: PageSpeed (wydajność ładowania i działania)

Wkleić w nowym czacie, gdy sekcje są gotowe. Uzupełnić [nawiasy].

---

Etap: wydajność strony [URL podglądu, np. GitHub Pages]. Wygląd, ruch i czasy animacji mają zostać takie jak teraz;
poprawiamy to, jak szybko strona się pokazuje i jak płynnie działa, zwłaszcza na telefonie.

1. **Najpierw pomiar, bez zmian w kodzie:**
   - Lighthouse (PageSpeed) dla telefonu i desktopu, po 3 przebiegi, mediana: LCP, FCP, CLS, TBT (jako przybliżenie INP),
     Speed Index, rozmiar i liczba pobieranych plików;
   - na prawdziwym telefonie: `tools/phone_load.py` (pierwsze malowanie, odsłonięcie strony, nagranie ładowania) i
     `tools/phone.py` z przejazdem całej strony (czasy klatek, zimny i rozgrzany).
   Wyniki w jednej tabeli, plus 3–5 największych kosztów z wyjaśnieniem po ludzku (co zjada czas i ile).
2. **Pokaż mi tabelę i plan poprawek od największego zysku,** z oceną ryzyka dla wyglądu. Bez zmian, dopóki nie wybiorę.
3. **Poprawki po jednej:** po każdej ten sam pomiar, co w punkcie 1 (tylko to, czego dotyczy), i sprawdzenie, że wygląd
   się nie zmienił (zrzuty w tych samych miejscach przed i po, porównanie pikseli; tam, gdzie poprawka dotyka ruchu,
   `motion.py`). Tabela przed / po.
4. **Typowe kierunki** (z doświadczenia z wir-studium; sprawdź, czy dotyczą):
   - nic ciężkiego przed pierwszym malowaniem (skrypt po pierwszej klatce, obrazy liczone w tle, w Workerze);
   - fonty: tylko potrzebne kroje i grubości, `preload` tych z pierwszego ekranu;
   - biblioteki: wersje zminifikowane, ładowanie dopiero, gdy potrzebne (np. 3D dopiero przed sekcją z bryłą),
     `defer`;
   - obrazy: właściwe rozmiary i formaty (WebP/AVIF), leniwe ładowanie poza pierwszym ekranem;
   - CLS: rezerwowane miejsce na wszystko, co się doczytuje;
   - płynność: rysowanie tylko widocznych scen, bez filtrów na wielu elementach, `will-change` tylko tam, gdzie potrzebne.
5. **Granice:**
   - nie zmieniaj czasów i kolejności animacji ani wyglądu;
   - jeśli coś wymaga kompromisu (np. słabsza jakość bryły na telefonie), zapytaj;
   - darmowe narzędzia lokalne; płatne usługi, konta i zewnętrzne CDN z rejestracją tylko po mojej zgodzie.

Na koniec: tabela przed / po, co zostało i dlaczego, wpis w `CLAUDE.md` (stan, zasady wydajności, które warto
utrzymywać przy kolejnych sekcjach). Odpowiadaj po polsku: najpierw wynik, potem szczegóły.
