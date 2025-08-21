
import pandas as pd

def get_package_slug(package_name):
    df = pd.read_csv('Package_Categories.csv',header=0,index_col=0)
    for i in range(df.shape[0]):
        if df.index[i] in package_name:
            return df.iloc[i]['Slug']



def get_package_name(package_name):
    df = pd.read_csv('PackageNameMatching.csv',header=0,index_col=0)
    for i in range(df.shape[0]):
        if df.index[i] in package_name:
            return df.iloc[i]['PackageName']
    return 'Stock Forecast & S&P500 Forecast'


# print(get_package_slug(get_package_name('IKForecast_SP500_stocks_Top10 - macro')))






#
