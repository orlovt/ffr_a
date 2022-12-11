import yfinance as yf
import pandas_datareader as pdr 

from datetime import datetime, timedelta




class ffr(): 
    def __init__(self, month, year, start_dt): 
        self.month = month 
        self.year = year
        self.start_dt = datetime.strptime(start_dt, '%Y-%m-%d' )
        self.futures_name = ffr.get_contract_name_ffr(self)
        self.effr = ffr.get_effr_df(self)
        self.futures_prices =  ffr.month_fututres_df(self)



    def get_contract_name_ffr(self): 
        
        f_d = {1:'ZQF', 2:'ZQG', 3:'ZQH', 4:'ZQJ', 
               5:'ZQK', 6:"ZQM", 7:'ZQN', 8:'ZQQ', 
               9:'ZQU', 10:'ZQV',11:'ZQX', 12:'ZQZ'}
        
        return f_d[self.month] + str(self.year) + '.CBT'

    def month_fututres_df(self): 
        
        df = yf.download(self.futures_name, start=self.start_dt, end = datetime.now(), progress=False)
        df.reset_index(inplace = True )
        df = df[["Date", "Close"]].copy()
        df["P"].round(2)
        df.columns = ["DT", "P"]
        df["R_IMPL"] = 100 - df["P"]

        df.set_index("DT")

        
        return df 

    def get_effr_df(self):
        end_dt = datetime.now()
        df = pdr.DataReader("EFFR", "fred", self.start_dt, end_dt)
        df.reset_index(inplace = True)
        df = df.dropna(axis = 0)
        df.columns = ["DT", "EFFR"]
        df.set_index("DT")
        return df     

class trajectory_dt(): 
    def __init__(self, dt):
        if type(dt) == str: 
            dt = datetime.strptime(dt, '%Y-%m-%d')
        self.dt = dt

        #self.range = {'12':'ZQZ22.CBT', '01':'ZQF23.CBT', '02':'ZQG23.CBT', '03':'ZQH23.CBT', 
        #              '04':'ZQJ23.CBT', '05':'ZQK23.CBT', '06':"ZQM23.CBT"}
        self.range = {'2022-12-01':'ZQZ22.CBT', '2023-01-01':'ZQF23.CBT', '2023-02-01':'ZQG23.CBT', '2023-03-01':'ZQH23.CBT', 
                      '2023-04-01':'ZQJ23.CBT', '2023-05-01':'ZQK23.CBT', '2023-06-01':'ZQM23.CBT', '2023-07-01':'ZQN23.CBT'}
        self.dfs = trajectory_dt.get_dfs(self)
        
    def get_dfs(self):
        res = {}

        for i in self.range:
            df = yf.download(self.range[i], start = self.dt - timedelta(90), end = self.dt, progress=False)
            df.reset_index(inplace = True )
            df["Close"].round(2)
            df["R_IMPL"] = 100 - df["Close"]
            #R_IMPL = round(100 - float(df.loc[df["Date"] == self.dt]["Close"]), 2)
            res[i] = df
        return res

    def price(self): 
        dict = {'dt':self.dt}        
        for i in self.range: 
            df = yf.download(self.range[i], start = self.dt - timedelta(2), end = self.dt + timedelta(2), progress=False)
            df.reset_index(inplace = True )

            R_IMPL = round(100 - float(df.loc[df["Date"] == self.dt]["Close"]), 2)
            dict[i] = R_IMPL

        return dict

    def price2(self): 
        dict = {'dt':self.dt}        
        for i in self.dfs: 
            df = self.dfs[i]
            R_IMPL = (df.loc[df["Date"] == self.dt]["R_IMPL"])
            print(R_IMPL)
            dict[i] = R_IMPL
        return dict

    

class Helpers(): 
    def B_filter(dt): # returns the last date markets were open for the date given in dt format
        dow = datetime.weekday(dt)
        if dow == 6: 
            return dt - timedelta(2)
        elif dow == 5:
            return dt - timedelta(1)
        else: 
            return dt


    def days_n_before(dt, n): #returns the nth day before the given day when the markets were working, (Sun,1)--> Fri in dt format
        dt = dt - timedelta(n)
        return Helpers.B_filter(dt)

if __name__ == "__main__":
    #test = ffr(1, 23, '2022-10-01')

    #print(test.get_contract_name_ffr())
    #print(test.month_fututres_df())
    #print(test.get_effr_df())

    #print(test.futures_name)
    #print(test.futures_prices.head(15))
    #print(test.effr.head(20))


    t = trajectory_dt('2021-09-01')
    #print(t.price())
    #for i in t.dfs:
    #    print(t.dfs[i].head())
    print(t.price())
    print(t.price2())