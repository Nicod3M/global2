#!/usr/bin/env python3
"""
Składa page.src.html w dwa pliki:

  index.html  — kompletny dokument do wgrania pod bocaboca.pl.
                Zdjęcia jako osobne pliki z img/ (lazy-loading, cache).

  page.html   — ten sam layout, ale ze zdjęciami wklejonymi jako data URI,
                czyli jeden samodzielny plik (podgląd, wysyłka mailem).

page.src.html jest jedynym źródłem treści — obu wynikowych plików nie edytuj.
"""

import base64
import json
import pathlib
import re
import struct
import sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "page.src.html"
IMG_DIR = ROOT / "img"
LOGO_DIR = ROOT / "logo"

# Zdjęcia w galerii — kolejność ma znaczenie, pierwsze zajmuje dwa rzędy.
# 15 kafli + podwójna wysokość pierwszego = równe 16 pól siatki 4×4.
# Witryna lokalu nie powtarza się tutaj — jest przy sekcji Kontakt.
GALLERY = [
    "burger-przekroj", "papryczki", "sernik", "cannoli",
    "brownie-makaroniki", "koktajle", "burger-batat", "paczki",
    "piwa", "spicy-smash", "patatas-bravas", "tacosy",
    "ciasto-marchewkowe", "wino-z-kranu", "burger-neon",
]

# Ładowane od razu, nie leniwie — widoczne w pierwszym ekranie.
EAGER = {"burger-neon"}


def jpeg_size(path):
    """Wymiary JPEG-a bez zewnętrznych bibliotek."""
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        (seg_len,) = struct.unpack(">H", data[i + 2:i + 4])
        i += 2 + seg_len
    raise ValueError("nie znaleziono wymiarów w %s" % path)


def data_uri(path):
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()


def load_meta():
    """Opisy alt pochodzą z photos.json wygenerowanego przy obróbce zdjęć."""
    meta_path = ROOT / "img" / "alt.json"
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    return {}


ALT = load_meta()


def img_tag(name, inline, cls="", sizes_attr="", eager=False):
    # wersja serwerowa bierze pełne zdjęcia, samodzielna — lżejsze z img/small,
    # żeby jeden plik nie urósł do kilku megabajtów
    path = IMG_DIR / (name + ".jpg")
    w, h = jpeg_size(path)
    src = data_uri(IMG_DIR / "small" / (name + ".jpg")) if inline else "img/%s.jpg" % name
    alt = ALT.get(name, "")
    loading = "eager" if eager else "lazy"
    prio = ' fetchpriority="high"' if eager else ""
    klass = ' class="%s"' % cls if cls else ""
    return ('<img%s src="%s" alt="%s" width="%d" height="%d" '
            'loading="%s" decoding="async"%s%s>'
            % (klass, src, alt, w, h, loading, prio, sizes_attr))


def gallery_markup(inline):
    out = []
    for i, name in enumerate(GALLERY):
        alt = ALT.get(name, "")
        cls = "shot tall" if i == 0 else "shot"
        out.append(
            '<button class="%s" type="button" aria-label="Powiększ zdjęcie: %s">%s</button>'
            % (cls, alt, img_tag(name, inline))
        )
    return "\n        ".join(out)


HEAD = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BOCA BOCA — tapas i smash burgery, Rzeszów</title>
<meta name="description" content="Tapas bar i smash burgery przy Kwiatkowskiego 44c w Rzeszowie. Hiszpańskie przekąski, burgery z blachy, wino rozlewane z kranu i ogródek z widokiem na zalew. Rezerwacja: 790 394 366.">
<link rel="canonical" href="https://bocaboca.pl/">
<meta name="theme-color" content="#FED291" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#2A0A0B" media="(prefers-color-scheme: dark)">

<meta property="og:type" content="restaurant.restaurant">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="BOCA BOCA">
<meta property="og:title" content="BOCA BOCA — tapas i smash burgery, Rzeszów">
<meta property="og:description" content="Hiszpańskie tapas, smash burgery z blachy i wino z kranu. Ogródek z widokiem na zachód słońca nad rzeszowskim zalewem.">
<meta property="og:url" content="https://bocaboca.pl/">
<meta property="og:image" content="https://bocaboca.pl/img/burger-neon.jpg">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="logo/logo-mark.jpg">
<link rel="apple-touch-icon" href="logo/logo-mark.jpg">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "BOCA BOCA",
  "description": "Tapas bar i smash burgery w Rzeszowie \\u2014 hiszpa\\u0144skie przek\\u0105ski, burgery sma\\u017cone na blasze, wino z kranu i ogr\\u00f3dek nad zalewem.",
  "url": "https://bocaboca.pl/",
  "telephone": "+48790394366",
  "email": "biuro@bocaboca.pl",
  "image": "https://bocaboca.pl/img/burger-neon.jpg",
  "servesCuisine": ["Hiszpa\\u0144ska", "Tapas", "Burgery"],
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Kwiatkowskiego 44c, lok. U2",
    "addressLocality": "Rzesz\\u00f3w",
    "postalCode": "35-311",
    "addressCountry": "PL"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 50.0095432, "longitude": 21.9999948 },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.4", "reviewCount": "214" },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "14:00", "closes": "22:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday"], "opens": "12:00", "closes": "22:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday", "Saturday"], "opens": "12:00", "closes": "23:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "12:00", "closes": "22:00" }
  ],
  "sameAs": [
    "https://www.facebook.com/p/BOCA-BOCA-61576581356510/",
    "https://www.instagram.com/bocaboca_rzeszow/"
  ],
  "hasMenu": "https://bocaboca.pl/#menu",
  "acceptsReservations": "https://bocaboca.pl/#kontakt"
}
</script>

<style>
  html { color-scheme: light dark; }
  body { margin: 0; }
  img { max-width: 100%; }
</style>
</head>
<body>
"""

FOOT = "\n</body>\n</html>\n"


def render(inline):
    html = SRC.read_text(encoding="utf-8")

    # logo w nawigacji — podmieniany jest sam atrybut src
    mark = LOGO_DIR / "logo-mark.jpg"
    html = html.replace("__LOGO_MARK__", data_uri(mark) if inline else "logo/logo-mark.jpg")

    # logo w stopce — cały znacznik
    lock = LOGO_DIR / "logo-lockup.jpg"
    w, h = jpeg_size(lock)
    lock_src = data_uri(lock) if inline else "logo/logo-lockup.jpg"
    html = html.replace(
        "__IMG_LOGO_LOCK__",
        '<img class="logo" src="%s" alt="BOCA BOCA — tapas, burger, wine" '
        'width="%d" height="%d" loading="lazy" decoding="async">' % (lock_src, w, h),
    )

    html = html.replace("__GALLERY__", gallery_markup(inline))

    # pozostałe zdjęcia
    def sub(m):
        name = m.group(1)
        cls = "cat-shot" if name in {
            "patatas-bravas", "burger-przekroj", "ciasto-marchewkowe",
            "wino-z-kranu", "koktajle", "piwa",
        } else ""
        return img_tag(name, inline, cls=cls, eager=(name in EAGER))

    html = re.sub(r"__IMG_([a-z0-9\-]+)__", sub, html)

    left = re.findall(r"__[A-Z_]+__", html)
    if left:
        raise SystemExit("niepodmienione zmienne: %s" % sorted(set(left)))
    return html


def main():
    if not SRC.exists():
        raise SystemExit("brak %s" % SRC)

    # 1. wersja serwerowa
    page = render(inline=False)
    body = "\n".join(l for l in page.splitlines() if not l.startswith("<title>"))
    (ROOT / "index.html").write_text(HEAD + body + FOOT, encoding="utf-8")

    # 2. wersja samodzielna
    (ROOT / "page.html").write_text(render(inline=True), encoding="utf-8")

    for f in ("index.html", "page.html"):
        size = (ROOT / f).stat().st_size
        print("%-12s %7.1f KB" % (f, size / 1024))


if __name__ == "__main__":
    main()
