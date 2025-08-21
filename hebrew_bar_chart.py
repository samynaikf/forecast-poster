import ast
import xlrd
import numpy as np
from overlayPNGs import *
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import sys
import csv
from datetime import date, timedelta
from dateutil.parser import parse

df = pd.read_csv('datcommodcurr.csv',header=1,index_col=0)
# df = pd.read_excel('datcommodcurr.xlsx',header=1,index_col=0)

def get_ROR(start_d,end_d,asset_name,forecast_type):
    try:
        end_val = df.loc[end_d][asset_name]
        start_val = df.iloc[df.index.get_loc(start_d) - 1][asset_name]

        if forecast_type == 'short':
            return round(100 * (start_val/end_val - 1),2)
        else:
            return round(100 * (end_val/start_val - 1),2)

    except Exception as e:
        print(e)
        return 0


def make_bar_chart(start_date,end_date,asset_list,benchmark,forecast_type,forecast_length):
    benchmarkROR = get_ROR(start_date,end_date,benchmark,'long')

    performance_dict = {}

    # get return performance
    for asset in asset_list:
        performance_dict[asset] = get_ROR(start_date,end_date,asset,forecast_type)

    labels = []
    values = []

    # sorting based on values
    for key, value in sorted(performance_dict.items(), key=lambda item: item[1]):
        labels.append(key)
        values.append(value)

    package_performance = round(np.mean(values),2)
    labels = [benchmark] + labels
    values = [benchmarkROR] + values

    n_bars = len(asset_list) + 1
    bar_width = .5
    index = np.arange(n_bars)

    img = plt.imread("small_logo.jpg")

    for plot_show in [True,False]:
        fig, ax = plt.subplots(figsize=(20,7.2))
        ax.yaxis.grid()
        bars = ax.bar(index,values,bar_width,color='blue',zorder=3,align='edge')

        for x in range(len(values)):
            if x == 0:
                continue
            if values[x] > 0:
                color = 'xkcd:leafy green'
            else:
                color = 'red'
            bars[x].set_color(color)

        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(labels,rotation=45,ha='center',fontsize=14)

        if plot_show:
            ax.set_ylabel('Percent Change',fontsize=16)
            set_bar_text = values
            ax.tick_params(axis='both', left=plot_show, top=False, right=False, bottom=True, labelleft=plot_show, labeltop=False, labelright=False, labelbottom=True)
        else:
            set_bar_text = labels
            ax.tick_params(axis='both', left=plot_show, top=False, right=False, bottom=False, labelleft=plot_show, labeltop=False, labelright=False, labelbottom=False)

        for x in range(len(values)):
            if values[x] >= 0:
                height = (bars[x].get_height()) + 0.03
                ax.text((bars[x].get_x() + bars[x].get_width()/2.0),height,set_bar_text[x],horizontalalignment='center',fontsize=16)
                if plot_show and not x == 0:
                    plt.imshow(img,extent=[bars[x].get_x()+.25*bar_width,bars[x].get_x()+.75*bar_width,height+.2,height+.4],aspect='auto')
            else:
                height = (bars[x].get_height()) - 0.15
                ax.text((bars[x].get_x() + bars[x].get_width()/2.0),height,set_bar_text[x],horizontalalignment='center',fontsize=16)
                if plot_show and not x == 0:
                    plt.imshow(img,extent=[bars[x].get_x()+.25*bar_width,bars[x].get_x()+.75*bar_width,height-.25,height-.05],aspect='auto')

        # fig.tight_layout()
        # fig.suptitle('Package Performance')

        hebrew_title = 'ביצועי נכסי החבילה לעומת המדד'
        hebrew_title = hebrew_title[::-1]

        # hebrew_title = 'Low P/E Stocks Performance'

        if forecast_length == 3:
            x_title = 'ימים'
            x_title = x_title[::-1] + ' 3'
        elif forecast_length == 7:
            x_title = 'שבוע'
            x_title = x_title[::-1]
        elif forecast_length == 14:
            x_title = 'יום'
            x_title = x_title[::-1] + ' 14'
        elif forecast_length == 30:
            x_title = 'חודש'
            x_title = x_title[::-1]
        elif forecast_length == 90:
            x_title = 'חודשים'
            x_title = x_title[::-1] + ' 3'
        elif forecast_length == 365:
            x_title = 'שנה'
            x_title = x_title[::-1]

        # x_title = '1 Year'

        if plot_show:
            output_name = 'demo_'+str(forecast_length)+'_'+forecast_type+'.png'
            title = '\nPackage Performance'
            fontsize = 28
            x_title = str(forecast_length) + " Days"
            ax.text((n_bars/2 - .6),(-3),x_title,fontsize=22)
            fig.suptitle(title,fontsize=fontsize,y=1.01)
        else:
            output_name = 'final_'+str(forecast_length)+'_'+forecast_type+'.png'
            fontsize = 28
            ax.set_xlabel(x_title,fontsize=26)
            fig.suptitle(hebrew_title,fontsize=fontsize,y=.95)

        plt.xlim(-1,11)
        plt.ylim(np.min(values)-.5,np.max(values)+.5)

        # plt.show()
        fig.savefig(output_name,transparent=True)
        plt.close()

        overlay_hebrew_chart(output_name)

# df_staging = pd.read_csv("staging_file.csv", header=None)
#
# start_date = df_staging.iloc[0, 1]
# end_date = df_staging.iloc[1, 1]
# asset_list = df_staging.values.tolist()[2][1:]
# benchmark = df_staging.iloc[3, 1]
# forecast_type = df_staging.iloc[4, 1]
# forecast_length = int(df_staging.iloc[5, 1])
#
# print(start_date)
# print(end_date)
# print(asset_list)
# print(benchmark)
# print(forecast_type)
# print(forecast_length)
book = xlrd.open_workbook('staging_file.xlsx')
sheet = book.sheet_by_index(0)
rows, cols = sheet.nrows, sheet.ncols

start_date = sheet.cell(0,1).value
end_date = sheet.cell(1,1).value
start_date = datetime.datetime(*xlrd.xldate_as_tuple(start_date, book.datemode))
end_date = datetime.datetime(*xlrd.xldate_as_tuple(end_date, book.datemode))
i = 0
for date in [start_date,end_date]:
    date_info = str(date).split(' ')[0].split('-')
    year = date_info[0][-2:]
    month = date_info[1]
    day = date_info[2]
    if month[0] == '0':
        month = month[1:]
    if day[0] == '0':
        day = day[1:]

    if i == 0:
        start_date = month+'/'+day+'/'+year
    else:
        end_date = month+'/'+day+'/'+year
    i += 1

asset_list = []
for x in range(cols-1):
    asset_list.append(sheet.cell(2,x+1).value)
benchmark = sheet.cell(3,1).value
forecast_type = sheet.cell(4,1).value
forecast_length = int(sheet.cell(5,1).value)
print(start_date)
print(end_date)
print(asset_list)
print(benchmark)
print(forecast_type)
print(forecast_length)

make_bar_chart(start_date,end_date,asset_list,benchmark,forecast_type,forecast_length)
