# Data_Analysis_Project - Kayla Lee & Jacob He
CMPT353 w/ Greg Baker

## 1) Install python

## 2) Clone the repository  
* https://github.sfu.ca/kel7/CMPT-353-Final-Project

## 3) Install required libraries
* pip install pandas
* pip install seaborn
* pip install matplotlib
* pip install scipy
* pip install sklearn
* pip install numpy
* pip install statsmodels

## 3.5) Clean the data 
* Already completed. Process documented below

## 4) Data analysis
* python data_analysis.py US_weekly_gas.xls sp500_index.csv
* This program graphs the data for visualization, and calculates the Spearman Correlation Coefficient to determine if there is a correlation between the cost of gas and the S&P 500 stock index. 3 images are created and saved as png files, gas_sp_graphs.png, gas_sp_together.png, and sp_plotted_against_gas.png. This program prints the Spearman Correlation Coefficients for the initial data as well as shifted data to identify if there is a delayed correlation between the two datasets. 

## 5) All Indexes Heatmap
* python heatmap.py US_weekly_gas.xls sp500_index.csv BigTech10.csv FoodAndBev10.csv Energy10.csv Industrials10.csv PreciousMetals10.csv
* This program calculates and saves a heatmap, stock_heatmap.png, of the correlations between the cost of gas and individual stock indexes. The heatmap's calculations are also printed. 

## 6) Random forest model
* python random_forest.py US_weekly_gas.xls Energy10.csv wti-crude-oil-prices-10-year-daily-chart.csv oil_consumption.xls
* This program creates a Random Forest Regressor model, and calculates the feature importances used. random_forest_importances.png is saved to visualize how the model used each feature in its predictions. 



## 3.5)
* The data has been already cleaned, and the clean data is already in the main folder. 
This part documents the cleaning raw data files.
* The raw data is in the "raw_data" folder
* Inspect the raw data tables in excel
* To clean the data:
* python etl.py inputfile number1 number2
* where inputfile is the filename of the raw data file, and number1 and number2 is where the row data you want starts and ends. Column names to remove should be manually added within  etl.py in create_dataframe function
* Rename the saved files to something appropriate
