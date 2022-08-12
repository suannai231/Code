import multiprocessing
import pandas as pd
import datetime
import os
import sys
from multiprocessing import Pool
import numpy as np
from datetime import timedelta
import time
import logging
import math

processed_data_path="//jack-nas/Work/Python/ProcessedData/"
screened_data_path="//jack-nas/Work/Python/ScreenedData/"

def screen(df,lines):

    close = df.iloc[-1]['close']
    ema5 = df.iloc[-1]['EMA5']
    ema10 = df.iloc[-1]['EMA10']
    ema20 = df.iloc[-1]['EMA20']
    ema60 = df.iloc[-1]['EMA60']
    ema120 = df.iloc[-1]['EMA120']
    ema250 = df.iloc[-1]['EMA250']
    # OBV = df.iloc[-1]['OBV']
    # OBV_Max = df.iloc[-1]['OBV_Max']
    turnover = df.iloc[-1]['volume']*close

    # ema5_max = df.iloc[-1]['EMA5_Max']
    # ema10_max = df.iloc[-1]['EMA10_Max']
    # ema20_max = df.iloc[-1]['EMA20_Max']
    # ema60_max = df.iloc[-1]['EMA60_Max']
    # ema120_max = df.iloc[-1]['EMA120_Max']
    # ema250_max = df.iloc[-1]['EMA250_Max']
    # close_max = df.iloc[-1]['Close_Max']

    # ema5_min = df.iloc[-1]['EMA5_Min']
    # ema10_min = df.iloc[-1]['EMA10_Min']
    # ema20_min = df.iloc[-1]['EMA20_Min']
    # ema60_min = df.iloc[-1]['EMA60_Min']
    # ema250_min = df.iloc[-1]['EMA250_Min']
    # close_min = df.iloc[-1]['Close_Min']

    if lines=="Strong":
        if close>=ema5>=ema10>=ema20:
            return True
        else:
            return False
    elif lines=="AMP":
        AMP = df.iloc[-1]['AMP']
        if (AMP >= 0.19) & (turnover >= 100000):
            return True
        else:
            return False
    return False

def run(ticker_chunk_df):
    if ticker_chunk_df.empty:
        return pd.DataFrame()
    tickers = ticker_chunk_df.ticker.unique()
    if len(tickers) == 0:
        return pd.DataFrame()
    ticker_chunk_df.set_index('date',inplace=True)
    return_ticker_chunk_df = pd.DataFrame()
    for ticker in tickers:
        ticker_df = ticker_chunk_df[ticker_chunk_df.ticker==ticker]
        # return_ticker_df = pd.DataFrame()
        # Breakout = 0
        # Wait_Cum = 0
        df = ticker_df.iloc[len(ticker_df)-10:]
        today_df = ticker_df.iloc[[-1]]
        for date in df.index:
            date_ticker_df = df[df.index==date]
            if date_ticker_df.empty:
                continue

            AMP_result = screen(date_ticker_df,"AMP")
            
            if AMP_result:
                Strong_result = screen(today_df,"Strong")
                if Strong_result:
                    return_ticker_chunk_df = pd.concat([return_ticker_chunk_df,today_df])
                break

        
    return return_ticker_chunk_df

def save(return_df,async_results,processed_data_file):
    df = pd.DataFrame()
    for async_result in async_results:
        result = async_result.get()
        if not result.empty:
            df = pd.concat([df,result])
    
    if(not df.empty):
        df.reset_index(drop=False,inplace=True)
        try:
            df.to_csv(screened_data_path + processed_data_file + '.csv')
            end = datetime.date.today()
            df = df.loc[df.date==str(end),'ticker']
            df.to_csv(screened_data_path + processed_data_file + '.txt',header=False, index=False)
            return_df = pd.concat([return_df,df])
        except Exception as e:
            logging.critical("return_df to_csv:"+str(e))
    else:
        logging.error("return_df empty")
    return return_df

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == '__main__':
    logpath = '//jack-nas/Work/Python/'
    logfile = logpath + datetime.datetime.now().strftime("%m%d%Y") + "_screen.log"
    logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.INFO)

    isPathExists = os.path.exists(screened_data_path)
    if not isPathExists:
        os.makedirs(screened_data_path)

    now = datetime.datetime.now()
    today830am = now.replace(hour=8,minute=30,second=0,microsecond=0)
    today3pm = now.replace(hour=15,minute=0,second=0,microsecond=0)

    while((now.weekday() <= 4) & (today830am <= datetime.datetime.now() <= today3pm)):
    # while(True):
        now = datetime.datetime.now()
        # today3pm = now.replace(hour=15,minute=5,second=0,microsecond=0)
        # if(now>today3pm):
        #     logging.info("time passed 3:05pm.")
        #     break
        start_time = now.strftime("%m%d%Y-%H%M%S")
        logging.info("start time:" + start_time)

        processed_data_files = os.listdir(processed_data_path)
        if len(processed_data_files) == 0:
            logging.warning("processed data not ready, sleep 10 seconds...")
            time.sleep(10)
            continue

        screened_data_files = os.listdir(screened_data_path)
        processed_data_files_str = processed_data_files[-1] + '_AMP.txt'
        if processed_data_files_str in screened_data_files:
            logging.warning("error: " + processed_data_files_str + " existed, sleep 10 seconds...")
            time.sleep(10)
            continue
        # date_time = datetime.datetime.now() 
        # datetime_str = date_time.strftime("%m%d%Y-%H")
        # end = datetime.date.today()
        logging.info("processing "+processed_data_files[-1])

        try:
            time.sleep(1)
            df = pd.read_feather(processed_data_path + processed_data_files[-1])
        except Exception as e:
            logging.critical(e)
            continue
        df = df.loc[df.date>"2022-01-01"]
        # today = datetime.date.today()
        # day1 = today - timedelta(days=1)
        # day2 = today - timedelta(days=2)
        # day3 = today - timedelta(days=3)
        # df = df.loc[(df.date == str(today)) | (df.date == str(day1)) | (df.date == str(day2)) | (df.date == str(day3))]
        # processed_data_files = os.listdir(processed_data_path)
        # screened_data_file = datetime_str + '_breakout.csv'
        # if screened_data_file in screened_data_files:
        #     print("error: " + screened_data_file + " existed.")
        #     sys.exit(1)

        # df = pd.read_feather(processed_data_path + datetime_str + '.feather')
        # df = df[df['date'] > '2017-01-01']
        # qfq = pd.read_feather(qfq_path+f'{end}'+'_qfq.feather')
        # qfq = qfq[qfq['date'] > '2017-01-01']

        tickers = df.ticker.unique()
        cores = multiprocessing.cpu_count()
        ticker_chunk_list = list(chunks(tickers,math.ceil(len(tickers)/cores)))
        pool=Pool(cores)
        # async_results_60_120 = []
        # async_results_120_250 = []
        # async_results_250 = []
        async_results_AMP = []
        for ticker_chunk in ticker_chunk_list:
            ticker_chunk_df = df[df['ticker'].isin(ticker_chunk)]
            async_result_AMP = pool.apply_async(run, args=(ticker_chunk_df,))
            async_results_AMP.append(async_result_AMP)
        pool.close()
        del(df)
        return_df = pd.DataFrame()

        return_df = save(return_df,async_results_AMP,processed_data_files[-1]+"_AMP")
        # if(not return_df.empty):
        #     try:
        #         return_df.to_csv(screened_data_path + processed_data_files[-1] + '_all.txt',header=False, index=False)
        #     except Exception as e:
        #         logging.critical("return_df to_csv:"+str(e))
        # else:
        #     logging.error("return_df empty")
        stop_time = datetime.datetime.now().strftime("%m%d%Y-%H%M%S")
        logging.info("stop time:" +stop_time)