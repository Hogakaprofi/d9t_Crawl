#!/bin/bash

# Arrays initialisieren
paths=("/pfad/zu/ordner1" "/pfad/zu/ordner2") # Pfade, die durchgegangen werden sollen
spiders=("spider1" "spider2") # Namen der Spider-Befehle

# Anzahl der Pfade und Spider-Namen überprüfen
num_paths=${#paths[@]}
num_spiders=${#spiders[@]}

if [ $num_paths -ne $num_spiders ]; then
  echo "Die Anzahl der Pfade und Spider-Namen muss übereinstimmen."
  exit 1
fi

# Durch die Pfade und Spider-Namen iterieren
for ((i=0; i<num_paths; i++)); do
  path=${paths[$i]}
  spider=${spiders[$i]}

  if [ -d "$path" ]; then
    echo "Wechseln in das Verzeichnis: $path"
    cd "$path" || { echo "Kann in das Verzeichnis $path nicht wechseln"; exit 1; }

    echo "Führe Scrapy-Befehl aus: scrapy crawl $spider"
    scrapy crawl $spider # Führe den Spider-Befehl aus

    if [ $? -eq 0 ]; then
      echo "Scrapy-Befehl für Spider $spider erfolgreich ausgeführt."
    else
      echo "Fehler beim Ausführen des Scrapy-Befehls für Spider $spider."
      exit 1
    fi

    # Zurück ins ursprüngliche Verzeichnis
    cd - > /dev/null
  else
    echo "Verzeichnis $path existiert nicht."
    exit 1
  fi
done

echo "Alle Befehle erfolgreich ausgeführt."
