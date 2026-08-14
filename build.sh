#!/usr/bin/env bash
# Cienka nakładka na build.py — opis w komentarzu tamtego pliku.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 build.py
