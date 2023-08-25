import pandas as pd
import numpy as np 
import sys
import datetime
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess

    

def main(gas, sp):
    # s&p data
    sp_data = pd.read_csv(sp)
    sp_data['Date'] = pd.to_datetime(sp_data['Date'])


    # gas data
    gas_data = pd.read_excel(gas, sheet_name='Data 1')


    # Grouping s&p data from daily to weekly data
    sp_data.set_index('Date', inplace=True)
    sp_data = sp_data.resample('W-Mon').mean().dropna()

    # combining gas and s&p data onto the same dataframe
    gas_sp_data = gas_data.merge(sp_data, left_on='Date', right_on='Date', how='inner')

    # loess filter for gas prices
    gas_filtered = lowess(gas_sp_data['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)'], gas_sp_data['Date'], frac=0.045)
    gas_smoothed_data = gas_filtered[:,1]

    # plotting gas
    plt.figure(figsize=(10,5))
    plt.subplot(1,2,1)
    plt.xlabel('Date')
    plt.ylabel('Dollars per Gallon (USD)')
    plt.title('Weekly Retail Gasoline Prices (Dollars per Gallon)')
    plt.scatter(gas_sp_data['Date'], gas_sp_data['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)'], s=8)
    plt.xticks(rotation=90)

    plt.plot(gas_sp_data['Date'], gas_smoothed_data, 'r-', linewidth=3)
    

    # loess filter and plotting for s&p stock index 
    sp_filtered = lowess(gas_sp_data['S&P500'], gas_sp_data['Date'], frac = 0.045)
    sp_smoothed_data = sp_filtered[:,1]

    plt.subplot(1,2,2)
    plt.xlabel('Date')
    plt.ylabel('S&P 500 Stock Index (USD)')
    plt.title('Weekly S&P 500 Stock Index')

    plt.scatter(gas_sp_data['Date'], gas_sp_data['S&P500'], s=8)
    plt.plot(gas_sp_data['Date'], sp_smoothed_data, 'r-', linewidth=3)
    plt.xticks(rotation=90)
    plt.savefig('gas_sp_graphs.png', bbox_inches='tight')

    # plot gas and s&p data on the same plot
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Dollars per Gallon (USD)')
    ax1.plot(gas_sp_data['Date'], gas_sp_data['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    # ax1.legend('Gas Prices')

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('S&P 500 Stock Index (USD)')
    ax2.plot(gas_sp_data['Date'], gas_sp_data['S&P500'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    
    plt.savefig('gas_sp_together.png', bbox_inches='tight')
    plt.show()




    # Plotting gas prices and S&P as x and y axises to get the relationship
    plt.scatter(gas_sp_data['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)'], gas_sp_data['S&P500'], s=10)
    a, b = np.polyfit(gas_sp_data['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)'], gas_sp_data['S&P500'], 1)
    plt.plot(gas_sp_data['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)'], a*gas_sp_data['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)']+b, color='r')
    plt.title('The Cost of Gas Against the S&P500 Index')
    plt.xlabel('Dollars per Gallon (USD)')
    plt.ylabel('S&P 500 Index (USD)')
    plt.savefig('sp_plotted_against_gas.png')
    plt.show()



    
    # spearman's correlation coefficient for non-linear data
    print('Spearman correlation coefficient:')
    print(stats.spearmanr(gas_sp_data['S&P500'], gas_sp_data['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)']).statistic)


    # calculating the correlation coefficient for the shifted s&p500 data
    for i in range(1,5):
        shift_df = gas_sp_data.copy()
        shift_df['S&P500'] = shift_df['S&P500'].shift(periods=4, axis=0)
        shift_df = shift_df.dropna()
        print(str(i)," week S&P shifted spearman correlation coefficient:")
        print(stats.spearmanr(shift_df['S&P500'], shift_df['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)']).statistic)

    for i in range(1,5):
        shift_df = gas_sp_data.copy()
        shift_df['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)'] = shift_df['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)'].shift(periods=4, axis=0)
        shift_df = shift_df.dropna()
        print(str(i)," week gas shifted spearman correlation coefficient:")
        print(stats.spearmanr(shift_df['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)'], shift_df['S&P500']).statistic)




if __name__ == '__main__':
    gas_data = sys.argv[1]
    sp_data = sys.argv[2]
 
    main(gas_data, sp_data)


    # python data_analysis.py US_weekly_gas.xls sp500_index.csv
