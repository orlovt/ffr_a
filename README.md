# Intro


## Idea 

On my Money and Banking class at the University of Minnesota Terry Firzgerald has shows us the [FedWatch tool by CME](https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html). This tool shows the probability distribution of the implied FedFundsRate hikes before FOMC meetings. I wanted to replecate this, because it seemed itneresing, looked at the [methodology](https://www.cmegroup.com/education/demos-and-tutorials/fed-funds-futures-probability-tree-calculator.html) and found out that CME is not upfront about how exacly they are getting the data. 

## Implementation 

Later on I decied that it would be pretty convenient and cool to see how the implied trajectory of the fed funds rate changes over time. In order to do this I downloaded the futures historical prices from [yahoo finiance](https://finance.yahoo.com/quote/ZQ%3DF/futures?p=ZQ%3DF) using [yfinance](https://pypi.org/project/yfinance/), conducted some algebraic operations on the data and plotted the trajectories using [ploty](https://plotly.com). 

# Some Examples

>graphs.impl_exp("2022-06-05", "2022-06-30", 7)

>The command plots the impled trajectories of the fedfunds from the June 5th to June 30th with a period of 7 days 
![EX1](plts/plot1.png)<

>graphs.impl_exp("2022-10-18", "2022-12-15", 10)

>The command plots the impled trajectories of the fedfunds from the Oct 18 5th to Dec 15th with a period of 10 days 
![ex2](plts/plot2.png)<

Both of the graphs are centered around FOMC meeting, EX1 is centered around the June 15th meeting, where the FedFundsRate was hiked by 75 basis poins, we can see how the markets changed the future expedted rate. It's also important to mention that from the plots it is evident that the June 15th announcment changed the consensus maximum expected rate and moved the MAX(ffr) along tghe timeline. 

# Summary 

I'd be happy if someone used this tool! Seems pretty simple but usefull, especially for estimating the effect of FED anouncments. 




