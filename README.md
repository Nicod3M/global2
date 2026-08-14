# BOCA BOCA — strona internetowa

Jednostronicowa witryna dla tapas baru **BOCA BOCA** (Kwiatkowskiego 44c lok. U2,
35-311 Rzeszów), przygotowana pod domenę **bocaboca.pl**.

## Pliki

| Plik | Rola |
| --- | --- |
| `page.src.html` | **Źródło.** Cały markup, style i skrypt. Tutaj wprowadzasz zmiany. |
| `build.py` | Składa źródło w dwa pliki wynikowe. `./build.sh` to nakładka na niego. |
| `index.html` | **Generowany.** Plik do wgrania na serwer — zdjęcia jako osobne pliki z `img/`. |
| `page.html` | **Generowany.** Ten sam layout, ale ze zdjęciami wklejonymi w treść — jeden samodzielny plik do podglądu lub wysyłki mailem. |
| `img/` | Zdjęcia w rozmiarze webowym, `img/small/` — lżejsze wersje do wersji samodzielnej. |
| `img/alt.json` | Opisy alternatywne zdjęć (dostępność i SEO). |
| `logo/` | Oryginalne logo od klienta i dwa kadry z niego. |

```bash
./build.sh      # page.src.html -> index.html + page.html
```

Na serwer wgrywa się `index.html` razem z katalogami `img/` i `logo/`.
Zero zależności, zero zewnętrznych zasobów, żadnego backendu.

## Skąd pochodzą dane

Wszystkie treści są prawdziwe:

- **Karta i ceny** — przepisane z fotografii menu obowiązującego w lokalu
  (tapasy, smash burgery, sałatki, zupy, dodatki, wino, koktajle, moctaile,
  piwo, alkohole mocne, kawa, matcha, herbata, lemoniady, softy).
  Oznaczenie 🌱 jest przeniesione 1:1 z karty, nie zgadywane.
- **Godziny otwarcia, adres, telefon, ocena 4,4 z 214 opinii** — profil Google Maps.
- **Cytaty w sekcji „Opinie"** — prawdziwe opinie Google wraz z autorem i datą.
- **Menu RestaurantWeek 2026** — materiały prasowe z rzeszowskiej edycji festiwalu.
- **Zdjęcia** — materiały własne lokalu.

Uwaga: karta dowozowa na Uber Eats i Pyszne.pl jest węższa i ma **inne ceny**
niż karta w lokalu. Strona pokazuje kartę lokalową i mówi o tym wprost
w przypisie pod menu. Przy aktualizacji cen zmień też datę w tym przypisie.

## Logo

W `logo/` leży oryginalny plik od klienta (`bocaboca-logo.jpg`) oraz dwa kadry
wycięte z niego bez ingerencji w grafikę:

- `logo-lockup.jpg` — pełny znak (usta, kieliszek, wordmark, tagline), w stopce,
- `logo-mark.jpg` — sam znak (usta + kieliszek), w nawigacji i jako favicon.

Tło strony to dokładnie ten sam piaskowy co w logo (`#FED291`), więc kadry
wtapiają się bez widocznej ramki. W motywie ciemnym logo zostaje na swoim
piaskowym tle i czyta się jako naklejka — to celowe, dzięki temu znak nigdy
nie jest przemalowywany.

Kolory całej strony pobrane są pipetą z pliku logo: piaskowy `#FED291`
i winny `#940C0C`.

## Motyw jasny i ciemny

Motyw jasny to logo wprost: wino na piaskowym. Motyw ciemny to logo odwrócone:
piaskowy na winnym — akcentem jest wtedy ten sam piaskowy, który znak ma
we własnym tle. Przełącza się automatycznie za ustawieniem systemowym
odwiedzającego. Kolory są zdefiniowane wyłącznie jako zmienne CSS w `:root`;
nie wpisuj wartości kolorów bezpośrednio w regułach komponentów.

## Interakcje

- **Karta** — trzy zakładki (Jedzenie / Bar / Kawa i napoje) plus przełącznik
  „Tylko wege". Kategorie bez pasujących pozycji chowają się same, a zmiana
  jest ogłaszana przez `role="status"`.
- **Galeria** — siatka 4×4 z lightboxem: strzałki, Escape, klik w tło,
  powrót fokusu na kafel po zamknięciu.
- **Godziny** — status „otwarte teraz / zamknięte, otwieramy o…" liczony
  po stronie klienta z prawdziwych godzin z Google.

## Animacje

Sekwencja startowa hero, odsłonięcia przy przewijaniu, dorysowywana kreska
nagłówka sekcji, naliczanie oceny 4,4, wypełnianie słupków rozkładu ocen,
pasek postępu czytania pod nawigacją, podświetlenie aktywnej sekcji w menu.

Panel „zachód słońca nad zalewem" jest zbudowany w całości w CSS, bez zdjęcia:
słońce zsuwa się na horyzont, odbicie migocze, fale dryfują. Nawiązuje
do motywu wracającego w opiniach gości i cytuje jedną z nich.

Wszystko respektuje `prefers-reduced-motion` — przy tym ustawieniu strona
pokazuje się od razu, bez ruchu.

## Responsywność

Sprawdzone na 320, 375, 414, 768, 1024, 1280, 1440 i 1920 px — zero
przewijania w poziomie. Typografia i odstępy skalują się przez `clamp()`,
nawigacja zwija się do arkusza pełnoekranowego poniżej 1000 px.
Jest też arkusz dla druku — karta wychodzi na papier bez tła, zdjęć
i przycisków, ze wszystkimi zakładkami rozwiniętymi.
