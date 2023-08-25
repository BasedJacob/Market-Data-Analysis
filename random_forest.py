import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
import datetime
from sklearn.ensemble import RandomForestRegressor

def main(gas_data, energy_data, crude_oil_data, oil_consumption_data):

    # Reading dataframes and grouping the daily data to weekly averages
    gas_df = pd.read_excel(gas_data, sheet_name='Data 1')
    gas_df['Date'] = pd.to_datetime(gas_df['Date'])
    crude_oil_df = pd.read_csv(crude_oil_data, skiprows=15)
    crude_oil_df['date'] = pd.to_datetime(crude_oil_df['date'])

    oil_consumption_df = pd.read_excel(oil_consumption_data, sheet_name='Data 1', skiprows=2)
    oil_consumption_df['Date'] = pd.to_datetime(oil_consumption_df['Date'])
    energy_df = pd.read_csv(energy_data)
    energy_df['date'] = pd.to_datetime(energy_df['date'])
    energy_df.set_index('date', inplace=True)
    energy_df = energy_df.resample('W-Mon').mean()


    crude_oil_df.set_index('date', inplace=True)
    oil_consumption_df.set_index('Date', inplace=True)
    crude_oil_df = crude_oil_df.resample('W-Mon').mean().dropna()
    oil_consumption_df = oil_consumption_df.resample('W-Mon').mean().dropna()

    # Merging the separate data into the same dataframe
    df = gas_df.copy()
    df = gas_df.merge(crude_oil_df, left_on='Date', right_on='date', how='inner')
    df.rename(columns={' value': 'crudeoil'}, inplace=True)
    df = df.merge(energy_df, left_on='Date', right_on='date', how='inner')
    df.rename(columns={' energy': 'Energy'}, inplace=True)
    df = df.merge(oil_consumption_df, left_on='Date', right_on='Date', how='inner')
    df.rename(columns={' value': 'oil consumption'}, inplace=True)
    df = df.dropna()

    # separating the X and y training points for the model
    X = df[['crudeoil', 'Weekly U.S. Product Supplied of Finished Motor Gasoline  (Thousand Barrels per Day)', 'energy']]
    y = df['Weekly U.S. All Grades All Formulations Retail Gasoline Prices  (Dollars per Gallon)']

    # Separating training and validation data for the model
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)

    # A Random Forest Regressor model was chosen to calculat the feature importances, and due to the presence of multiple features influencing the price of gas
    model = RandomForestRegressor(30, max_depth=5)

    model.fit(X_train, y_train)
    print("Training score:")
    print(model.score(X_train, y_train))
    print("Validation score:")
    print(model.score(X_valid, y_valid))

    # extracting the feature importances
    importances = model.feature_importances_

    forest_importances = {'Cost of Crude Oil' : importances[0], 'Gas Demand in the US':importances[1], 'Energy Index':importances[2]}
    forest_importances_series = pd.Series(data = forest_importances, index=['Cost of Crude Oil', 'Gas Demand in the US', 'Energy Index'])

    # graphing the feature importances
    plt.bar(forest_importances_series.index, forest_importances_series.values)
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.title('Feature Importances in Influencing the Cost of Gas')
    plt.savefig('random_forest_importances.png')
    


if __name__ == '__main__':

    gas_data = sys.argv[1]
    energy_data = sys.argv[2]
    crude_oil_data = sys.argv[3]
    oil_consumption_data = sys.argv[4]

    main(gas_data, energy_data, crude_oil_data, oil_consumption_data)

    # python random_forest.py US_weekly_gas.xls Energy10.csv wti-crude-oil-prices-10-year-daily-chart.csv oil_consumption.xls
