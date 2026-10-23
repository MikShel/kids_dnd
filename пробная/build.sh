#!/bin/bash
# Собирает файлы пробной игры: print/*.html и print/*.pdf
set -e
cd "$(dirname "$0")"
mkdir -p print
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for name in сценарий герой карточки опросник родителям; do
  cls=""; [ "$name" = "сценарий" ] && cls="gm"; [ "$name" = "карточки" ] && cls="cards"
  pandoc "$name.md" -s --embed-resources --css ../print.css -V lang=ru \
    --metadata title="$name" -V pagetitle="$name" \
    -o "print/$name.html"
  if [ -n "$cls" ]; then sed -i '' "s/<body>/<body class=\"$cls\">/" "print/$name.html"; fi
  sed -i '' 's#<header id="title-block-header">.*##; /<h1 class="title">/d; /<\/header>/d' "print/$name.html"
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="print/$name.pdf" "file://$PWD/print/$name.html" 2>/dev/null
done
ls -la print
