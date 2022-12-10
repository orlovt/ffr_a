import yfinance as yf
import pandas_datareader as pdr 

from datetime import datetime, timedelta




class ffr(): 
    def __init__(self, month, year, start_dt): 
        self.month = month 
        self.year = year
        self.start_dt = datetime.strptime(start_dt, '%Y-%m-%d' )


    def get_contract_name_ffr(self): 
        
        f_d = {'01':'ZQF', '02':'ZQG', '03':'ZQH', '04':'ZQJ', 
               '05':'ZQK', '06':"ZQM", '07':'ZQN', '08':'ZQQ', 
               '09':'ZQU', '10':'ZQV','11':'ZQX', '12':'ZQZ'}
        
        return f_d[self.month] + self.year + '.CBT'

    def month_fututres_df(self): 
        
        df = yf.download(ffr.get_contract_name_ffr(self), start=self.start_dt, end = datetime.now(), progress=False)
        df.reset_index(inplace = True )
        df = df[["Date", "Close"]].copy()
        df.columns = ["DT", "P"]

        
        return df 

    def get_effr_df(self):
        end_dt = datetime.now()
        df = pdr.DataReader("EFFR", "fred", self.start_dt, end_dt)
        df.reset_index(inplace = True)
        df = df.dropna(axis = 0)
        df.columns = ["DT", "EFFR"]
        return df     


if __name__ == "__main__":
    test = ffr('01', '23', '2022-10-01')

    print(test.get_contract_name_ffr())
    print(test.month_fututres_df())
    print(test.get_effr_df())

