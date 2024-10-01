from tkinter import *
from tkinter import font
from tkinter import ttk
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import threading
from utils import *

def singleMessageWindow(title, message):
    window = Tk()
    window.title(title)
    window.geometry('450x200')
    window.configure(bg='#f0f0f0')

    common_font = font.Font(family="Helvetica", size=12)
    lbl = Label(window, text=message, bg='#f0f0f0', font=common_font, wraplength=400)
    lbl.pack(padx=20, pady=20)

    window.mainloop()


def textWindow(title, message_object):
    window = Tk()
    window.title(title)
    window.geometry('550x700')
    window.configure(bg='#f0f0f0')
    for text_line in message_object:
        lbl = Label(window, text=text_line, bg='#f0f0f0', font=font.Font(family="Helvetica", size=10), wraplength=400)
        lbl.pack(padx=20, pady=20)
    window.mainloop()


def labeledEntry(window, text, row, column, initial_value, width=50):
    lbl = Label(window, text=text, bg='#f0f0f0', font=font.Font(family="Helvetica", size=12))
    lbl.grid(column=column, row=row, padx=10, pady=5, sticky="ew")
    entry = Entry(window, width=width, font=font.Font(family="Helvetica", size=12))
    entry.insert(0, initial_value)
    entry.grid(column=column, row=row+1, padx=10, pady=5, sticky="ew")

    # Make the label and entry widgets responsive
    window.grid_columnconfigure(column, weight=1)
    window.grid_rowconfigure(row, weight=1)
    window.grid_rowconfigure(row+1, weight=1)

    return entry
    
#primeira tela
welcome_message = "Bem vindo ao analisador de estratégia V0.5 alpha"

def startWindow():
    window = Tk()
    window.title(welcome_message)
    window.geometry('500x200')  
    window.configure(bg='#f0f0f0')  
    
    metaTraderPath = labeledEntry(window, "Escolha o MT5 que deseja analisar", row=0, column=0, initial_value="C:/Program Files/MetaTrader 5/terminal64.exe")
    metaTraderPath.focus()
    
    def onClickNext():
        path = metaTraderPath.get()
        closeWindowAndConnect(window, path)
    
    btnProximaTela = Button(window, text="Próximo", command=onClickNext, cursor="hand2", font=font.Font(family="Helvetica", size=12, weight="bold"))
    btnProximaTela.grid(column=0, row=3, padx=10, pady=15, sticky="ew")
    
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(3, weight=1)
  
    window.mainloop()


def main():
    startMessageObject = [
    f'{welcome_message} \n',
    ]
    for message in message_list.values():
        startMessageObject.append(f'{message} \n')
    text_window_thread = threading.Thread(target=textWindow, args=("Bem vindo!", startMessageObject))
    text_window_thread.start()
    startWindow()

#segunda tela
def currencyPairWindow():
    window = Tk()
    window.title("Escolha o Par de Moedas")
    window.geometry('850x650')
    window.configure(bg='#f0f0f0')

    analyzer_object_pair = "Escolha o par de moedas que deseja analisar"
    analyzer_object_timeframe = "Escolha o timeframe"
    analyzer_object_time = "Escolha a hora (HH:MM) para analisar \n Deve estar de acordo com o timeframe"
    analyzer_object_days = "Desde quando? Inserir número de dias"
    analyser_object_associated_candles_string = "Antes, depois, ambos ou nenhum?"
    analyser_object_associated_candles_number = "Quantas velas associadas deseja analisar?"
    analyser_object = {
        analyzer_object_pair: "EURUSD",
        analyzer_object_timeframe: "M5",
        analyzer_object_time: "08:00",
        analyzer_object_days: "10",
        analyser_object_associated_candles_string: ["Antes", "Depois", "Ambos", "Nenhum"],
        analyser_object_associated_candles_number: 0
    }
    
    entries = {}
    for i, (label, default_value) in enumerate(analyser_object.items()):
            entries[label] = labeledEntry(window, label, row=i*2, column=0, initial_value=default_value)

    def onClickAnalyze():
        if not mt5.initialize():
            singleMessageWindow("Erro", "Erro ao conectar ao MetaTrader 5.")
            return
        pair = entries[analyzer_object_pair].get().upper()  # Get the currency pair and convert to uppercase
        if not pair:
            singleMessageWindow("TÁ VAZIO", "Não tem moeda fantasma. Escreve ali!")
            return
        
        if not mt5.symbol_info(pair):
            singleMessageWindow("ERRO", f'{pair} tá errado. Analfabeto! \n E quem disse foi o próprio MetaTrader 5.')
            return
        
        time_frame = entries[analyzer_object_timeframe].get().upper()  # Get the timeframe and convert to uppercase
        if not time_frame:
            singleMessageWindow("TÁ VAZIO", "Não sou vidente. Escreve o timeframe!")
            return
        
        metatrader_timeframes = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1"]
        if time_frame not in metatrader_timeframes:
            singleMessageWindow("ERRO", "Timeframe errado. Escolha um dos seguintes: M1, M5, M15, M30, H1, H4, D1, W1, MN1")
            return
        
        time = entries[analyzer_object_time].get()  # Get the time
        if not time:
            singleMessageWindow("TÁ VAZIO", "Não sou vidente. Escreve a hora!") 
            return
        
        days_back_str = entries[analyzer_object_days].get()  # Get the number of days
        if not days_back_str:
            singleMessageWindow("TÁ VAZIO", "Não sou vidente. Escreve a quantidade de dias!") 
            return
        
        try:
            days_back = int(days_back_str)
        except ValueError:
            singleMessageWindow("ERRO", "A quantidade de dias deve ser um número inteiro!")
            return

        if days_back < 0:
            days_back = abs(days_back)
        
        analyzer_candles_1 = entries[analyser_object_associated_candles_string].get()
        if not analyzer_candles_1:
            singleMessageWindow("TÁ VAZIO", "Não sou vidente. Escreve antes, depois, ambos ou nenhum!") 
            return
        
        if analyzer_candles_1 not in ["Antes", "Depois", "Ambos", "Nenhum"]:
            singleMessageWindow("ERRO", "Escreve antes, depois, ambos ou nenhum! \n Primeira letra maiúscula, por favor.") 
            return
        
        associated_candles = 0
        candle_numbers_str = entries[analyser_object_associated_candles_number].get()
        if analyzer_candles_1 != "Nenhum":
            if not candle_numbers_str:
                singleMessageWindow("TÁ VAZIO", "Não sou vidente. Escreve a quantidade de velas!") 
                return
            
            try:
                candle_numbers = int(candle_numbers_str)
            except ValueError:
                singleMessageWindow("ERRO", "A quantidade de velas deve ser um número inteiro!")
                return

            if candle_numbers < 0:
                singleMessageWindow("ERRO", "Eu podia tornar positivo automaticamente pra você, mas não quis. Escreve um número positivo!")
                return
            
            associated_candles = candle_numbers
        
        result = pairAnalysisPattern(pair, time, days_back, time_frame, associated_candles, analyzer_candles_1)
        print(result)
        if result is not None:
            displayResults(result, pair, time_frame, analyzer_candles_1)
        else:
            singleMessageWindow("Erro", "Deu ruim")

    btnAnalisar = Button(window, text="Analisar", command=onClickAnalyze, cursor="hand2", font=font.Font(family="Helvetica", size=12))
    btnAnalisar.grid(column=0, row=len(analyser_object)*2, padx=10, pady=10, sticky="ew")

    window.mainloop()
   
    
def closeWindowAndConnect(window, path):
    
    if mt5.initialize(path):
        print("Conectado com sucesso!")
        window.destroy()
        currencyPairWindow()
    else:
        error_code = mt5.last_error()
        singleMessageWindow("Erro", f"Erro ao conectar ao MetaTrader 5. Código de erro:\n {error_code}")
        

def pairAnalysisPattern(pair, target_time_str, days_back, time_frame, associated_candles_number=0, associated_candles_string="Nenhum"):
    if not mt5.initialize():
        singleMessageWindow("Erro", "Erro ao conectar ao MetaTrader 5.")
        return None
    
    target_time = datetime.strptime(target_time_str, "%H:%M").time() # vela escolhida para análise

    start_date = datetime.now() - timedelta(days=days_back)
    start_date = start_date.replace(hour=target_time.hour, minute=target_time.minute, second=0, microsecond=0)
    
    time_frame_value = getattr(mt5, f'TIMEFRAME_{time_frame}')
    if time_frame == "MN" or time_frame == "W1":
        number_of_candles = days_back
    else:
        number_of_candles = DAYS_CANDLE_COUNTER.get(time_frame) * days_back  
    
    rates = mt5.copy_rates_from(pair, time_frame_value, start_date, number_of_candles)
    if rates is None or len(rates) == 0:
        print("Não foi possível recuperar as taxas para o par de moedas especificado.")
        mt5.shutdown()
        return None
    
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return get_associated_candles(df, target_time, associated_candles_string, associated_candles_number, pair)
    

def get_associated_candles(df, target_time, associated_candles_string, candle_count, pair):

    combined_filtered_df = sort_candles(df, target_time, associated_candles_string, candle_count)
    
    multiplier = 10 ** mt5.symbol_info(pair).digits
    reduced_df = combined_filtered_df.drop(columns=['real_volume', 'spread', 'tick_volume'])
    reduced_df['direction'] = reduced_df.apply(lambda row: "subiu" if pd.notna(row['open']) and pd.notna(row['close']) and row['close'] > row['open'] 
                                               else ("desceu" if pd.notna(row['open']) and pd.notna(row['close']) and row['close'] < row['open'] 
                                               else None), axis=1)
    reduced_df['delta'] = reduced_df['close'] - reduced_df['open']
    reduced_df['delta'] = reduced_df['delta'].abs() * multiplier
    reduced_df['subida máxima'] = reduced_df.apply(lambda row: row['high'] - row['open'], axis=1).round(5) * multiplier
    reduced_df['queda máxima'] = reduced_df.apply(lambda row: row['open'] - row['low'], axis=1).round(5) * multiplier
    reduced_df[['open', 'high', 'low', 'close', 'delta']] = reduced_df[['open', 'high', 'low', 'close', 'delta']].round(5)

    mt5.shutdown()
    
    return reduced_df

#terceira e quarta tela
def displayResults(dataframe, pair, timeframe, associated_candles_string):
    if dataframe is None or dataframe.empty:
        singleMessageWindow("Erro", "Nenhum dado disponível para exibir.")
        return
    
    # Initialize the window and display the table
    results_window = Tk()
    results_window.title("Resultados da Análise")
    results_window.geometry('800x400+700+100')
    results_window.configure(bg='#f0f0f0')
    results_window.grid_columnconfigure(0, weight=1)
    results_window.grid_rowconfigure(0, weight=1)

    tree = ttk.Treeview(results_window)
    tree["columns"] = list(dataframe.columns)
    tree["show"] = "headings"

    for col in dataframe.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for index, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(expand=True, fill='both')

    scrollbar_y = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
    scrollbar_y.pack(side=RIGHT, fill=Y)
    tree.config(yscrollcommand=scrollbar_y.set)

    scrollbar_x = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
    scrollbar_x.pack(side=BOTTOM, fill=X)
    tree.config(xscrollcommand=scrollbar_x.set)
    
    # Analyze the groups separated by NaN rows
    total_candles = len(dataframe[pd.notna(dataframe['time'])])
    data_groups = []
    
    # Identify groups based on NaN rows
    mask = pd.notna(dataframe['time'])
    group_boundaries = mask.ne(mask.shift()).cumsum()  # Group by consecutive non-NaN rows
    grouped = dataframe.groupby(group_boundaries)
    
    # Perform analysis on each group
    message_object = []
    for group_num, group in grouped:
        if pd.isna(group['time']).all():
            continue  # Skip empty groups
        
        # Find the first candle's open and the last candle's close
        start_time = group['time'].iloc[0]
        end_time = group['time'].iloc[-1]
        first_open = group['open'].iloc[0]
        last_close = group['close'].iloc[-1]
        
        total_subiu = len(group[group["direction"] == "subiu"])
        total_desceu = len(group[group["direction"] == "desceu"])
        percentage_up = total_subiu / len(group) * 100
        percentage_down = total_desceu / len(group) * 100
        delta_mean = group["delta"].mean()
        
        # Add group analysis to the message_object
        message_object.append(f'Análise de {start_time} até {end_time}:')
        message_object.append(f'Primeira vela: {first_open}, Última vela: {last_close}')
        message_object.append(f'Número de candles que subiram: {total_subiu}, Número de candles que desceram: {total_desceu}')
        message_object.append(f'Média de delta (abertura-fechamento): {delta_mean}')
        message_object.append(f'Subiu (%): {percentage_up:.2f}%, Desceu (%): {percentage_down:.2f}%')
        message_object.append('')  # Add a blank line between groups

    # Display the message object in a new window
    textWindow("Resultado", message_object)
    
    mt5.shutdown()
    results_window.mainloop()



if __name__ == "__main__":
    main()
    
