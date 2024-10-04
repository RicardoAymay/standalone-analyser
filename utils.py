from main import singleMessageWindow
import pandas as pd
from datetime import datetime

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


message_list = {
    "Como usar": "Mudanças da versão 0.6beta",
    "m1": "Escolha o metatrader que quer usar, colocando o caminho do arquivo \n terminal64.exe",
    "m2": "Escolha o par de moedas, em MAIÚSCULO e sem espaços antes ou depois",
    "m3": "Escolher a hora a ser analisada. Deve estar de acordo com o timeframe escolhido. \n Escolher por exemplo 08:15 em H1 vai dar problema. \nA hora deve ser inserida no formato HH:MM. \n Exemplo: 08:45",
    "m4": "Evite semanal e mensal",
    "m7": "O retorno de informação é de 1 vela ou grupo de velas por dia no timeframe escolhido."
}

def sort_candles(df, target_time, associated_candles_string, candle_count, multiplier, pair, time_frame):
    matching_indices = df.index[df['time'].dt.time == target_time].tolist()
    
    if not matching_indices:
        singleMessageWindow("Erro", "Nenhuma vela encontrada para o tempo especificado.")
        return None

    all_filtered_dfs = []
    open_close_list = []
    open_close_with_date = []
    message_object = []
    high_low_list = []
    high_low_list_with_date = []
    def organize_dataframe(filtered_df):
        open_first = filtered_df.iloc[0]['open'] #abertura da primeira vela do grupo
        close_last = filtered_df.iloc[-1]['close'] #fechamento da última vela do grupo
        max_high = max(filtered_df['high'].values) #maior máximo do grupo
        max_low = min(filtered_df['low'].values) #menor mínimo do grupo
        date = filtered_df.iloc[0]['time']
        formatted_date = date.strftime('%d-%m (%A)')
        high_low_difference = (max_high-max_low)*multiplier       
        difference_open_close = (open_first - close_last)*multiplier
        high_low_list.append(high_low_difference.round(2))
        high_low_list_with_date.append(f'{formatted_date} -------------------------> {high_low_difference.round(2)} PONTOS')
        open_close_list.append(difference_open_close.round(2))
        open_close_with_date.append(f'{formatted_date} -------------------------> {difference_open_close.round(2)} PONTOS')
        empty_row = pd.DataFrame([[None] * len(filtered_df.columns)], columns=filtered_df.columns)
        filtered_df = pd.concat([filtered_df, empty_row], ignore_index=True)
        all_filtered_dfs.append(filtered_df)
        return filtered_df
    for target_index in matching_indices:
        if associated_candles_string == "Antes":
            start_index = max(0, target_index - candle_count) #onde começa a seleção do grupo
            filtered_df = df.iloc[start_index:target_index + 1] #onde termina a seleção do grupo
            organize_dataframe(filtered_df)
            
        elif associated_candles_string == "Depois":
            filtered_df = df.iloc[target_index: target_index + candle_count]
            organize_dataframe(filtered_df)
        elif associated_candles_string == "Ambos":
            start_index = max(0, target_index - candle_count)
            end_index = target_index + candle_count
            filtered_df = df.iloc[start_index:end_index + 1]
            all_filtered_dfs.append(filtered_df)
        elif associated_candles_string == "Nenhum":
            filtered_df = df.iloc[[target_index]]
            all_filtered_dfs.append(filtered_df)
    start_index_time = filtered_df.iloc[0]['time']
    start_index_hour = datetime.strptime(str(start_index_time), "%Y-%m-%d %H:%M:%S").time()
    if associated_candles_string in ["Antes", "Ambos"]:
        pair_and_time = f'{pair} vela das {start_index_hour} até {target_time} em {time_frame}'
    elif associated_candles_string == "Depois":
        pair_and_time = f'{pair} vela das {target_time} até {start_index_hour} em {time_frame}'
        pass
    else:
        pair_and_time = f'{pair} vela das {target_time}'
    
    largest_movement = f'Maior movimento em cada dia: \n {high_low_list_with_date}'
    median_movement = f'Movimentação média da abertura ao fechamento: \n {sum(open_close_list)/len(open_close_list)} pontos'
    median_high_low = f'Movimentação média de máximo e mínimo: {sum(high_low_list)/len(high_low_list)}'
    highest_to_lowest = f'Movimentação da abertura ao fechamento \n {open_close_with_date}'
    
    combined_filtered_df = pd.concat(all_filtered_dfs, ignore_index=True)
    message_object.append(pair_and_time)
    message_object.append(median_movement)
    message_object.append(median_high_low)
    message_object.append(largest_movement)
    message_object.append(highest_to_lowest)
    return combined_filtered_df, message_object

 
    