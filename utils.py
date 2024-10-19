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
    "Como usar": "Mudanças da versão 1.0 TAURA",
    "changes" : "Melhorias na sumarização de dados. \n Tabela agora é dividida por cor e não por uma linha vazia",    
    "Tutorial": "TUTORIAL",
    "m1": "Escolha o metatrader que quer usar, colocando o caminho do arquivo \n terminal64.exe",
    "m2": "Escolha o par de moedas, em MAIÚSCULO e sem espaços antes ou depois",
    "m3": "Escolher a hora a ser analisada. Deve estar de acordo com o timeframe escolhido. \n Escolher por exemplo 08:15 em H1 vai dar problema. \nA hora deve ser inserida no formato HH:MM. \n Exemplo: 08:45",
    "m4": "Evite semanal e mensal",
    "m7": "O retorno de informação é de 1 vela ou grupo de velas por dia no timeframe escolhido."
}

def sort_candles(df, target_time, associated_candles_string, candle_count, multiplier, pair, time_frame, days_back):
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
    open_low_list = []
    open_high_list = []
    open_high_list_with_date = []
    open_low_list_with_date = []
    
    def organize_dataframe(filtered_df):
        open_first = filtered_df.iloc[0]['open']  # abertura da primeira vela do grupo
        close_last = filtered_df.iloc[-1]['close']  # fechamento da última vela do grupo
        max_high = max(filtered_df['high'].values)  # maior máximo do grupo
        max_low = min(filtered_df['low'].values)  # menor mínimo do grupo
        date = filtered_df.iloc[0]['time']
        formatted_date = date.strftime('%d-%m (%A)')

        open_high_group = (max_high - open_first) * multiplier
        open_high_list.append(open_high_group.round(2))
        open_high_message = f'{formatted_date} < ------ > {open_high_group.round(2)}'
        open_high_list_with_date.append(open_high_message)

        open_low_group = (max_low - open_first) * multiplier
        open_low_list.append(open_low_group.round(2))

        open_low_message = f'{formatted_date} < ------ > {open_low_group.round(2)}'
        open_low_list_with_date.append(open_low_message)

        high_low_difference = (max_high - max_low) * multiplier
        difference_open_close = (close_last - open_first) * multiplier

        high_low_list.append(high_low_difference.round(2))
        date_hl_diff_rounded = f' {formatted_date} < ------ > {high_low_difference.round(2)} PONTOS'
        high_low_list_with_date.append(date_hl_diff_rounded)

        open_close_list.append(difference_open_close.round(2))
        open_close_with_date.append(f'{formatted_date} < ------ > {difference_open_close.round(2)} PONTOS')

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
            organize_dataframe(filtered_df)
            
        elif associated_candles_string == "Nenhum":
            filtered_df = df.iloc[[target_index]]
            organize_dataframe(filtered_df)
            
    start_index_time = filtered_df.iloc[0]['time']
    start_index_hour = datetime.strptime(str(start_index_time), "%Y-%m-%d %H:%M:%S").time()
    if associated_candles_string in ["Antes"]:
        pair_and_time = f'{pair} vela das {start_index_hour} até {target_time} em {time_frame}'
    elif associated_candles_string == "Depois":
        end_index_time = filtered_df.iloc[-1]['time']
        end_index_hour = datetime.strptime(str(end_index_time), "%Y-%m-%d %H:%M:%S").time()
        pair_and_time = f'{pair} vela das {target_time} até {end_index_hour} em {time_frame}'
    elif associated_candles_string == "Ambos":
        end_index_time = filtered_df.iloc[-1]['time']
        end_index_hour = datetime.strptime(str(end_index_time), "%Y-%m-%d %H:%M:%S").time()
        pair_and_time = f'{pair} vela das {start_index_hour} até {end_index_hour}'
    else:
        pair_and_time = f'{pair} vela das {target_time}'
    
    
    open_close_with_date = '\n'.join(open_close_with_date)
    high_low_list_with_date = '\n'.join(high_low_list_with_date)
    open_low_list_with_date = '\n'.join(open_low_list_with_date)
    open_high_list_with_date = '\n'.join(open_high_list_with_date)
    subiu_grupo = 0
    desceu_grupo = 0
    
    for hlcount in open_close_list:
        if hlcount > 0:
            subiu_grupo += 1
        if hlcount <= 0:
            desceu_grupo +=1
        else:
            singleMessageWindow("Erro", "Erro de valor inválido. Tente novamente ou fale com o desenvolvedor")    
        
    
    #messages displayed based on the results
    largest_movement = f'Maior movimento em cada dia: \n {high_low_list_with_date}'
    
    average_delta_open_close = sum(open_close_list)/len(open_close_list)
    rounded_avg_delta_oc = average_delta_open_close.round(2)
    average_movement_oc = f'Movimentação média da abertura ao fechamento: \n {rounded_avg_delta_oc} pontos'
    
    avg_high_low = sum(high_low_list)/len(high_low_list)
    rounded_avg_high_low = avg_high_low.round(2)
    average_high_low_msg = f'Média do ponto mais alto ao ponto mais baixo: {rounded_avg_high_low}'
    highest_to_lowest = f'Média abertura ao fechamento \n {open_close_with_date}'
    open_to_high_str = f'Abertura até o ponto mais alto \n {open_high_list_with_date}'
    open_to_low_str = f'Abertura até o ponto mais baixo \n {open_low_list_with_date}' 
    
    combined_filtered_df = pd.concat(all_filtered_dfs, ignore_index=True)
    message_object.append(pair_and_time)
    message_object.append(average_movement_oc)
    message_object.append(average_high_low_msg)
    message_object.append(open_to_high_str)
    message_object.append(open_to_low_str)
    message_object.append(largest_movement)
    message_object.append(highest_to_lowest)
    return combined_filtered_df, message_object

 
    