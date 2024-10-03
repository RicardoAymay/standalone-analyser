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
    "mudancas": "Mudanças da versão 0.5beta",
    "m1": "Alterado nome 'divergência' para 'delta'.",
    "m2": "Exóticos e criptos podem ser analisados",
    "m3": "Tela de boas vindas adicionada",
    "m4": "Escolha de timeframe adicionada",
    "m5": "Renomeada 'divergência' para delta, que é a diferença entre abertura e fechamento da vela.",
    "m6": "A hora deve ser inserida no formato HH:MM. \n Exemplo: 08:45",
    "m7": "O retorno de informação é de 1 vela por dia no timeframe escolhido."
}

def sort_candles(df, target_time, associated_candles_string, candle_count, multiplier, pair, time_frame):
    matching_indices = df.index[df['time'].dt.time == target_time].tolist()
    
    if not matching_indices:
        singleMessageWindow("Erro", "Nenhuma vela encontrada para o tempo especificado.")
        return None

    all_filtered_dfs = []
    open_close_list = []
    message_object = []
    high_low_list = []
    def organize_dataframe(filtered_df):
        open_first = filtered_df.iloc[0]['open'] #abertura da primeira vela do grupo
        close_last = filtered_df.iloc[-1]['close'] #fechamento da última vela do grupo
        add_high = max(filtered_df['high'].values) #maior máximo do grupo
        add_low = min(filtered_df['low'].values) #menor mínimo do grupo
        date = filtered_df.iloc[0]['time']
        formatted_date = date.strftime('%d-%m (%A)')
        high_low_difference = (add_high-add_low)*multiplier       
        difference_open_close = (open_first - close_last)*multiplier
        high_low_list.append(f'{formatted_date} -------------------------> {high_low_difference.round(2)} PONTOS')
        open_close_list.append(difference_open_close.round(2))
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
    open_close_movement = f'Movimentação Abertura -> Fechamento: {max(open_close_list)}'
    largest_movement = f'Maior movimento em cada dia: \n {high_low_list}'
    median_movement = f'Movimentação média: {sum(open_close_list)/len(open_close_list)}'
    highest_to_lowest = f'Maior movimentação no intervalo \n (ponto mais alto -> ponto mais baixo) \n {open_close_list}'
    
    combined_filtered_df = pd.concat(all_filtered_dfs, ignore_index=True)
    message_object.append(pair_and_time)
    message_object.append(open_close_movement)
    message_object.append(median_movement)
    message_object.append(largest_movement)
    message_object.append(highest_to_lowest)
    return combined_filtered_df, message_object

 
    