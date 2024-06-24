import pandas as pd

# Pfad zur JSON-Datei
json_file = 'grimmgasto.json'

# Lade die JSON-Daten in einen Pandas DataFrame
df = pd.read_json(json_file)

# Speichern als CSV-Datei mit UTF-8 Encoding
# csv_file = 'ausgabe.csv'
# df.to_csv(csv_file, index=False, encoding='utf-8')

# Speichern als Excel-Datei mit UTF-8 Encoding
excel_file = 'grimmgasto.xlsx'
df.to_excel(excel_file, index=False, engine='openpyxl')  # Hier 'openpyxl' oder 'xlsxwriter' verwenden

print(f'Daten erfolgreich als Excel (UTF-8) gespeichert.')
