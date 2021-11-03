
import pandas as pd
import datetime
import time

CLOSE_ABOVE_EMA = True
MACD_DIF_ABOVE_MACD_DEA = True
TURN_MINMAX = False
TURN_2575 = True
OBV_ABOVE_ZERO_DAYS_MINMAX = False
OBV_ABOVE_ZERO_DAYS_2575 = True
OBV_DIFF_RATE_MINMAX = False
OBV_DIFF_RATE_2575 = True
CUM_TURN_RATE_MINMAX = False
CUM_TURN_RATE_2575 = True
WR34_MINMAX = False
WR34_2575 = True
WR120_MINMAX = False
WR120_2575 = True
WR120_50_MINMAX = False
WR120_50_2575 = True
WR120_80_MINMAX = False
WR120_80_2575 = True

TURN_25 = 0
TURN_75 = 0.06
OBV_ABOVE_ZERO_DAYS_25 = 135.25
OBV_ABOVE_ZERO_DAYS_75 = 200
OBV_DIFF_RATE_25 = 0
OBV_DIFF_RATE_75 = 0.77
CUM_TURN_RATE_25 = 0
CUM_TURN_RATE_75 = 2.15085156
WR34_25 = 0
WR34_75 = 79.48277376
WR120_25 = 0
WR120_75 = 88.29148528
WR120_GREATER_THAN_50_DAYS_25 = 182
WR120_GREATER_THAN_50_DAYS_75 = 200
WR120_GREATER_THAN_80_DAYS_25 = 93.75
WR120_GREATER_THAN_80_DAYS_75 = 200

TURN_MIN = 0.023769694
TURN_MAX = 4.854261389
OBV_ABOVE_ZERO_DAYS_MIN = 8
OBV_ABOVE_ZERO_DAYS_MAX = 200
OBV_DIFF_RATE_MIN = 0.000140247
OBV_DIFF_RATE_MAX = 1
CUM_TURN_RATE_MIN = 1.200638886
CUM_TURN_RATE_MAX = 77.99560789
WR34_MIN = 0
WR34_MAX = 100
WR120_MIN = 0.757581046
WR120_MAX = 100
WR120_GREATER_THAN_50_DAYS_MIN = 60
WR120_GREATER_THAN_50_DAYS_MAX = 200
WR120_GREATER_THAN_80_DAYS_MIN = 12
WR120_GREATER_THAN_80_DAYS_MAX = 200

def screen(df):
    lastindex = df.index[-1]

    if CLOSE_ABOVE_EMA & (df['close'][lastindex] < df['EMA34'][lastindex]):
        return pd.DataFrame()

    if MACD_DIF_ABOVE_MACD_DEA & ((df['MACD_dif'][lastindex]-df['MACD_dea'][lastindex]) < 0):
        return pd.DataFrame()

    if TURN_MINMAX & ((df['turn'][lastindex] > TURN_MAX) | (df['turn'][lastindex] < TURN_MIN)):
        return pd.DataFrame()
    if TURN_2575 & ((df['turn'][lastindex] > TURN_75) | (df['turn'][lastindex] < TURN_25)):
        return pd.DataFrame()

    if OBV_ABOVE_ZERO_DAYS_MINMAX & ((df['obv_above_zero_days'][lastindex] > OBV_ABOVE_ZERO_DAYS_MAX) | (df['obv_above_zero_days'][lastindex] < OBV_ABOVE_ZERO_DAYS_MIN)):
        return pd.DataFrame()
    if OBV_ABOVE_ZERO_DAYS_2575 & ((df['obv_above_zero_days'][lastindex] > OBV_ABOVE_ZERO_DAYS_75) | (df['obv_above_zero_days'][lastindex] < OBV_ABOVE_ZERO_DAYS_25)):
        return pd.DataFrame()

    if OBV_DIFF_RATE_MINMAX & ((df['OBV_DIFF_RATE'][lastindex] > OBV_DIFF_RATE_MAX) | (df['OBV_DIFF_RATE'][lastindex] < OBV_DIFF_RATE_MIN)):
        return pd.DataFrame()
    if OBV_DIFF_RATE_2575 & ((df['OBV_DIFF_RATE'][lastindex] > OBV_DIFF_RATE_75) | (df['OBV_DIFF_RATE'][lastindex] < OBV_DIFF_RATE_25)):
        return pd.DataFrame()

    cum_turn_rate = df['upper_cum_turn'][lastindex]/df['lower_cum_turn'][lastindex]
    if CUM_TURN_RATE_MINMAX & ((cum_turn_rate > CUM_TURN_RATE_MAX) | (cum_turn_rate < CUM_TURN_RATE_MIN)):
        return pd.DataFrame()
    if CUM_TURN_RATE_2575 & ((cum_turn_rate > CUM_TURN_RATE_75) | (cum_turn_rate < CUM_TURN_RATE_25)):
        return pd.DataFrame()

    if WR34_MINMAX & ((df.WR34[lastindex] > WR34_MAX) | (df.WR34[lastindex] < WR34_MIN)):
        return pd.DataFrame()
    if WR34_2575 & ((df.WR34[lastindex] > WR34_75) | (df.WR34[lastindex] < WR34_25)):
        return pd.DataFrame()

    if WR120_MINMAX & ((df.WR120[lastindex] > WR120_MAX) | (df.WR120[lastindex] < WR120_MIN)):
        return pd.DataFrame()
    if WR120_2575 & ((df.WR120[lastindex] > WR120_75) | (df.WR120[lastindex] < WR120_25)):
        return pd.DataFrame()

    if WR120_50_MINMAX & ((df['wr120_larger_than_50_days'][lastindex] < WR120_GREATER_THAN_50_DAYS_MIN) | (df['wr120_larger_than_50_days'][lastindex] > WR120_GREATER_THAN_50_DAYS_MAX)):
        return pd.DataFrame()
    if WR120_50_2575 & ((df['wr120_larger_than_50_days'][lastindex] < WR120_GREATER_THAN_50_DAYS_25) | (df['wr120_larger_than_50_days'][lastindex] > WR120_GREATER_THAN_50_DAYS_75)):
        return pd.DataFrame()

    if WR120_80_MINMAX & ((df['wr120_larger_than_80_days'][lastindex] < WR120_GREATER_THAN_80_DAYS_MIN) | (df['wr120_larger_than_80_days'][lastindex] > WR120_GREATER_THAN_80_DAYS_MAX)):
        return pd.DataFrame()
    if WR120_80_2575 & ((df['wr120_larger_than_80_days'][lastindex] < WR120_GREATER_THAN_80_DAYS_25) | (df['wr120_larger_than_80_days'][lastindex] > WR120_GREATER_THAN_80_DAYS_75)):
        return pd.DataFrame()

    return df

end = datetime.date.today()
processed_data_path=f"//jack-nas/Work/Python/ProcessedData/"
screened_data_path=f"//jack-nas/Work/Python/ScreenedData/"

if __name__ == '__main__':
    df = pd.read_feather(processed_data_path + f'{end}' + '.feather')
    df = df[(df['date'] == '2021-11-01') & (df['ticker'] == 'LMFA')]
    screen(df)