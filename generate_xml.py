'''
Script to generate XML files for wordpress upload
'''
from get_paragraph import get_paragraph
from get_icon import get_icon
import os
import glob
import numpy as np
from get_company_info import *
from package_info import *
import matplotlib.pyplot as plt
import pandas as pd
import operator
import csv


def add_item(PACKAGE_NAME="",
            PACKAGE_URL_NAME="",
            ASSET_TYPE="",
            RETURNS_1_FULL="",
            RETURNS_2="",
            RETURNS_3="",
            FORECAST_LENGTH="",
            RETURNS_1_LEFT="",
            RETURNS_1_RIGHT="",
            LENGTH_NUM="",
            LENGTH_UNIT="",
            PACKAGE_CATEGORY="",
            FORECAST_DIRECTION="",
            START_DATE="",
            END_DATE="",
            AVERAGE_RETURN="",
            HIT_NUM="",
            ASSET_1="",
            ASSET_2="",
            ASSET_3="",
            ASSET_4="",
            ASSET_5="",
            ASSET_6="",
            ASSET_7="",
            ASSET_8="",
            ASSET_9="",
            ASSET_10="",
            ASSET_LOWER_1="",
            ASSET_LOWER_2="",
            ASSET_LOWER_3="",
            ASSET_LOWER_4="",
            ASSET_LOWER_5="",
            ASSET_LOWER_6="",
            ASSET_LOWER_7="",
            ASSET_LOWER_8="",
            ASSET_LOWER_9="",
            ASSET_LOWER_10="",
            BENCHMARK_NAME="",
            BENCHMARK_RETURN="",
            YYYY="",
            MM="",
            DD="",
            GMT_H="",
            HH="",
            MINUTE="",
            SS="",
            COMPANY_INFO="",
            GIF_NAME="",
            PACKAGE_SLUG="",
            ICON_LINK="",
            HEADER_PARAGRAPH=""):

    OUT_PERFORMANCE = str(round(float(AVERAGE_RETURN) - float(BENCHMARK_RETURN),2))

    f = open('content.txt',encoding="utf-8")
    content = f.read()

    content = content.replace('HEADER_PARAGRAPH',HEADER_PARAGRAPH)
    content = content.replace('PACKAGE_NAME',PACKAGE_NAME)
    content = content.replace('PACKAGE_URL_NAME', PACKAGE_URL_NAME.lower())
    content = content.replace('ASSET_TYPE', ASSET_TYPE)
    content = content.replace('RETURNS_1_FULL', RETURNS_1_FULL)
    content = content.replace('RETURNS_2', RETURNS_2)
    content = content.replace('RETURNS_3', RETURNS_3)
    content = content.replace('FORECAST_LENGTH', FORECAST_LENGTH)
    content = content.replace('RETURNS_1_LEFT', RETURNS_1_LEFT)
    content = content.replace('RETURNS_1_RIGHT', RETURNS_1_RIGHT)
    content = content.replace('LENGTH_NUM', LENGTH_NUM)
    content = content.replace('LENGTH_UNIT', LENGTH_UNIT)
    content = content.replace('PACKAGE_CATEGORY', PACKAGE_CATEGORY)
    content = content.replace('FORECAST_DIRECTION', FORECAST_DIRECTION)
    content = content.replace('START_DATE', START_DATE)
    content = content.replace('END_DATE', END_DATE)
    content = content.replace('AVERAGE_RETURN', AVERAGE_RETURN)
    content = content.replace('HIT_NUM', HIT_NUM)
    content = content.replace('ASSET_1', ASSET_1)
    content = content.replace('ASSET_2', ASSET_2)
    content = content.replace('ASSET_3', ASSET_3)
    content = content.replace('ASSET_4', ASSET_4)
    content = content.replace('ASSET_5', ASSET_5)
    content = content.replace('ASSET_6', ASSET_6)
    content = content.replace('ASSET_7', ASSET_7)
    content = content.replace('ASSET_8', ASSET_8)
    content = content.replace('ASSET_9', ASSET_9)
    content = content.replace('ASSET_10', ASSET_10)
    content = content.replace('ASSET_LOWER_1', ASSET_LOWER_1)
    content = content.replace('ASSET_LOWER_2', ASSET_LOWER_2)
    content = content.replace('ASSET_LOWER_3', ASSET_LOWER_3)
    content = content.replace('ASSET_LOWER_4', ASSET_LOWER_4)
    content = content.replace('ASSET_LOWER_5', ASSET_LOWER_5)
    content = content.replace('ASSET_LOWER_6', ASSET_LOWER_6)
    content = content.replace('ASSET_LOWER_7', ASSET_LOWER_7)
    content = content.replace('ASSET_LOWER_8', ASSET_LOWER_8)
    content = content.replace('ASSET_LOWER_9', ASSET_LOWER_9)
    content = content.replace('ASSET_LOWER_10', ASSET_LOWER_10)
    content = content.replace('BENCHMARK_NAME', BENCHMARK_NAME)
    content = content.replace('BENCHMARK_RETURN', BENCHMARK_RETURN)
    content = content.replace('YYYY', YYYY)
    content = content.replace('MM', MM)
    content = content.replace('DD', DD)
    content = content.replace('GMT_H', GMT_H)
    content = content.replace('HH', HH)
    content = content.replace('MINUTE', MINUTE)
    content = content.replace('SS', SS)
    content = content.replace('COMPANY_INFO', COMPANY_INFO)
    content = content.replace('GIF_NAME', GIF_NAME)
    content = content.replace('OUT_PERFORMANCE', OUT_PERFORMANCE)
    content = content.replace('PACKAGE_SLUG', PACKAGE_SLUG)
    content = content.replace('ICON_LINK', ICON_LINK)


    '''
    picture path format:
    --------------------
    /YYYY/MM/IKForecast_top_10_Israel_08_Apr_2019-3-days-long-until-11-April-2019.gif
    '''

    return content


month_name_to_num = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
                    'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


def generate_xml(directory,SITE_URL):
    if os.path.isfile('Output.xml'):
        os.remove('Output.xml')

    YYYY = directory[-5:-1]
    MM = directory[:2]
    DD = directory[2:4]

    f = open('outer_wrapper.txt',encoding="utf-8")
    outer_wrapper = f.read()

    all_content = ""

    folders = glob.glob(directory+'*CSV*/')
    gif_folders = glob.glob(directory+'*GIF*/')
    for i, folder in enumerate(folders):
        # if i == 1:
            # break
        if 'HEBREW' in folder:
            continue
        files = glob.glob(folder+'*.csv')
        for j, file in enumerate(files):

            file_info = file.replace('\\','/').split('/')[-1].split('-')
            for gif_folder in gif_folders:
                gif_files = glob.glob(gif_folder+'*.gif')
                for gif_file in gif_files:
                    if file_info[0] in gif_file:
                        GIF_NAME = gif_file.replace('\\','/').split('/')[-1]
                        break

            LENGTH_NUM = file_info[1]
            LENGTH_UNIT = file_info[2]
            FORECAST_DIRECTION = file_info[3]
            package_info = file_info[0].split('_')

            with open(file) as csvFile:
                csv_reader = csv.reader(csvFile)
                a_list = []
                ror = []
                asset_list = {}
                hit_num = 0
                for i, row in enumerate(csv_reader):
                    if i == 0:
                        start_date = row[1]
                    elif i == 1:
                        end_date = row[1]
                    elif i >= 3 and i <= 12:
                        asset_list[row[0]] = row[2]
                        ror.append(row[2])
                        a_list.append(row[0])
                        if row[3] == '1':
                            hit_num += 1
                    elif i == 13:
                        average_return = row[2]
                    elif i == 14:
                        benchmark_name = row[0]
                        benchmark_return = row[2]

                inds = np.array(ror).argsort()[::-1]
                asset_returns = []
                asset_list = []
                for ind in inds:
                    asset_returns.append(ror[ind])
                    asset_list.append(a_list[ind])

                if len(get_company_info(asset_list[0])) < 3:
                    c_info = ' '
                else:
                    c_info = get_company_info(asset_list[0])

                all_content += add_item(
                                        PACKAGE_NAME=get_package_name(file),
                                        PACKAGE_URL_NAME=get_package_name(file).replace(' ','-'),
                                        ASSET_TYPE='',
                                        RETURNS_1_FULL=str(asset_returns[0]),
                                        RETURNS_2=str(asset_returns[1]),
                                        RETURNS_3=str(asset_returns[2]),
                                        FORECAST_LENGTH=LENGTH_NUM+' '+LENGTH_UNIT,
                                        RETURNS_1_LEFT=str(asset_returns[0]).split('.')[0],
                                        RETURNS_1_RIGHT=str(asset_returns[0]).split('.')[1],
                                        LENGTH_NUM=LENGTH_NUM,
                                        LENGTH_UNIT=LENGTH_UNIT,
                                        PACKAGE_CATEGORY=get_package_name(file),
                                        FORECAST_DIRECTION=FORECAST_DIRECTION,
                                        START_DATE=start_date,
                                        END_DATE=end_date,
                                        AVERAGE_RETURN=str(average_return),
                                        HIT_NUM=str(hit_num),
                                        ASSET_1=asset_list[0],
                                        ASSET_2=asset_list[1],
                                        ASSET_3=asset_list[2],
                                        ASSET_4=asset_list[3],
                                        ASSET_5=asset_list[4],
                                        ASSET_6=asset_list[5],
                                        ASSET_7=asset_list[6],
                                        ASSET_8=asset_list[7],
                                        ASSET_9=asset_list[8],
                                        ASSET_10=asset_list[9],
                                        ASSET_LOWER_1=asset_list[0].lower(),
                                        ASSET_LOWER_2=asset_list[1].lower(),
                                        ASSET_LOWER_3=asset_list[2].lower(),
                                        ASSET_LOWER_4=asset_list[3].lower(),
                                        ASSET_LOWER_5=asset_list[4].lower(),
                                        ASSET_LOWER_6=asset_list[5].lower(),
                                        ASSET_LOWER_7=asset_list[6].lower(),
                                        ASSET_LOWER_8=asset_list[7].lower(),
                                        ASSET_LOWER_9=asset_list[8].lower(),
                                        ASSET_LOWER_10=asset_list[9].lower(),
                                        BENCHMARK_NAME=benchmark_name,
                                        BENCHMARK_RETURN=str(benchmark_return),
                                        YYYY=YYYY,
                                        MM=MM,
                                        DD=DD,
                                        GMT_H="10",
                                        HH="07",
                                        MINUTE="23",
                                        SS="04",
                                        COMPANY_INFO=c_info,
                                        GIF_NAME=GIF_NAME.replace(' ','-').lower(),
                                        PACKAGE_SLUG=get_package_slug(get_package_name(file)),
                                        ICON_LINK=get_icon(get_package_name(file)),
                                        HEADER_PARAGRAPH=get_paragraph(get_package_name(file))
                                        )


    outer_wrapper = outer_wrapper.replace('INSERT_CONTENT',all_content)
    outer_wrapper = outer_wrapper.replace('SITE_URL',SITE_URL.lower())

    # print(outer_wrapper)
    text_file = open(directory + directory[:-1]+".xml", "w",encoding="utf-8")
    text_file.write(outer_wrapper)
    text_file.close()


















#
