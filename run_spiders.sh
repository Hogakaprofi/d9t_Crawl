#!/bin/bash

# Arrays initialisieren
paths=("/home/user/crawl/d9t_Crawl/grimmgastro" "/home/user/crawl/d9t_Crawl/schafferer/" "/home/user/crawl/d9t_Crawl/toptable" "/home/user/crawl/d9t_Crawl/edgarfuchs" "/home/user/crawl/d9t_Crawl/hinschegastrowelt" "/home/user/crawl/d9t_Crawl/dueGuenther") # Pfade, die durchgegangen werden sollen
spiders=("grimm" "schaff" "ttable" "edgar" "hinsche" "guenther") # Namen der Spider-Befehle

# Anzahl der Pfade und Spider-Namen überprüfen
num_paths=${#paths[@]}
num_spiders=${#spiders[@]}

if [ $num_paths -ne $num_spiders ]; then
  echo "Die Anzahl der Pfade und Spider-Namen muss übereinstimmen."
  exit 1
fi

source home/user/crawl/d9t_Crawl/myenv/bin/activate

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

echo "Alle Spider erfolgreich ausgeführt."

echo ""

python3 /home/user/crawl/d9t_Crawl/Excel_Output/convert.py

echo "Alle json dateien in Excel-Dateien umgewandelt. Bzw. convert.py ausgeführt!"
