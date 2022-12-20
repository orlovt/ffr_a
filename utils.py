import pandas as pd 
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
        df["Close"].round(2)
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
            df["R_IMPL"] = df["R_IMPL"].round(2)
            df = df[["Date", "R_IMPL"]].copy()

            res[i] = Helpers.df_to_dict(df)

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

class ffr_months_df():
    def __init__(self, dt_finish = 0):
        
        if dt_finish == 0: 
            dt = datetime.now()

        self.dt = dt 
        self.df = ffr_months_df.get_df(self)
    
    def get_df(self): 
        
        contracts= {'2022-12-01':'ZQZ22.CBT', '2023-01-01':'ZQF23.CBT', '2023-02-01':'ZQG23.CBT', '2023-03-01':'ZQH23.CBT', 
                    '2023-04-01':'ZQJ23.CBT', '2023-05-01':'ZQK23.CBT', '2023-06-01':'ZQM23.CBT', '2023-07-01':'ZQN23.CBT', 
                    '2023-08-01':'ZQQ23.CBT', '2023-09-01':'ZQU23.CBT', '2023-10-01':'ZQV23.CBT', '2023-11-01':'ZQX23.CBT', 
                    '2023-12-01':'ZQZ23.CBT'}
        res = ffr_months_df.get_futures(self, 'ZQN23.CBT')
        res = res[["Date"]]
        res["Date"] = res['Date'].astype('datetime64[ns]') 

    
        for i in contracts: 
            temp = ffr_months_df.get_futures(self, contracts[i])
            res[i] = temp["R_IMPL"]
        return res

    def get_futures(self, contract): 
        
        df = yf.download(contract, start = self.dt - timedelta(185), end = self.dt, progress=False)
        df.reset_index(inplace = True )

        df["R_IMPL"] = 100 - df["Close"].round(2)
        df = df[["Date", "R_IMPL"]].copy()


        return df


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

    def df_to_dict(df): 
        res = {}
        for i in range(df.shape[0]):
            res[df['Date'][i]] = df['R_IMPL'][i]
        return res 





if __name__ == "__main__":
    #test = ffr(1, 23, '2022-10-01')
    
    #print(test.get_contract_name_ffr())
    #print(test.month_fututres_df())
    #print(test.get_effr_df())

    #print(test.futures_name)
    #print(test.futures_prices.head(15))
    #print(test.effr.head(20))


    #t = trajectory_dt('2021-09-01')
    #print(t.price())
    #dt = datetime.strptime("2022-11-01", '%Y-%m-%d' )
    
    #for i in t.dfs:
    #    print(t.dfs[i][dt])

    #print(t.price())
    #print(t.price2()) 

    #print(ffr_months_df().df.tail(5))
    print(ffr_months_df().df)

