import pandas as pd
import json 
def load_and_clean_data(file_path):
    # Carica i dati
    df = pd.read_json(file_path, lines=True)

    # Espandi l'array 'samples' in righe separate
    rows = []
    for _, row in df.iterrows():
        for sample in row['samples']:
            # Converti la stringa in un dizionario se necessario
            if isinstance(sample, str):
                sample = json.loads(sample)
    
    # Estrai i dati dal sample
            sensor_name = sample['name'].split('_')[-1] if 'name' in sample else None
            sensor_value = sample['value'] if 'value' in sample else None
            sensor_time = pd.to_datetime(sample['time']['$numberLong'], unit='ms') if 'time' in sample else None

            # Aggiungi al DataFrame
            rows.append({'folder': row['folder'], 'sensor_name': sensor_name, 'sensor_value': sensor_value, 'sensor_time': sensor_time})

    new_df = pd.DataFrame(rows)

    return new_df

# Carica il dataset
file_path = './eqtq.json'
df = load_and_clean_data(file_path)

# Visualizza le prime righe del dataframe per conferma
print(df.head())
"""
    # Carica i dati
    df = pd.read_csv(file_path)

    # Espandi l'array 'samples' in righe separate
    #df = df.explode('samples')
    #print(df.head()['samples'][0])

    # Assicurati che ogni elemento in 'samples' sia un dizionario
    #df['samples'] = df['samples'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    samples = df.drop('samples', axis=1).join(pd.json_normalize(df['samples']).explode('samples').reset_index(drop=True))

    #print(df['samples'])
    # Estrai informazioni dai campi nidificati
    def lam_name(x):
        #print(x)
        #print(x[0]['name'])
        for i in x:
            if i and i['name']:
                return i['name'].split('_')[-1]
        else:
                return None
    def lam_value(x):
        #print(x)
        #print(x[0]['name'])
        for i in x:
            if i and i['value']:
                return i['value']
        else:
                return None
    
    def lam_time(x):
        #print(x)
        #print(x[0]['name'])
        for i in x:
            if i and i['time']:
                
                #return i['time']
                return pd.to_datetime(i['time'], unit = 'ms')
        else:
                return None
        
    df['sensor_name'] = samples.apply(lam_name)
    df['sensor_value'] = samples.apply(lam_value)
    df['sensor_time'] = samples.apply(lam_time)

    # Elimina la colonna 'samples' e altre colonne non necessarie
    df = df.drop(columns=['samples', '_id', 'day', 'first_time', 'last_time', 'nsamples'])

    # Riordina le colonne se necessario
    df = df[['sensor_time', 'folder', 'sensor_name', 'sensor_value']]

    return df

# Carica il dataset
file_path = './arol.csv'
df = load_and_clean_data(file_path)

# Visualizza le prime righe del dataframe per conferma
print(df)
"""