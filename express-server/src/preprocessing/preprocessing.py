import pandas as pd
import json 

import pandas as pd

def merge_csv_files(file1, file2, output_file):
    # Carica i due file CSV
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
     

    
    # Concatena i due DataFrame
    merged_df = pd.concat([df1, df2], ignore_index=True, sort=False)

    # Salva il DataFrame unito in un nuovo file CSV
    merged_df.to_csv(output_file, index=False)

    print(f"File merged and saved as '{output_file}'")

def load_and_clean_data(file_path):
    # Carica i dati
    df = pd.read_csv(file_path)

    # Espandi l'array 'samples' in righe separate
    df = df.explode('samples')
    df = df.dropna(subset=['first_time', 'last_time'])

    # Assicurati che ogni elemento in 'samples' sia un dizionario
    df['samples'] = df['samples'].apply(lambda x: eval(x) if isinstance(x, str) else x)

    # Crea un nuovo dataframe per i dati espansi
    expanded_data = []
    for index, row in df.iterrows():
        for sample in row['samples']:
            if sample and 'name' in sample and 'value' in sample and 'time' in sample:
                expanded_data.append({
                    'type': row['folder'],
                    '_id': row['_id'],
                    'sensor_name': sample['name'].split('_')[-1],
                    'sensor_value': sample['value'],
                    'sensor_time': pd.to_datetime(sample['time'], unit='ms')
                })
            elif sample and 'value' in sample and 'time' in sample and row['variable']:
                print(sample, row['variable'])
                expanded_data.append({
                    'type': 'PLC',
                    '_id': row['_id'],
                    'sensor_name': row['variable'],
                    'sensor_value': sample['value'],
                    'sensor_time': pd.to_datetime(sample['time'], unit='ms')
                })

    # Crea un nuovo DataFrame dai dati espansi
    expanded_df = pd.DataFrame(expanded_data)

    # Riordina le colonne se necessario
    expanded_df = expanded_df[['sensor_time', 'sensor_name', 'sensor_value', 'type']]

    return expanded_df

# Percorsi dei file sorgente
file1 = './arol.csv'
file2 = './arol_drive.csv'
file3 = './arol_plc.csv'

# Percorso del file di output
output_file_1 = './merged_arol_1.csv'
output_file_2 = './merged_arol_final.csv'

# Esegui la funzione di unione
merge_csv_files(file1, file2, output_file_1)
merge_csv_files(output_file_1, file3, output_file_2)
# Carica il dataset
file_path = output_file_2

df = load_and_clean_data(file_path)

# Visualizza le prime righe del dataframe per conferma
print(df)
