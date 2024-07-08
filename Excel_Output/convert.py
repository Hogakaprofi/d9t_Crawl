import os
import pandas as pd

# Liste von Dateipfaden, die überprüft werden sollen
file_paths = [
    '../grimmgastro/grimmgastro.json',
    '../schafferer/schafferer.json'
]

output = './'

for file_path in file_paths:
    if os.path.exists(file_path):
        try:
            # Lade die JSON-Daten in einen Pandas DataFrame
            df = pd.read_json(file_path)

            # Erstelle einen Namen für die Excel-Datei
            excel_file = os.path.splitext(os.path.basename(file_path))[0] + '.xlsx'
            excel_path = os.path.join(output, excel_file)

            # Speichern als Excel-Datei mit UTF-8 Encoding
            df.to_excel(excel_path, index=False, engine='openpyxl')  # Hier 'openpyxl' oder 'xlsxwriter' verwenden

            print(f'Daten aus {file_path} erfolgreich als Excel (UTF-8) gespeichert.')
        except Exception as e:
            print(f'Fehler beim Verarbeiten der Datei {file_path}: {e}')
    else:
        print(f'Datei {file_path} nicht gefunden.')

#-----------------------------------------------------------------------------------------------------------------------
# import pandas as pd
#
# # Pfad zur JSON-Datei
# json_file = 'schafferer.json'
#
# # Lade die JSON-Daten in einen Pandas DataFrame
# df = pd.read_json(json_file)
#
# # Speichern als CSV-Datei mit UTF-8 Encoding
# # csv_file = 'ausgabe.csv'
# # df.to_csv(csv_file, index=False, encoding='utf-8')
#
# # Speichern als Excel-Datei mit UTF-8 Encoding
# excel_file = 'schafferer.xlsx'
# df.to_excel(excel_file, index=False, engine='openpyxl')  # Hier 'openpyxl' oder 'xlsxwriter' verwenden
#
# print(f'Daten erfolgreich als Excel (UTF-8) gespeichert.')
