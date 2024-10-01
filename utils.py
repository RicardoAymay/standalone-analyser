from main import singleMessageWindow
import pandas as pd
import numpy as np

DAYS_CANDLE_COUNTER = {
    "M1": 1440,
    "M5" : 288,
    "M15" : 96,
    "M30" : 48,
    "H1" : 24,
    "H4" : 6,
    "D1" : 1,
    "W1" : 1,
}

def getAssociatedCandles():
    pass

message_list = {
    "mudancas": "Mudanças da versão 0.5beta",
    "m1": "Alterado nome 'divergência' para 'delta'.",
    "m2": "Exóticos e criptos podem ser analisados",
    "m3": "Tela de boas vindas adicionada",
    "m4": "Escolha de timeframe adicionada",
    "m5": "Renomeada 'divergência' para delta, que é a diferença entre abertura e fechamento da vela.",
    "m6": "A hora deve ser inserida no formato HH:MM. \n Exemplo: 08:45",
    "m7": "O retorno de informação é de 1 vela por dia no timeframe escolhido."
}

def sort_candles(df, target_time, associated_candles_string, candle_count):
    matching_indices = df.index[df['time'].dt.time == target_time].tolist()
    
    if not matching_indices:
        singleMessageWindow("Erro", "Nenhuma vela encontrada para o tempo especificado.")
        return None

    all_filtered_dfs = []
    empty_row = pd.DataFrame([np.nan] * len(df.columns)).T
    empty_row.columns = df.columns
    for target_index in matching_indices:

        if associated_candles_string == "Antes":
            start_index = max(0, target_index - candle_count)
            filtered_df = df.iloc[start_index:target_index + 1]
            all_filtered_dfs.append(filtered_df)

        elif associated_candles_string == "Depois":
            filtered_df = df.iloc[target_index: target_index + candle_count]
            all_filtered_dfs.append(filtered_df)

        elif associated_candles_string == "Ambos":
            start_index = max(0, target_index - candle_count)
            end_index = target_index + candle_count
            filtered_df = df.iloc[start_index:end_index + 1]
            all_filtered_dfs.append(filtered_df)

        elif associated_candles_string == "Nenhum":
            filtered_df = df.iloc[[target_index]]
            all_filtered_dfs.append(filtered_df)
        all_filtered_dfs.append(empty_row)
            
    # Combine all the filtered dataframes into one, or return them as a list if needed
    combined_filtered_df = pd.concat(all_filtered_dfs)
    return combined_filtered_df
 
    