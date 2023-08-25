import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import sys

def main(gas, sp, tech, foodbev, energy, industrials, precious_metals):

    #Read all the data into their respective data frames
    sp_data = pd.read_csv(sp)
    sp_data['date'] = pd.to_datetime(sp_data['Date'])
    sp_data = sp_data.drop('Date', axis=1)
    sp_data.set_index('date', inplace=True)
    sp_data = sp_data.resample('W-Mon').mean()
    # print(sp_data)

    gas_data = pd.read_excel(gas, sheet_name='Data 1')
    gas_data['date'] = pd.to_datetime(gas_data['Date'])
    gas_data = gas_data.drop('Date', axis=1)


    tech_data = pd.read_csv(tech)
    tech_data['date'] = pd.to_datetime(tech_data['date'])
    tech_data.set_index('date', inplace=True)
    tech_data = tech_data.resample('W-Mon').mean()
    # print(tech_data)

    food_bev_data = pd.read_csv(foodbev)
    food_bev_data['date'] = pd.to_datetime(food_bev_data['date'])
    food_bev_data.set_index('date', inplace=True)
    food_bev_data = food_bev_data.resample('W-Mon').mean()
    # print(food_bev_data)
    

    energy_data = pd.read_csv(energy)
    energy_data['date'] = pd.to_datetime(energy_data['date'])
    energy_data.set_index('date', inplace=True)
    energy_data = energy_data.resample('W-Mon').mean()

    industrials_data = pd.read_csv(industrials)
    industrials_data['date'] = pd.to_datetime(industrials_data['date'])
    industrials_data.set_index('date', inplace=True)
    industrials_data = industrials_data.resample('W-Mon').mean()
    
    precious_metals_data = pd.read_csv(precious_metals)
    precious_metals_data['date'] = pd.to_datetime(precious_metals_data['date'])
    precious_metals_data.set_index('date', inplace=True)
    precious_metals_data = precious_metals_data.resample('W-Mon').mean()


    #Merge all the dataframes together into one big dataframe "df"
    df = tech_data.copy()
    df = df.merge(food_bev_data, left_on='date', right_on='date', how='inner')
    df = df.merge(energy_data, left_on='date', right_on='date', how='inner')
    df = df.merge(industrials_data, left_on='date', right_on='date', how='inner')
    df = df.merge(precious_metals_data, left_on='date', right_on='date', how='inner')
    df = df.merge(sp_data, left_on='date', right_on='date', how='inner')
    df = df.merge(gas_data, left_on='date', right_on='date', how='inner')

    #drop the rows with empty cells (usually edge cases for the starting days or ending days)
    df = df.dropna()
    df.rename(columns={'Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)': 'Gas Prices'}, inplace=True)
    # print(df)
    cormat = df.corr(method = 'spearman')
    sns.heatmap(cormat, annot = True)
    plt.title('Spearman Correlation Heatmap')
    plt.savefig('stock_heatmap.png', bbox_inches='tight')
    plt.show()
    print(cormat)

#  Take in all the input files as parameters, and  call "main"
if __name__ == '__main__':
    gas = sys.argv[1]
    sp = sys.argv[2]
    tech = sys.argv[3]
    foodbev = sys.argv[4]
    energy = sys.argv[5]
    industrials = sys.argv[6]
    precious_metals = sys.argv[7]
 
    main(gas, sp, tech, foodbev, energy, industrials, precious_metals)

#To run the program, copy the line below into the terminal
# python heatmap.py US_weekly_gas.xls sp500_index.csv BigTech10.csv FoodAndBev10.csv Energy10.csv Industrials10.csv PreciousMetals10.csv
