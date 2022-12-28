import pandas as pd 
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta


class FFR__df():
    def __init__(self, dt_finish = 0):

        #if dt_finish not given, dt_finish is """now"""        
        if dt_finish == 0: 
            dt = datetime.now()

        #attributes setup 
        self.dt = dt 
        self.df = FFR__df.get_df(self)
    
    def get_df(self): 
        
        # setting up dictionary for futures contracts 
        
        contracts= {'2022-12-01':'ZQZ22.CBT', '2023-01-01':'ZQF23.CBT', '2023-02-01':'ZQG23.CBT', '2023-03-01':'ZQH23.CBT', 
                    '2023-04-01':'ZQJ23.CBT', '2023-05-01':'ZQK23.CBT', '2023-06-01':'ZQM23.CBT', '2023-07-01':'ZQN23.CBT', 
                    '2023-08-01':'ZQQ23.CBT', '2023-09-01':'ZQU23.CBT', '2023-10-01':'ZQV23.CBT', '2023-11-01':'ZQX23.CBT', 
                    '2023-12-01':'ZQZ23.CBT'}
        
        # using the "get_futures" method from class 
        # data frame with one column: "Data"
        
        res = FFR__df.get_futures(self, 'ZQN23.CBT')
        res = res[["Date"]]
        res["Date"] = res['Date'].astype('datetime64[ns]') 

        # looping thru the contract names and appending colums to the dataframe
        # columns are fututes prices for given month 
        
        for i in contracts: 
            temp = FFR__df.get_futures(self, contracts[i])
            
            #column "name" is a column containing a transformaed daily closing prices of the FFR
            res[i] = temp["R_IMPL"]
        return res


    def get_futures(self, contract): 
    # parsing futures prices using yfinancie library 
        
        # setting start and end date 
        range_days = 185
        df = yf.download(contract, start = self.dt - timedelta(range_days), end = self.dt, progress=False)
        df.reset_index(inplace = True )

        # creating implied rate column 
        df["R_IMPL"] = 100 - df["Close"].round(2)
        

        return df[["Date", "R_IMPL"]].copy()

class FFR_graphs():
    def __init__(self):
        self.df = FFR__df().df.copy()

    def hist_exp(self, start_dt, end_dt, period):

        h_df =self.df.loc[(self.df["Date"] >= start_dt) & (self.df["Date"] <= end_dt)]


        #plotting futures data
        #0y axis is the rate 
        #0x date 
        #legends correspond to futures contracts from yahoo finance  
        fig = go.Figure()
        fig.update_layout(title = "Implired FedFundsRate for given month")

        #setting number of months and intervals 
        for i in h_df.columns[1::period]:
            #converting column name into datetime format, for lines naming 
            dt = datetime.strptime(i, '%Y-%m-%d' )
            fig.add_trace(go.Scatter(x = h_df['Date'], y = h_df[i], name = dt.strftime("%b") + dt.strftime("%y")))
        #return fig_2.show()
        return fig.show()

    def impl_exp(self, start_dt, end_dt, period):
        
        i_df =self.df.loc[(self.df["Date"] >= start_dt) & (self.df["Date"] <= end_dt)][::period]

        # transforming dataframe, resetting indexes
        i_df = i_df.set_index('Date')
        i_df = i_df.T
        i_df.reset_index(inplace = True)

        # plotting the implied ffr trajectory using plotly library 
        fig = go.Figure()
        fig.update_layout(title = "Implied FFR trajectory @time")
        for proj_month in i_df.columns[1:]:#setting custom range 

            fig.add_trace(go.Scatter(x = i_df['index'], y = i_df[proj_month], name = proj_month.strftime("%d") + proj_month.strftime("%b") + proj_month.strftime("%y"))) #labeling and plotting lines

        return fig.show()

class Helpers(): 

     
    def B_filter(dt):
    
    # returns the last day when the markets were open for the date given in dt format
        dow = datetime.weekday(dt)
        if dow == 6: 
            return dt - timedelta(2)
        elif dow == 5:
            return dt - timedelta(1)
        else: 
            return dt
    
    
    def days_n_before(dt, n): 
    
    # returns the nth day before the given day when the markets were working, (Sun,1)--> Fri in dt format
        return Helpers.B_filter(dt)


if __name__ == "__main__":

    #print(FFR__df().df.head(20))
    g = FFR_graphs()
    #print(g.df.head(10))
    #print(dir(g))
    #print(g.hist_exp("2022-01-01", "2022-12-25", 10))
    print(g.impl_exp("2022-01-01", "2022-12-25", 30))




