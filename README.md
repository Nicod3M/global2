# BOCA BOCA — strona internetowa

Jednostronicowa witryna dla tapas baru **BOCA BOCA** (Kwiatkowskiego 44c lok. U2,
35-311 Rzeszów), przygotowana pod domenę **bocaboca.pl**.

## Pliki

| Plik | Rola |
| --- | --- |
| `page.html` | **Źródło.** Fragment strony: `<title>`, `<style>` i cały markup. Tutaj wprowadzasz zmiany. |
| `build.sh` | Składa `page.html` w kompletny dokument z `<head>`, meta, Open Graph i danymi strukturalnymi. |
| `index.html` | **Generowany.** Plik do wgrania na serwer. Nie edytuj ręcznie. |

```bash
./build.sh      # page.html -> index.html
```

Strona jest w całości statyczna — jeden plik `index.html`, zero zależności,
zero zewnętrznych zasobów. Wgrywa się przez FTP do katalogu głównego domeny.

## Skąd pochodzą dane

Wszystkie treści są prawdziwe, nie są wygenerowane na potrzeby makiety:

- **Menu i ceny** — karta dowozowa Uber Eats i Pyszne.pl (stan: sierpień 2026).
- **Godziny otwarcia, adres, telefon, ocena 4,4 z 214 opinii** — profil Google Maps.
- **Cytaty w sekcji „Opinie”** — prawdziwe opinie Google wraz z autorem i datą.
- **Menu RestaurantWeek 2026** — materiały prasowe z rzeszowskiej edycji festiwalu.

Przy aktualizacji cen zmieniaj też datę w przypisie pod menu (`menu-note`).

## Logo

W `logo/` leży oryginalny plik od klienta (`bocaboca-logo.jpg`) oraz dwa kadry
wycięte z niego bez żadnej ingerencji w grafikę:

- `logo-lockup.jpg` — pełny znak (usta, kieliszek, wordmark, tagline), używany w hero,
- `logo-mark.jpg` — sam znak (usta + kieliszek), używany w nawigacji i stopce.

Oba kadry są wklejone do `page.html` jako data URI, żeby strona pozostała
jednym samodzielnym plikiem. Tło strony to dokładnie ten sam piaskowy co
w logo (`#FED291`), więc kadry wtapiają się w stronę bez widocznej ramki.
W motywie ciemnym logo zostaje na swoim piaskowym tle i czyta się jako naklejka —
to celowe, dzięki temu znak nigdy nie jest przemalowywany.

Kolory całej strony pobrane są pipetą z pliku logo: piaskowy `#FED291`
i winny `#940C0C`.

## Zdjęcia

Strona celowo nie zawiera zdjęć zastępczych. W `page.html` przygotowana jest
zakomentowana sekcja `GALERIA` — wystarczy wstawić 6 zdjęć (wnętrze, ogródek
o zachodzie słońca, smash burger, patatas bravas, deska serów, bar),
odkomentować blok i podmienić `src`. Zalecany format: `.webp`, dłuższy bok 1600 px.

## Motyw jasny i ciemny

Strona jest ciemna domyślnie i ma pełnoprawny wariant jasny — przełącza się
automatycznie za ustawieniem systemowym odwiedzającego. Kolory są zdefiniowane
wyłącznie jako zmienne CSS w `:root`; nie wpisuj wartości kolorów bezpośrednio
w regułach komponentów.
