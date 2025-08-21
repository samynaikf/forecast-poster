import io
import csv
import numpy as np
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from plotter import plot_chart
from overlayPNGs import overlay

def load_data(filename,asset):
    '''
    Load data from given file
    '''
    found_asset = False
    dataMat = []
    # with open(filename,encoding='mac_roman') as csvFile:
    with io.open(filename,encoding='mac_roman') as csvFile:
        csv_reader = csv.reader(csvFile)

        counter = 0
        num = 0
        for row in csv_reader:
            num += 1
            if not found_asset:
                if num == 2:
                    break
                for item in row:
                    if item == asset:
                        found_asset = True
                        col_num = counter
                        break
                    counter+=1
            if num > 1:
                dataMat.append([row[0],float(row[col_num])])
                counter += 1

    if not found_asset:
        print('Unable to find asset in database')

    return dataMat


def get_year_array(data,end_date='3/1/19'):
    '''
    Go through data until date is reached, then calculate percentage
    change for different time horizons
    '''
    reached_end = False
    index = 1
    #Loop through data until date reached
    while not reached_end:
        if index >= len(data):
            print('Invalid date entered')
            break

        if data[index][0] == end_date:
            #get 1 year of data
            year_array = data[index-400:index+1]
            break
        index += 1

    #Return year of past data
    return year_array


def get_price_change(year_array,length):

    ROI = round(100*(prices[-1]/prices[0] -1),2)
    if ROI > 0:
        ROI = '+' + "%.2f" % ROI + '%'
    else:
        ROI = "%.2f" % ROI + '%'
    return ROI




data_filename = 'data.csv'
#get imput
asset_name = input("Enter the name of asset you would like information for:\n\n")

#load data
data = load_data(data_filename,asset_name)

#Check to make sure data isn't empty
if len(data) > 1:
    # horizon = input("\nEnter the time horizon to chart for {}:\n\n".format(asset_name))

    start_date = input("\nEnter the start date you would like information for:\n\n")

    end_date = input("\nEnter the end date you would like information for:\n\n")

    #get percent changes
    year_array = get_year_array(data,end_date=end_date)

    info_list = [['TIME HORIZON','3-day',
                                '1-week',
                                '2-week',
                                '1-month',
                                '3-month',
                                '1-year'],
                ['RATE OF RETURN',str(round(100*((year_array[-1][1]/year_array[-4][1]) - 1),2))+'%',
                                str(round(100*((year_array[-1][1]/year_array[-8][1]) - 1),2))+'%',
                                str(round(100*((year_array[-1][1]/year_array[-15][1]) - 1),2))+'%',
                                str(round(100*((year_array[-1][1]/year_array[-31][1]) - 1),2))+'%',
                                str(round(100*((year_array[-1][1]/year_array[-91][1]) - 1),2))+'%',
                                str(round(100*((year_array[-1][1]/year_array[-366][1]) - 1),2))+'%']]

    #print table
    print(tabulate(info_list,[asset_name + ' Report',' ',' ',' ',' ',' ',' '],"fancy_grid"))

    prices = []
    dates = []
    started = False
    # for x in range(len(year_array)-int(horizon),len(year_array)):
    for x in range(len(year_array)):
        if year_array[x][0] == start_date:
            started = True
        if started:
            dates.append(year_array[x][0])
            prices.append(year_array[x][1])
        if year_array[x][0] == end_date:
            started = False
    dates = np.array(dates)
    prices = np.array(prices)

    plot_chart(dates,prices,asset_name)













#
