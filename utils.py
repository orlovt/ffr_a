import pandas as pd 
import yfinance as yf
import pandas_datareader as pdr 

from datetime import datetime, timedelta

class trajectory_dt(): 
    def __init__(self, dt):
        if type(dt) == str: 
            dt = datetime.strptime(dt, '%Y-%m-%d')
        self.dt = dt

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

class FFR__df():
    def __init__(self, dt_finish = 0):
        
        if dt_finish == 0: 
            dt = datetime.now()

        self.dt = dt 
        self.df = FFR__df.get_df(self)
    
    def get_df(self): 
        
        contracts= {'2022-12-01':'ZQZ22.CBT', '2023-01-01':'ZQF23.CBT', '2023-02-01':'ZQG23.CBT', '2023-03-01':'ZQH23.CBT', 
                    '2023-04-01':'ZQJ23.CBT', '2023-05-01':'ZQK23.CBT', '2023-06-01':'ZQM23.CBT', '2023-07-01':'ZQN23.CBT', 
                    '2023-08-01':'ZQQ23.CBT', '2023-09-01':'ZQU23.CBT', '2023-10-01':'ZQV23.CBT', '2023-11-01':'ZQX23.CBT', 
                    '2023-12-01':'ZQZ23.CBT'}
        res = FFR__df.get_futures(self, 'ZQN23.CBT')
        res = res[["Date"]]
        res["Date"] = res['Date'].astype('datetime64[ns]') 

    
        for i in contracts: 
            temp = FFR__df.get_futures(self, contracts[i])
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


    #t = trajectory_dt('2021-09-01')
    #print(t.price())
    #dt = datetime.strptime("2022-11-01", '%Y-%m-%d' )
    
    #for i in t.dfs:
    #    print(t.dfs[i][dt])

    #print(t.price())
    #print(t.price2()) 

    print(ffr_months_df().df)

