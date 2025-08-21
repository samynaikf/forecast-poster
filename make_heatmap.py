
import os
import time
import glob
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from overlayPNGs import overlay_heatmap
from get_package_name import get_package_name
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from get_index import get_index
import pandas as pd
import matplotlib
import shutil
import xlrd
import csv
from tqdm import tqdm
import operator
import pdb
def get_tables(data_file,forecast_length,start_d,df):
    '''
    Function to make dictionary from excel files

    parameters:
    -data file path
    -forecast_length
    -start date
    -data frame

    returns:
    -return_dict = dictionary with heatmap info
    -sp_chart = boolean that tells whether S&P 500 box should be included in heatmap
    -sp_dir = boolean that tells direction of S&P 500 prediction
    '''


    sp_keys = ['_Stocks_SP500_',
                '_top_5_SP500_',
                '_top_10_SP500_',
                '_top_15_SP500_',
                '_top_20_SP500_',
                '_top_40_SP500_',]
    sp_chart = False
    for key_val in sp_keys:
        if key_val in data_file:
            sp_chart = True
            break

    if forecast_length == '3':
        start_sheet = 0
        start_col = 1
        end_col = 5
    elif forecast_length == '7':
        start_sheet = 0
        start_col = 7
        end_col = 11
    elif forecast_length == '14':
        start_sheet = 0
        start_col = 13
        end_col = 17
    elif forecast_length == '30':
        start_sheet = 1
        start_col = 1
        end_col = 5
    elif forecast_length == '90':
        start_sheet = 1
        start_col = 7
        end_col = 11
    elif forecast_length == '365':
        start_sheet = 1
        start_col = 13
        end_col = 17

    return_dict = {'bright lime green': {},'lightgreen': {},'red': {},'salmon': {}}

    book = xlrd.open_workbook(data_file,formatting_info=True,on_demand=True)
    sheets = book.sheet_names()

    sheet = book.sheet_by_index(start_sheet)
    rows, cols = sheet.nrows, sheet.ncols

    reached_end = False
    sp_dir = True
    sp_color = None
    for row in range(5,rows-2,3):
        if reached_end:
            break

        for col in range(start_col,end_col+1):
            thecell = sheet.cell(row,col)

            xfx = sheet.cell_xf_index(row,col)
            xf = book.xf_list[xfx]
            bgx = xf.background.pattern_colour_index

            if bgx == 65 or bgx == 64:
                reached_end = True
                break
            if bgx == 11:
                if sp_chart:
                    if thecell.value == '^S&P500':
                        sp_dir = True
                        sp_color = 'bright lime green'
                if thecell.value == '' and not sheet.cell(row+1,col).value == '' and not sheet.cell(row+2,col).value == '':
                    return_dict['bright lime green'][start_sheet*100+row*10+col] = [sheet.cell(row+1,col).value,sheet.cell(row+2,col).value]
                elif sheet.cell(row+1,col).value == '' or sheet.cell(row+2,col).value == '':
                    continue
                else:
                    return_dict['bright lime green'][thecell.value] = [sheet.cell(row+1,col).value,sheet.cell(row+2,col).value]
            elif bgx == 42:
                if sp_chart:
                    if thecell.value == '^S&P500':
                        sp_dir = True
                        sp_color = 'lightgreen'
                if thecell.value == '' and not sheet.cell(row+1,col).value == '':
                    return_dict['lightgreen'][start_sheet*100+row*10+col] = [sheet.cell(row+1,col).value,sheet.cell(row+2,col).value]
                elif sheet.cell(row+1,col).value == '':
                    continue
                else:
                    return_dict['lightgreen'][thecell.value] = [sheet.cell(row+1,col).value,sheet.cell(row+2,col).value]
            elif bgx == 10:
                if sp_chart:
                    if thecell.value == '^S&P500':
                        sp_dir = False
                        sp_color = 'red'
                if thecell.value == '' and not sheet.cell(row+1,col).value == '':
                    return_dict['red'][start_sheet*100+row*10+col] = [sheet.cell(row+1,col).value,sheet.cell(row+2,col).value]
                elif sheet.cell(row+1,col).value == '':
                    continue
                else:
                    return_dict['red'][thecell.value] = [sheet.cell(row+1,col).value,sheet.cell(row+2,col).value]
            elif bgx == 29:
                if sp_chart:
                    if thecell.value == '^S&P500':
                        sp_dir = False
                        sp_color = 'salmon'
                if thecell.value == '' and not sheet.cell(row+1,col).value == '':
                    return_dict['salmon'][start_sheet*100+row*10+col] = [sheet.cell(row+1,col).value,sheet.cell(row+2,col).value]
                elif sheet.cell(row+1,col).value == '':
                    continue
                else:
                    return_dict['salmon'][thecell.value] = [sheet.cell(row+1,col).value,sheet.cell(row+2,col).value]
    print(sp_chart)

    return return_dict, sp_chart, sp_dir, sp_color

def make_heatmap(dict,forecast_type,sp_chart,top_20=False,gold_heatmap=False,sp_color=None):
    '''
    Function to choose boxes that will go into heatmap

    parameters:
    -heatmap dictionary
    -forecast type
    -sp_chart = sp_chart = boolean that tells whether S&P 500 box should be included in heatmap
    -top_20 = boolean that tells whether top 20 heatmap should be made

    returns:
    -dictionary with only values that will go in final heatmap
    '''
    total_boxes = len(dict['bright lime green'])+len(dict['lightgreen'])+len(dict['red'])+len(dict['salmon'])

    dark_goods = []
    light_goods = []
    dark_bads = []
    light_bads = []

    new_dict = {}

    if forecast_type == 'long' or forecast_type == 'long+short' or forecast_type == 'currencies':
        darks_good_id = 'bright lime green'
        lights_good_id = 'lightgreen'
        darks_bad_id = 'red'
        lights_bad_id = 'salmon'

    elif forecast_type == 'short':
        darks_good_id = 'red'
        lights_good_id = 'salmon'
        darks_bad_id = 'bright lime green'
        lights_bad_id = 'lightgreen'

    dg = len(dict[darks_good_id])
    g = len(dict[lights_good_id])
    db = len(dict[darks_bad_id])
    b = len(dict[lights_bad_id])

    if top_20:
        min_num = 20
    else:
        min_num = 10

    if forecast_type == 'currencies':
        dg_to_get = dg
        g_to_get = g
        db_to_get = db
        b_to_get = b
    elif dg + g + db + b < 35:
        dg_to_get = dg
        g_to_get = g
        db_to_get = db
        b_to_get = b

    else:
        count = 0
        dg_to_get = min(dg,35)
        g_to_get = min(g,35)
        db_to_get = min(db,35)
        b_to_get = min(b,35)
        count = (dg_to_get+g_to_get+db_to_get+b_to_get)
        if count > 35:
            extras = count - 35

            if dg_to_get > min_num:
                min_dg_to_get = min_num
                min_g_to_get = np.min([g_to_get,8])
            else:
                min_dg_to_get = dg_to_get
                min_g_to_get = np.min([min_num - dg_to_get + 8, g_to_get])

            while extras > 0:
                if db_to_get > 0:
                    db_to_get -= 1
                    extras -= 1
                if extras > 0 and b_to_get > 0:
                    b_to_get -= 1
                    extras -= 1
                if extras > 0 and g_to_get > min_g_to_get:
                    g_to_get -= 1
                    extras -= 1
                if extras > 0 and dg_to_get > min_dg_to_get:
                    dg_to_get -= 1
                    extras -= 1

    got_sp = False
    sp_box = {}
    got_gld = False
    got_xau = False
    gld_xau_boxes = {}

    for i, main_value in enumerate([
                    [light_goods,lights_good_id,g_to_get],
                    [dark_goods,darks_good_id,dg_to_get],
                    [light_bads,lights_bad_id,b_to_get],
                    [dark_bads,darks_bad_id,db_to_get],
                    ]):
        counter = 0
        for key, value in dict[main_value[1]].items():
            counter += 1
            if main_value[1] == 'red' or main_value[1] == 'salmon':
                if counter > (len(dict[main_value[1]]) - main_value[2]):
                    value.append(main_value[1])
                    main_value[0].append({key:value})
            else:
                if counter <= main_value[2]:
                    value.append(main_value[1])
                    main_value[0].append({key:value})

            if key == '^S&P500':
                sp_box[key] = value
                if main_value[1] == 'red' or main_value[1] == 'salmon':
                    if counter > (len(dict[main_value[1]]) - main_value[2]):
                        got_sp = True
                else:
                    if counter <= main_value[2]:
                        got_sp = True
            if key == 'GLD':
                gld_xau_boxes[key] = value
            if key == 'XAU':
                gld_xau_boxes[key] = value
        main_value[0][::-1]
        main_value[0] = main_value[0][len(main_value[0])-main_value[2]:]

    # print(got_sp)
    if (sp_chart and not got_sp):
        last_sig = 1000
        if forecast_type == 'short':
            for d in [dark_bads,light_bads,light_goods,dark_goods]:
                for value in d:
                    new_dict[list(value.keys())[0]] = value[list(value.keys())[0]]
        else:
            for d in [light_goods,dark_goods,dark_bads,light_bads]:
                for value in d:
                    new_dict[list(value.keys())[0]] = value[list(value.keys())[0]]

        temp_dict = {}
        for key, value in new_dict.items():
            temp_dict[key] = value[0]
        temp_dict['^S&P500'] = sp_box['^S&P500'][0]

        final_dict = {}

        sorted_x = sorted(temp_dict.items(), key=operator.itemgetter(1))[::-1]
        if forecast_type == 'short':
            if sorted_x[0][0] != '^S&P500':
                sorted_x.pop(0)
            else:
                sorted_x.pop(1)
        elif forecast_type == 'long':
            if sorted_x[-1][0] != '^S&P500':
                sorted_x.pop(-1)
            else:
                sorted_x.pop(-2)

        for item in sorted_x:
            if item[0] == '^S&P500':
                if sp_color is not None:
                    final_dict['^S&P500'] = [sp_box['^S&P500'][0],sp_box['^S&P500'][1],sp_color]
                else:
                    final_dict['^S&P500'] = [sp_box['^S&P500'][0],sp_box['^S&P500'][1],'lightgreen']
            else:
                final_dict[item[0]] = new_dict[item[0]]
        new_dict = final_dict

    else:
        if forecast_type == 'long' or forecast_type == 'long+short' or forecast_type == 'currencies':
            for x in range(len(dark_goods)):
                for key, value in dark_goods[x].items():
                    new_dict[key] = value
            for x in range(len(light_goods)):
                for key, value in light_goods[x].items():
                    new_dict[key] = value
            for x in range(len(light_bads)):
                for key, value in light_bads[x].items():
                    new_dict[key] = value
            for x in range(len(dark_bads)):
                for key, value in dark_bads[x].items():
                    new_dict[key] = value

        elif forecast_type == 'short':
            for x in range(len(dark_bads)):
                for key, value in dark_bads[x].items():
                    new_dict[key] = value
            for x in range(len(light_bads)):
                for key, value in light_bads[x].items():
                    new_dict[key] = value
            for x in range(len(light_goods)):
                for key, value in light_goods[x].items():
                    new_dict[key] = value
            for x in range(len(dark_goods)):
                for key, value in dark_goods[x].items():
                    new_dict[key] = value
    #print (new_dict)
    return new_dict

def print_heat_map(sheet_names,true_dates,abs_date,df,file_name,start_d,end_d,dict,forecast_length,forecast_type,index,short_forecast,commodities=False,hebrew=False,sp_chart=False,top_20=False,gold_heatmap=False, bitcoin=False):
    '''
    Function to plot heatmap

    parameters:
    -sheet_names = dictionary that holds info on filename and position in selection spreadsheet
    -true_dates = dictionary that holds info on dates on which file's predictions are made. This
        was a problem with using forecasts for days that are not the forecast
    -abs_date = date of actual forecast
    -df = data frame
    -file_name
    -start date
    -end date
    -forecast length
    -forecast type
    -index = benchmark index to use for chart
    -short_forecast = boolean that tells whether heatmap is less than 35 boxes

    returns:
    -saves heatmap into folder
    -dictionary of assets to show for accuracy chart
    '''

    if forecast_type == 'currencies':
        # fig,ax = plt.subplots(figsize=(12.5,27.6))
        fig,ax = plt.subplots(figsize=(5.25,11.3))
    # elif top_20:
    #     fig,ax = plt.subplots(figsize=(6.8,9))
    elif commodities:
        fig,ax = plt.subplots(figsize=(11.4,15.7))
    elif hebrew:
        fig,ax = plt.subplots(figsize=(11.4,15.6))
    elif 'bitcoin' in file_name.lower():
        fig,ax = plt.subplots(figsize=(11.4,15.7))
    else:
        fig,ax = plt.subplots(figsize=(11.5,15.6))

    x_indices_mult = .2
    if forecast_type == 'currencies':
        y_indices_mult = 1/(int((len(dict)/5))+1)
    else:
        y_indices_mult = 1/7

    font_to_use = {'fontname': 'Arial'}
    counter = 0

    best_performers = {}
    if forecast_type == 'currencies':
        text_adj = .035
        size = 12
        size2 = 10
        x_adj = 0.005
    else:
        text_adj = .06
        size = 24
        size2 = 22
        x_adj = 0


    if forecast_length == 3:
        starting_row = 1
    elif forecast_length == 7:
        starting_row = 29
    elif forecast_length == 14:
        starting_row = 57
    elif forecast_length == 30:
        starting_row = 85
    elif forecast_length == 90:
        starting_row = 113
    elif forecast_length == 365:
        starting_row = 141

    if (forecast_type == 'long' or forecast_type == 'short') and not top_20:
        retrieved_items = []
        spreadsheet_wb = abs_date+'.xlsx'
        # spreadsheet_wb = '04072019.xlsx'
        book = xlrd.open_workbook(spreadsheet_wb,on_demand=True)
        sheet = book.sheet_by_index(0)
        rows, cols = sheet.nrows, sheet.ncols
        #Loop through correct columns
        for col in range(2,cols,3):
            if sheet.cell(starting_row,col).value == '' or sheet.cell(starting_row,col).value == ' ':
                print("Couldn't find match in reference sheet")
                break
            thecell_info = sheet.cell(starting_row,col).value.replace('\\','/').split('/')
            package_name = thecell_info[-1]

            check_package_name = file_name.replace('\\','/').split('/')[-1]
            if sheet_names[file_name.replace('\\','/').split('/')[-1]] == sheet.cell(starting_row,col).value.replace('\\','/'):
                if forecast_type == 'long':
                    row_count = starting_row + 2
                elif forecast_type == 'short':
                    row_count = starting_row + 15
                for x in range(10):
                    if forecast_type == 'short':
                        best_performers[sheet.cell(row_count,col).value] = -100*sheet.cell(row_count,col+1).value
                    else:
                        best_performers[sheet.cell(row_count,col).value] = 100*sheet.cell(row_count,col+1).value
                    row_count += 1
                break

    MIN_BOXES = 35
    if short_forecast:
        if len(dict) >= 30:
            MIN_BOXES = 30
        elif len(dict) >= 20:
            MIN_BOXES = 20
        else:
            MIN_BOXES = 10
        if forecast_type == 'long':
            for x in range(35 - len(dict)):
                dict['missing_'+str(x)] = ['','','white']
        else:
            for q in range(len(dict)%5):
                del dict[list(dict.keys())[q]]


    actual_box_count = 0
    counter_i = 0

    for key, value in dict.items():

        counter_i += 1
        if 'missing' in str(key):
            counter += 1
            continue
        actual_box_count += 1

        x_index = counter % 5
        y_index = int(counter/5)
        graph_color = 'xkcd:' + value[-1]

        points = ((x_index*x_indices_mult),(1 - y_index*y_indices_mult - y_indices_mult))
        counter += 1
        rect = Rectangle(points,x_indices_mult,y_indices_mult,color=graph_color)
        ax.add_artist(rect)
        if (sp_chart and key == '^S&P500') or (gold_heatmap and (key == 'GLD' or key == 'XAU' or key == 'XAG' or key == 'CME_CI1' or key == 'SLV')):
            plt.plot([points[0],points[0]+x_indices_mult,points[0]+x_indices_mult,points[0],points[0]],[points[1]+y_indices_mult,points[1]+y_indices_mult,points[1],points[1],points[1]+y_indices_mult],'b',linewidth=6)

        if (forecast_type == 'long' and counter <= 10) or (forecast_type == 'short' and counter >= len(dict) - 9) or (forecast_type == 'long+short' and (counter <= 5 or counter >= 31)) or forecast_type == 'currencies' or \
            (forecast_type == 'long' and counter <= 20 and top_20) or (forecast_type == 'short' and counter >= 16 and top_20) or (sp_chart and key == '^S&P500') or \
            (forecast_type == 'long+short' and top_20 and (counter <= 10 or actual_box_count >= MIN_BOXES-9)) or (gold_heatmap and (key == 'GLD' or key == 'XAU' or key == 'XAG' or key == 'CME_CI1' or key == 'SLV')):

            if forecast_type == 'currencies':
                ROI = get_ROR(df,start_d,end_d,key)
                best_performers[key] = [ROI,value[-1]]
            elif forecast_type == 'long+short':
                ROI = get_ROR(df,start_d,end_d,key)
                best_performers[key] = ROI
            elif top_20:
                try:
                    ROI = get_ROR(df,start_d,end_d,key)
                except:
                    ROI = 0
                best_performers[key] = ROI

            if forecast_type == 'currencies':
                text_adj = .035
                size = 12
                size2 = 10
                x_adj = 0.005
                if 'missing' in str(key):
                    pass
                elif len(str(key)) > 7:
                    plt.text(points[0]+.004,points[1]+.072,key,color='black',fontweight='bold',fontsize=11,**font_to_use)
                else:
                    plt.text(points[0]+.01,points[1]+.072,key,color='black',fontweight='bold',fontsize=10,**font_to_use)
            else:
                if gold_heatmap and not (key == 'GLD' or key == 'XAU' or key == 'XAG' or key == 'CME_CI1' or key == 'SLV'):
                    pass
                else:
                    x_adj = 0
                    size = 24
                    size2 = 22
                    text_adj = .06
                    if len(str(key)) > 7:
                        plt.text(points[0]+.004,points[1]+.115,key,color='black',fontweight='bold',fontsize=22,**font_to_use)
                    else:
                        plt.text(points[0]+.01,points[1]+.115,key,color='black',fontweight='bold',fontsize=24,**font_to_use)

        if value[0] == 0 or value[0] == '' or value[0] == ' ':
            value[0] = .01
        if 'missing' in str(key):
            pass
        elif len(str('%.2f' % value[0])) > 7:
            plt.text(points[0]+x_adj+.04,points[1]+text_adj,'%.2f' % value[0],color='black',fontweight='bold',fontsize=size,**font_to_use)
        elif len(str('%.2f' % value[0])) == 7:
            plt.text(points[0]+x_adj+.05,points[1]+text_adj,'%.2f' % value[0],color='black',fontweight='bold',fontsize=size,**font_to_use)
        elif len(str('%.2f' % value[0])) == 6:
            plt.text(points[0]+x_adj+.07,points[1]+text_adj,'%.2f' % value[0],color='black',fontweight='bold',fontsize=size,**font_to_use)
        elif len(str('%.2f' % value[0])) == 5:
            plt.text(points[0]+x_adj+.09,points[1]+text_adj,'%.2f' % value[0],color='black',fontweight='bold',fontsize=size,**font_to_use)
        elif len(str('%.2f' % value[0])) == 4:
            plt.text(points[0]+x_adj+.11,points[1]+text_adj,'%.2f' % value[0],color='black',fontweight='bold',fontsize=size,**font_to_use)
        elif len(str('%.2f' % value[0])) == 3:
            plt.text(points[0]+x_adj+.13,points[1]+text_adj,'%.2f' % value[0],color='black',fontweight='bold',fontsize=size,**font_to_use)
        else:
            plt.text(points[0]+x_adj+.15,points[1]+text_adj,'%.2f' % value[0],color='black',fontweight='bold',fontsize=size,**font_to_use)

        if value[1] == 0 or value[1] == '' or value[1] == ' ':
            value[1] = .01
        if forecast_type == 'currencies':
            plt.text(points[0]+.01,points[1]+.005,'%.2f' % value[1],color='black',fontweight='bold',fontsize=size2,**font_to_use)
        elif 'missing' in str(key):
            pass
        else:
            plt.text(points[0]+.01,points[1]+.01,'%.2f' % value[1],color='black',fontweight='bold',fontsize=size2,**font_to_use)

    x_points = [0,.2,.4,.6,.8,1]
    y_points = []
    if forecast_type == 'currencies':
        for x in range(len(x_points)):
            if (x > 2 and len(dict) == 52) or (x > 1 and len(dict) == 51):
                plt.plot([x_points[x],x_points[x]],[y_indices_mult,1],'k',linewidth=2)
            else:
                plt.plot([x_points[x],x_points[x]],[0,1],'k',linewidth=2)
        if len(dict) == 50:
            for x in range(int(len(dict)/5) + 1):
                y_points.append(y_indices_mult*x)
                plt.plot([0,1],[y_points[-1],y_points[-1]],'k',linewidth=2)
        elif len(dict) == 51:
            for x in range(int(len(dict)/5) + 2):
                y_points.append(y_indices_mult*x)
                if x == 0:
                    plt.plot([0,.2],[y_points[-1],y_points[-1]],'k',linewidth=2)
                else:
                    plt.plot([0,1],[y_points[-1],y_points[-1]],'k',linewidth=2)
        else:
            for x in range(int(len(dict)/5) + 2):
                y_points.append(y_indices_mult*x)
                if x == 0:
                    plt.plot([0,.4],[y_points[-1],y_points[-1]],'k',linewidth=2)
                else:
                    plt.plot([0,1],[y_points[-1],y_points[-1]],'k',linewidth=2)


    #elif 'bitcoin' in file_name.lower():
     #   plt.plot([0,0],[6/7,1],'k',linewidth=2)
      #  plt.plot([.2,.2],[6/7,1],'k',linewidth=2)
       # plt.plot([.4,.4],[6/7,1],'k',linewidth=2)

        #plt.plot([0,.4],[1,1],'k',linewidth=2)
        #plt.plot([0,.4],[6/7,6/7],'k',linewidth=2)
    else:
        if short_forecast:
            if MIN_BOXES <= 20:
                for x in range(len(x_points)):
                    plt.plot([x_points[x],x_points[x]],[(3/7),1],'k',linewidth=2)
            else:
                for x in range(len(x_points)):
                    plt.plot([x_points[x],x_points[x]],[(1/7),1],'k',linewidth=2)
            if MIN_BOXES > 20:
                plt.plot([0,1],[(1/7),(1/7)],'k',linewidth=2)
                plt.plot([0,1],[(2/7),(2/7)],'k',linewidth=2)
            plt.plot([0,1],[(3/7),(3/7)],'k',linewidth=2)
            plt.plot([0,1],[(4/7),(4/7)],'k',linewidth=2)
            plt.plot([0,1],[(5/7),(5/7)],'k',linewidth=2)
            plt.plot([0,1],[(6/7),(6/7)],'k',linewidth=2)
            plt.plot([0,1],[1,1],'k',linewidth=2)
        else:
            for x in range(len(x_points)):
                plt.plot([x_points[x],x_points[x]],[0,1],'k',linewidth=2)
            for x in range(int(len(dict)/5) + 1):
                y_points.append(y_indices_mult*x)
                plt.plot([0,1],[y_points[-1],y_points[-1]],'k',linewidth=2)

    if gold_heatmap:
        pass
    elif top_20:
        if forecast_type == 'long':
            plt.plot([0,0,1,1,0],[y_indices_mult*3,y_indices_mult*7,y_indices_mult*7,y_indices_mult*3,y_indices_mult*3],'b',linewidth=6)
        elif forecast_type == 'short':
            plt.plot([0,0,1,1,0],[y_indices_mult*0,y_indices_mult*4,y_indices_mult*4,y_indices_mult*0,y_indices_mult*0],'b',linewidth=6)
        elif forecast_type == 'long+short':
            plt.plot([0,0,1,1,0],[y_indices_mult*0,y_indices_mult*2,y_indices_mult*2,y_indices_mult*0,y_indices_mult*0],'b',linewidth=6)
            plt.plot([0,0,1,1,0],[y_indices_mult*5,y_indices_mult*7,y_indices_mult*7,y_indices_mult*5,y_indices_mult*5],'b',linewidth=6)
    #elif 'bitcoin' in file_name.lower():
     #   plt.plot([0,0,.4,.4,0],[1,6/7,6/7,1,1],'b',linewidth=6)
    elif short_forecast and forecast_type == 'short':
        if MIN_BOXES == 20:
            plt.plot([0,0,1,1,0],[y_indices_mult*5,y_indices_mult*3,y_indices_mult*3,y_indices_mult*5,y_indices_mult*5],'b',linewidth=6)
        elif MIN_BOXES == 30:
            plt.plot([0,0,1,1,0],[y_indices_mult*1,y_indices_mult*3,y_indices_mult*3,y_indices_mult*1,y_indices_mult*1],'b',linewidth=6)
        else:
            plt.plot([0,0,1,1,0],[y_indices_mult*0,y_indices_mult*2,y_indices_mult*2,y_indices_mult*0,y_indices_mult*0],'b',linewidth=6)
    elif forecast_type == 'long':
        plt.plot([0,0,1,1,0],[y_indices_mult*5,y_indices_mult*7,y_indices_mult*7,y_indices_mult*5,y_indices_mult*5],'b',linewidth=6)
    elif forecast_type == 'short':
        plt.plot([0,0,1,1,0],[y_indices_mult*0,y_indices_mult*2,y_indices_mult*2,y_indices_mult*0,y_indices_mult*0],'b',linewidth=6)
    elif forecast_type == 'long+short':
        plt.plot([0,0,1,1,0],[y_indices_mult*6,y_indices_mult*7,y_indices_mult*7,y_indices_mult*6,y_indices_mult*6],'b',linewidth=6)
        plt.plot([0,0,1,1,0],[y_indices_mult*0,y_indices_mult*1,y_indices_mult*1,y_indices_mult*0,y_indices_mult*0],'b',linewidth=6)
    elif forecast_type == 'currencies':
        if len(dict) == 50:
            plt.plot([0,0,1,1,0],[0,y_indices_mult*11,y_indices_mult*11,0,0],'b',linewidth=3)
        elif len(dict) == 51:
            plt.plot([0,0,1,1,.2,.2,0],[0,y_indices_mult*11,y_indices_mult*11,y_indices_mult,y_indices_mult,0,0],'b',linewidth=3)
        else:
            plt.plot([0,0,1,1,.4,.4,0],[0,y_indices_mult*11,y_indices_mult*11,y_indices_mult,y_indices_mult,0,0],'b',linewidth=3)

    plt.xlim(-.01,1.01)
    plt.ylim(-.01,1.01)
    plt.tick_params(top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # plt.show()
    fig.savefig('heatmap_demo.png',bbox_inches='tight',pad_inches=0.0,dpi=50)

    return best_performers

def get_ROR(df,start_d,end_d,asset_name):
    if asset_name == 'CME_IE1':
        asset_name = 'CME_CL1'
    end_val = df.loc[end_d][asset_name]
    start_val = df.iloc[df.index.get_loc(start_d) - 1][asset_name]

    return round(100 * (end_val/start_val - 1),2)




def start_process(abs_date,path_to_folder,true_dates,sheet_names):
    '''
    Function to start heatmap generation, path_to_folder gives folder where excel forecasts are stored
    '''
    #Dictionary for conversion of filename info to calendar dates
    calendar_dates = {'January': '1','February': '2','March': '3','April': '4','May': '5','June': '6',
                    'July': '7','August': '8','September': '9','October': '10','November': '11','December': '12',
                    'Jan': '1','Feb': '2','Mar': '3','Apr': '4','May': '5','Jun': '6',
                    'Jul': '7','Aug': '8','Sep': '9','Oct': '10','Nov': '11','Dec': '12'}

    #Dictionary to convert index to forecast horizon
    index_to_horizon = {0:3,1:7,2:14,3:30,4:90,5:365}

    #Dictionary to convert horizon to forecast index
    horizon_to_index = {'3':0,'7':1,'14':2,'30':3,'90':4,'365':5}

    #Get all forecast files in folder
    files = os.listdir(path_to_folder)
    # output_date = path_to_folder.split('Output-')[-1]
    output_date = path_to_folder.split('/')[0]

    #Make data frame with pandas
    df = pd.read_csv('datcommodcurr.csv',header=1,index_col=0)
    print("Opening data file")
    #Go through files
    for name in tqdm(files,desc="Creating heatmaps",total=len(files)):
        top_20 = False
        commodities = False
        gold_heatmap = False
        bitcoin = False
        if '.DS' in name:
            continue
        if ('commodities' in name or 'Commodities' in name or 'InterestRates' in name or 'Commodity' in name):
            commodities = True
        if ('BITCOIN' in name):
            bitcoin = True
            #print('var flipped') #check print
        if 'GLD_XAU' in name or 'XAU_GLD_XAG' in name:
            gold_heatmap = True
            #pdb.set_trace()
        # print(name)
        name = path_to_folder+'/'+name
        try:
        # if True:
            #Find corresponding index for forecast file
            name_info = name.split(' ')
            index_name = get_index(name)

            new_name = name
            has_sticky = False
            if name_info[-1] == 'sticky.xls':
                has_sticky = True
                new_name = name[:-11] + '.xls'
            name_info = new_name.split(' ')

            if 'currencies' in name or 'Currencies' in name:
                forecast_type = 'currencies'

                forecast_length = name_info[-7]
                if (forecast_length == 'one' or forecast_length == '1') and name_info[-6] == 'year':
                    forecast_length = '365'
            else:
                if '_top_20 ' in new_name:
                    top_20 = True
                    name_info = name.replace('_top_20','').split(' ')
                    index_name = get_index(name)
                    new_name = name.replace('_top_20','')
                
                forecast_type = name_info[-5]

                forecast_length = name_info[-7]
                if (forecast_length == 'one' or forecast_length == '1') and name_info[-6] == 'year':
                    forecast_length = '365'

            if name_info[-3] == '0':
                name_info[-3] = name_info[-3][1:]
            date = name_info[-3] + '_' + name_info[-2] + '_' + name_info[-1][:4]

            day = name_info[-3]

            if day[0] == '0':
                day = day[1]
            calendar_date = calendar_dates[name_info[-2]] + '/' + day + '/' + name_info[-1][2:4]

            start_d_info = name_info[0].split('_')
            if start_d_info[-3][0] == '0':
                start_d_info[-3] = start_d_info[-3][1:]
            start_d = calendar_dates[start_d_info[-2]] + '/' + start_d_info[-3] + '/' +  start_d_info[-1][-2:]

            index_ROI = get_ROR(df,start_d,calendar_date,index_name)
            table, sp_chart, sp_dir, sp_color = get_tables(name,forecast_length,start_d,df)
            new_dict = make_heatmap(table,forecast_type,sp_chart,top_20=top_20,gold_heatmap=gold_heatmap,sp_color=sp_color)
            short_forecast = False
            if len(new_dict) < 35:
                short_forecast = True

            for hebrew in [True,False]:
                # if hebrew:
                    # print("Making hebrew heatmap")
                    # pass
                # else:
                    # print("Making regular heatmap")
                best_performers = print_heat_map(sheet_names,true_dates,abs_date,df,name,start_d,calendar_date,new_dict,int(forecast_length),forecast_type,index_to_horizon[horizon_to_index[forecast_length]],short_forecast,commodities=commodities,hebrew=hebrew,sp_chart=sp_chart,top_20=top_20,gold_heatmap=gold_heatmap, bitcoin=bitcoin)
                picture_path = overlay_heatmap(output_date,forecast_type,index_name,index_ROI,best_performers,horizon_to_index[forecast_length],new_name, new_dict, 'heatmap_demo.png',commodities=commodities,hebrew=hebrew,sp_chart=sp_chart,sp_dir=sp_dir,has_sticky=has_sticky,top_20=top_20,short_forecast=short_forecast,gold_heatmap=gold_heatmap, bitcoin_chart=bitcoin) #edit: add dict input
                h_num = 0
                c = 0
                all_vals = []
                # for key, value in best_performers.items():
                #     if key == '':
                #         continue
                #     all_vals.append(value)
                #     if forecast_type == 'long' or (forecast_type == 'long+short' and c < 5):
                #         if value > 0:
                #             h_num += 1
                #     elif forecast_type == 'short' or (forecast_type == 'long+short' and c > 4):
                #         if value < 0:
                #             h_num += 1
                #     c += 1

                # if not hebrew and not forecast_type == 'currencies':
                #     del best_performers['']
                #     x = sorted(((v,k) for k,v in best_performers.items()))
                #     vals = sorted(best_performers.values())
                #     if forecast_type == 'short':
                #         f_best_asset = x[0][1]
                #         s_best_asset = x[1][1]
                #         t_best_asset = x[2][1]
                #         f_best_return = -round(vals[0],2)
                #         s_best_return = -round(vals[1],2)
                #         t_best_return = -round(vals[2],2)
                #         overall_return = -round(np.mean(all_vals),2)
                #     else:
                #         f_best_asset = x[-1][1]
                #         s_best_asset = x[-2][1]
                #         t_best_asset = x[-3][1]
                #         f_best_return = round(vals[-1],2)
                #         s_best_return = round(vals[-2],2)
                #         t_best_return = round(vals[-3],2)
                #         overall_return = round(np.mean(all_vals),2)
                #
                #     if 'sticky' in name:
                #         sticky_val = True
                #     else:
                #         sticky_val = False
                #
                #     print("\n")
        except Exception as e:
            print(e)
            shutil.copyfile(name,output_date+'/OutputFailed/' + name.replace('\\','/').split('/')[-1])
            print("Unable to make heatmap for file: {}".format(name))
            print("\n")
#
