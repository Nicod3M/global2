#!/usr/bin/env bash
# Składa page.html (fragment: <title>, <style>, markup) w kompletny index.html
# gotowy do wgrania pod domenę bocaboca.pl.
#
#   ./build.sh
#
# page.html jest jedynym źródłem treści — index.html jest generowany.
set -euo pipefail

cd "$(dirname "$0")"

SRC="page.html"
OUT="index.html"

[ -f "$SRC" ] || { echo "Brak $SRC" >&2; exit 1; }

{
cat <<'HEAD'
<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BOCA BOCA — tapas i smash burgery, Rzeszów</title>
<meta name="description" content="Tapas bar i smash burgery przy Kwiatkowskiego 44c w Rzeszowie. Hiszpańskie przekąski, burgery z blachy, wino i ogródek z widokiem na zalew. Zamów online lub zarezerwuj stolik: 790 394 366.">
<link rel="canonical" href="https://bocaboca.pl/">
<meta name="theme-color" content="#101013">

<meta property="og:type" content="restaurant.restaurant">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="BOCA BOCA">
<meta property="og:title" content="BOCA BOCA — tapas i smash burgery, Rzeszów">
<meta property="og:description" content="Hiszpańskie tapas, smash burgery z blachy i wino. Ogródek z widokiem na zachód słońca nad rzeszowskim zalewem.">
<meta property="og:url" content="https://bocaboca.pl/">
<meta name="twitter:card" content="summary_large_image">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "BOCA BOCA",
  "description": "Tapas bar i smash burgery w Rzeszowie — hiszpańskie przekąski, burgery smażone na blasze, wino i ogródek nad zalewem.",
  "url": "https://bocaboca.pl/",
  "telephone": "+48790394366",
  "email": "biuro@bocaboca.pl",
  "servesCuisine": ["Hiszpańska", "Tapas", "Burgery"],
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Kwiatkowskiego 44c, lok. U2",
    "addressLocality": "Rzeszów",
    "postalCode": "35-311",
    "addressCountry": "PL"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 50.0095432,
    "longitude": 21.9999948
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.4",
    "reviewCount": "214"
  },
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
  "hasMenu": "https://www.ubereats.com/pl/store/boca-boca-rzeszow/ajPMjgy_U4iiRHnPGe-Tnw",
  "acceptsReservations": "https://bocaboca.pl/#kontakt"
}
</script>

<style>
  html { color-scheme: dark light; }
  body { margin: 0; }
  img { max-width: 100%; }
</style>
</head>
<body>
HEAD

# fragment bez linii <title> — tytuł siedzi już w <head>
grep -v '^<title>' "$SRC"

cat <<'FOOT'
</body>
</html>
FOOT
} > "$OUT"

echo "Zbudowano $OUT ($(wc -c < "$OUT") bajtów)"
