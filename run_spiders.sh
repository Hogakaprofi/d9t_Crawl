#!/bin/bash

# Arrays initialisieren test
paths=("/home/user/crawl/d9t_Crawl/grimmgastro" "/home/user/crawl/d9t_Crawl/schafferer/" "/home/user/crawl/d9t_Crawl/toptable" "/home/user/crawl/d9t_Crawl/edgarfuchs" "/home/user/crawl/d9t_Crawl/hinschegastrowelt" "/home/user/crawl/d9t_Crawl/dueGuenther") # Pfade, die durchgegangen werden sollen
spiders=("grimm" "schaff" "ttable" "edgar" "hinsche" "guenther") # Namen der Spider-Befehle
pathjson=("/home/user/crawl/d9t_Crawl/grimmgastro/grimmgastro.json" "/home/user/crawl/d9t_Crawl/schafferer/schafferer.json" "/home/user/crawl/d9t_Crawl/toptable/toptable.json" "/home/user/crawl/d9t_Crawl/edgarfuchs/edgarfuchs.json" "/home/user/crawl/d9t_Crawl/hinschegastrowelt/hinschegastro.json" "/home/user/crawl/d9t_Crawl/dueGuenther/guenther.json")

# Anzahl der Pfade und Spider-Namen überprüfen
num_paths=${#paths[@]}
num_spiders=${#spiders[@]}

if [ $num_paths -ne $num_spiders ]; then
  echo "Die Anzahl der Pfade und Spider-Namen muss übereinstimmen."
  exit 1
fi


echo "Virtual Enviroment aktivieren!"
source /home/user/crawl/d9t_Crawl/myenv/bin/activate

# Durch die Pfade und Spider-Namen iterieren
for ((i=0; i<num_paths; i++)); do
  path=${paths[$i]}
  spider=${spiders[$i]}
  pjson=${pathjson[$i]}

  if [ -d "$path" ]; then

    if [ -d "$pjson" ]; then
        echo "json-datei $pjson wird jetzt geleert!"
        > "$pjson"
    else
      echo "Datei nicht gefunden"
    fi
    echo "-------------------------------------------------------------------------------"

    echo "Wechseln in das Verzeichnis: $path"
    cd "$path" || { echo "Kann in das Verzeichnis $path nicht wechseln"; exit 1; }
    pwd

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

echo "Alle Spider erfolgreich durchlaufen/ausgeführt."

echo "-------------------------------------------------------------------------------"

echo "Convert.py ausführen!"
python3 /home/user/crawl/d9t_Crawl/Excel_Output/convert.py
echo "Alle json dateien in Excel-Dateien umgewandelt. Bzw. convert.py ausgeführt!"

echo "Deaktiviere Virtual Enviroment"

deactivate