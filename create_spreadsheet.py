import xlrd
import xlsxwriter


def colToExcel(col):
    excelCol = str()
    div = col
    while div:
        (div, mod) = divmod(div-1, 26)
        excelCol = chr(mod + 65) + excelCol
    return excelCol

def make_reference_sheet(end_date,info_dict,workbook):
    '''
    Makes reference sheet with package name and top 10 asset names and
    performance. This sheet will be linked to main spreadsheet and can be
    used as reference to see performance of individual assets.

    Input:
    ------
        * Dictionary where keys are file names (e.g. Bovespa_12_Mar_2019
        3 days long until March 15 2019) and values are matrix where items are
        array of assets and percentage performance (e.g. ['AAPL', 10.45]). The
        first 10 arrays are long performance, and the last 10 are short
        performance.

    Returns:
    --------
        * Dictionary where keys are files names and values are cell numbers
        to link from spreadsheet to reference sheet.
    '''

    return_dict = {}
    percent_dict = {}

    title_format1 = workbook.add_format()
    title_format1.set_border_color('black')
    title_format1.set_border()

    title_format2 = workbook.add_format()
    title_format2.set_bold()
    title_format2.set_border_color('black')
    title_format2.set_border()

    cell_format1 = workbook.add_format({'num_format': '0.00%'})
    cell_format1.set_bg_color('#99FF99')
    cell_format1.set_border_color('black')
    cell_format1.set_border()
    cell_format2 = workbook.add_format({'num_format': '0.00%'})
    cell_format2.set_bg_color('#FF9999')
    cell_format2.set_border_color('black')
    cell_format2.set_border()
    cell_format3 = workbook.add_format()
    cell_format3.set_bg_color('#99FF99')
    cell_format3.set_border_color('black')
    cell_format3.set_border()
    cell_format4 = workbook.add_format()
    cell_format4.set_bg_color('#FF9999')
    cell_format4.set_border_color('black')
    cell_format4.set_border()
    cell_format5 = workbook.add_format({'num_format': '0.00%'})
    cell_format5.set_bg_color('#42D3FF')
    cell_format5.set_border_color('black')
    cell_format5.set_border()
    cell_format6 = workbook.add_format()
    cell_format6.set_bg_color('#42D3FF')
    cell_format6.set_border_color('black')
    cell_format6.set_border()


    worksheet = workbook.add_worksheet('Reference_Sheet')
    loop = 0
    for main_key, main_value in info_dict.items():
        counter = 2
        if loop == 0:
            starting_row = 1
        elif loop == 1:
            starting_row = 29
        elif loop == 2:
            starting_row = 57
        elif loop == 3:
            starting_row = 85
        elif loop == 4:
            starting_row = 113
        elif loop == 5:
            starting_row = 141
        loop += 1

        for key, value, in main_value.items():
            col_name = xlsxwriter.utility.xl_col_to_name(counter)
            if key in return_dict.keys():
                return_dict['X'+key] = col_name+str(starting_row+1)
            else:
                return_dict[key] = col_name+str(starting_row+1)
            col_name2 = xlsxwriter.utility.xl_col_to_name(counter+1)
            if key in percent_dict.keys():
                percent_dict['X'+key] = col_name2
            else:
                percent_dict[key] = col_name2
            worksheet.write(col_name+str(starting_row+1),key,title_format1)
            worksheet.write(col_name2+str(starting_row+1),'%',title_format1)

            worksheet.write(col_name+str(starting_row+2),'Long',title_format2)
            worksheet.write(col_name+str(starting_row+15),'Short',title_format2)
            row_count = starting_row + 3
            for key2, value2 in value.items():
                item_count = 0
                if len(value2) == 1:
                    worksheet.write(col_name2+str(row_count),0)
                for item in value2:
                    if item == value2[-1]:
                        format = cell_format5
                        format_main = cell_format6
                        if row_count < starting_row+15:
                            row_num = starting_row + 13
                        else:
                            row_num = starting_row + 26
                    elif value2[item_count][1] > 0:
                        format = cell_format1
                        format_main = cell_format3
                        row_num = row_count
                    else:
                        format = cell_format2
                        format_main = cell_format4
                        row_num = row_count
                    worksheet.write(col_name+str(row_num),value2[item_count][0],format_main)
                    worksheet.write(col_name2+str(row_num),value2[item_count][1],format)
                    item_count += 1
                    if item == value2[-1]:
                        row_count = starting_row + 15
                    row_count += 1
            worksheet.set_column(col_name+':'+col_name,60)
            counter += 3

    return return_dict, percent_dict, worksheet


def make_workbook(end_date,info_Mat,info_dict,best_currency):
    '''
    Create selection spreadsheet
    '''

    captions = ['3 days','7 days','14 days','1 month','3 months','1 year']
    workbook = xlsxwriter.Workbook(end_date+'.xlsx')
    link_dict, percent_dict, worksheet0 = make_reference_sheet(end_date,info_dict,workbook)
    reference_book_name = end_date+'.xlsx#Reference_Sheet'

    #Initialize formats
    cell_format1 = workbook.add_format({'num_format': '0.00%'})
    cell_format1.set_bg_color('#00CC00')
    cell_format2 = workbook.add_format({'num_format': '0.00%'})
    cell_format2.set_bg_color('#99FF99')
    cell_format3 = workbook.add_format({'num_format': '0.00%'})
    cell_format3.set_bg_color('#FF9999')
    cell_format4 = workbook.add_format({'num_format': '0.00%'})
    cell_format4.set_bg_color('#FF0000')
    cell_format1b = workbook.add_format()
    cell_format1b.set_bg_color('#00CC00')
    cell_format2b = workbook.add_format()
    cell_format2b.set_bg_color('#99FF99')
    cell_format3b = workbook.add_format()
    cell_format3b.set_bg_color('#FF9999')
    cell_format4b = workbook.add_format()
    cell_format4b.set_bg_color('#FF0000')
    percent_fmt = workbook.add_format({'num_format': '0.00%'})
    percent_fmt2 = workbook.add_format({'num_format': '0.00%'})
    percent_fmt2.set_bg_color('#00CC00')
    percent_fmt3 = workbook.add_format({'num_format': '0.00%'})
    percent_fmt3.set_bg_color('#FF0000')
    zero_fmt = workbook.add_format()
    zero_fmt.set_bg_color('#F9A333')

    #Make sheets
    worksheet1 = workbook.add_worksheet(captions[0])
    worksheet2 = workbook.add_worksheet(captions[1])
    worksheet3 = workbook.add_worksheet(captions[2])
    worksheet4 = workbook.add_worksheet(captions[3])
    worksheet5 = workbook.add_worksheet(captions[4])
    worksheet6 = workbook.add_worksheet(captions[5])
    all_worksheets = [worksheet1,worksheet2,worksheet3,worksheet4,worksheet5,worksheet6]

    #Add tables to sheets
    for x in range(len(info_Mat)):
        all_worksheets[x].set_column('C:C',60)
        all_worksheets[x].set_column('D:R',12)
        all_worksheets[x].set_column('S:U',14)
        all_worksheets[x].write('B1',captions[x]+' sheet')

        num = str(len(info_Mat[x])+5)
        #Add table
        all_worksheets[x].add_table('B4:U'+num,{'data':info_Mat[x],'columns':[{'header':'Info Link'},
                                                                            {'header':'Package Name'},
                                                                            {'header':'Start Date'},
                                                                            {'header':'End Date'},
                                                                            {'header':'Long Top 5'},
                                                                            {'header':'Long Top 10'},
                                                                            {'header':'Long Top 20'},
                                                                            {'header':'Long Hit Ratio'},
                                                                            {'header':'Long Zeros'},
                                                                            {'header':'Short Top 5'},
                                                                            {'header':'Short Top 10'},
                                                                            {'header':'Short Top 20'},
                                                                            {'header':'Short Hit Ratio'},
                                                                            {'header':'Short Zeros'},
                                                                            {'header':'S&P500 Prediction'},
                                                                            {'header':'Benchmark'},
                                                                            {'header':'Performance'},
                                                                            {'header':'Include Long'},
                                                                            {'header':'Include Short'},
                                                                            {'header':'Include Long+Short'}]})


        #Determine colors of rows
        for z in range(len(info_Mat[x])):
            if x == 0:
                starting_row = 1
                end_index1 = 1
                end_index2 = 2
                end_index3 = 2
            elif x == 1:
                starting_row = 29
                end_index1 = 2
                end_index2 = 2
                end_index3 = 2
            elif x == 2:
                starting_row = 57
                end_index1 = 2
                end_index2 = 2
                end_index3 = 2
            elif x == 3:
                starting_row = 85
                end_index1 = 2
                end_index2 = 2
                end_index3 = 2
            elif x == 4:
                starting_row = 113
                end_index1 = 3
                end_index2 = 3
                end_index3 = 3
            elif x == 5:
                starting_row = 141
                end_index1 = 3
                end_index2 = 3
                end_index3 = 3


            if 'X'+info_Mat[x][z][1] in percent_dict.keys() and x > 0:
                long_range = percent_dict['X'+info_Mat[x][z][1]] + str(starting_row+3)+':' + percent_dict['X'+info_Mat[x][z][1]] + str(starting_row+12)
                short_range = percent_dict['X'+info_Mat[x][z][1]] + str(starting_row+16)+':' + percent_dict['X'+info_Mat[x][z][1]] + str(starting_row+25)
            else:
                long_range = percent_dict[info_Mat[x][z][1]] + str(starting_row+3)+':' + percent_dict[info_Mat[x][z][1]] + str(starting_row+12)
                short_range = percent_dict[info_Mat[x][z][1]] + str(starting_row+16)+':' + percent_dict[info_Mat[x][z][1]] + str(starting_row+25)

            long_formula = "=AVERAGE(Reference_Sheet!"+long_range+")"
            short_formula = "=AVERAGE(Reference_Sheet!"+short_range+")"

            long_zero_formula = "=COUNTIF(Reference_Sheet!"+long_range+",0)"
            short_zero_formula = "=COUNTIF(Reference_Sheet!"+short_range+",0)"


            for row_index in [4,6,7]:
                if (info_Mat[x][z][row_index] > 0 and info_Mat[x][z][row_index] > info_Mat[x][z][16] and info_Mat[x][z][7] > .5):
                    all_worksheets[x].write(colToExcel(row_index+2)+str(4+z+1),info_Mat[x][z][row_index],cell_format1)
                elif (info_Mat[x][z][row_index] > 0 and info_Mat[x][z][row_index] > info_Mat[x][z][16]):
                    all_worksheets[x].write(colToExcel(row_index+2)+str(4+z+1),info_Mat[x][z][row_index],cell_format2)
                elif (info_Mat[x][z][row_index] > 0):
                    all_worksheets[x].write(colToExcel(row_index+2)+str(4+z+1),info_Mat[x][z][row_index],cell_format3)
                else:
                    all_worksheets[x].write(colToExcel(row_index+2)+str(4+z+1),info_Mat[x][z][row_index],cell_format4)
            for row_index in [9,11,12]:
                if (info_Mat[x][z][row_index] > 0 and info_Mat[x][z][row_index] > info_Mat[x][z][16] and info_Mat[x][z][12] > .5):
                    all_worksheets[x].write(colToExcel(row_index+2)+str(4+z+1),info_Mat[x][z][row_index],cell_format1)
                elif (info_Mat[x][z][row_index] > 0 and info_Mat[x][z][row_index] > info_Mat[x][z][16]):
                    all_worksheets[x].write(colToExcel(row_index+2)+str(4+z+1),info_Mat[x][z][row_index],cell_format2)
                elif (info_Mat[x][z][row_index] > 0):
                    all_worksheets[x].write(colToExcel(row_index+2)+str(4+z+1),info_Mat[x][z][row_index],cell_format3)
                else:
                    all_worksheets[x].write(colToExcel(row_index+2)+str(4+z+1),info_Mat[x][z][row_index],cell_format4)


            if (info_Mat[x][z][5] > 0 and info_Mat[x][z][5] > info_Mat[x][z][16] and info_Mat[x][z][7] > .5):
                all_worksheets[x].write_formula('G'+str(4+z+1),long_formula,cell_format1)
            elif (info_Mat[x][z][5] > 0 and info_Mat[x][z][5] > info_Mat[x][z][16]):
                all_worksheets[x].write_formula('G'+str(4+z+1),long_formula,cell_format2)
            elif (info_Mat[x][z][5] > 0):
                all_worksheets[x].write_formula('G'+str(4+z+1),long_formula,cell_format3)
            else:
                all_worksheets[x].write_formula('G'+str(4+z+1),long_formula,cell_format4)

            if (info_Mat[x][z][10] > 0 and info_Mat[x][z][10] > info_Mat[x][z][16] and info_Mat[x][z][12] > .5):
                all_worksheets[x].write_formula('L'+str(4+z+1),short_formula,cell_format1)
            elif (info_Mat[x][z][10] > 0 and info_Mat[x][z][10] > info_Mat[x][z][16]):
                all_worksheets[x].write_formula('L'+str(4+z+1),short_formula,cell_format2)
            elif (info_Mat[x][z][10] > 0):
                all_worksheets[x].write_formula('L'+str(4+z+1),short_formula,cell_format3)
            else:
                all_worksheets[x].write_formula('L'+str(4+z+1),short_formula,cell_format4)
                if short_formula == '#DIV/0!':
                    all_worksheets[x].write_formula('L'+str(4+z+1),0,cell_format4)


            all_worksheets[x].write('C'+str(4+z+1),info_Mat[x][z][1])
            if 'X'+info_Mat[x][z][1] in link_dict.keys() and x > 0:
                all_worksheets[x].write_url('B'+str(4+z+1), r'external:'+reference_book_name+'!'+link_dict['X'+info_Mat[x][z][1]])
            else:
                all_worksheets[x].write_url('B'+str(4+z+1), r'external:'+reference_book_name+'!'+link_dict[info_Mat[x][z][1]])
            all_worksheets[x].write('D'+str(4+z+1),info_Mat[x][z][2])
            all_worksheets[x].write('E'+str(4+z+1),info_Mat[x][z][3])
            all_worksheets[x].write('J'+str(4+z+1),long_zero_formula,zero_fmt)
            # all_worksheets[x].write('J'+str(4+z+1),info_Mat[x][z][8],zero_fmt)
            all_worksheets[x].write('O'+str(4+z+1),short_zero_formula,zero_fmt)
            # all_worksheets[x].write('O'+str(4+z+1),info_Mat[x][z][13],zero_fmt)
            all_worksheets[x].write('Q'+str(4+z+1),info_Mat[x][z][15])
            try:
                if info_Mat[x][z][14] < 0:
                    all_worksheets[x].write('P'+str(4+z+1),info_Mat[x][z][14],percent_fmt3)
                else:
                    all_worksheets[x].write('P'+str(4+z+1),info_Mat[x][z][14],percent_fmt2)
            except Exception as e:
                # print(e)
                all_worksheets[x].write('P'+str(4+z+1),' ')
            all_worksheets[x].write('R'+str(4+z+1),info_Mat[x][z][16],percent_fmt)
            # all_worksheets[x].write()
            if ('currencies' in info_Mat[x][z][1] or 'Currencies' in info_Mat[x][z][1]) and best_currency != 0:
                if info_Mat[x][z][7] >= best_currency:
                    all_worksheets[x].write('S'+str(4+z+1),'x')
                    best_currency == 2

        all_worksheets[x].freeze_panes(0, 3)


    workbook.close()


















#
