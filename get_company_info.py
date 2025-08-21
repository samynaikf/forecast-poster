'''
Functions to get company name and info from ticker
'''
import pandas as pd
df = pd.read_excel('Company_info.xlsx',header=0,index_col=0)

def get_company_info(ticker):
    try:
        return df.loc[ticker]['Explanation']
    except:
        return ''

def get_company_name(ticker):
    try:
        return df.loc[ticker]['Name']
    except:
        return ''




#
