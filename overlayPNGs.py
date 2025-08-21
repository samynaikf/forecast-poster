
import os
import csv
import PIL
import glob
import numpy as np
from PIL import Image, ImageFile
from PIL import ImageFont
from PIL import ImageDraw
from hebrew_dictionary import translate
from get_index_name import get_index_name

def overlay(ROI,chart='im1.png',positive=True):
    foreground = Image.open(chart)
    background = Image.open('backgrounds/chart_background.png')
    draw = ImageDraw.Draw(foreground)
    try:
        font = ImageFont.truetype('Arial Bold.ttf',32)
    except:
        font = ImageFont.truetype(r"C:\Windows\Fonts\\arialbd.ttf",32)

    x_pos = 1530
    y_pos = 119
    if positive:
        y_pos = 515
        # background = Image.open('backgrounds/backgroundUp.png')
        draw.polygon([(x_pos,y_pos),(x_pos,y_pos+50),(x_pos+170,y_pos+50),(x_pos+170,y_pos)],fill='green')
        draw_centered_text(draw,(x_pos+90,y_pos+8),ROI,font=font,fill='#ffffff')
    else:
        # background = Image.open('backgrounds/backgroundDown.png')
        draw.polygon([(x_pos,y_pos),(x_pos,y_pos+50),(x_pos+170,y_pos+50),(x_pos+170,y_pos)],fill='red')
        draw_centered_text(draw,(x_pos+90,y_pos+8),ROI,font=font,fill='#ffffff')

    background.paste(foreground, (-100,0), foreground)
    background.save(chart)
    # background.show()

def overlay_hebrew_chart(chart='hebrew_demo.png'):
    foreground = Image.open(chart)
    background = Image.open('backgrounds/chart_background.png')
    draw = ImageDraw.Draw(foreground)
    try:
        font = ImageFont.truetype('Arial Bold.ttf',32)
    except:
        font = ImageFont.truetype(r"C:\Windows\Fonts\\arialbd.ttf",32)
    background.paste(foreground, (-170,-10), foreground)
    background.save('hebrew_charts/'+chart[:-4]+'.gif')
    background.show()


def draw_underlined_text(draw, pos, text, font, fill, color, center=False, right=False, adj=0, width=3, **options):
    twidth, theight = draw.textsize(text, font=font)

    lx, ly = pos[0], pos[1] + theight + 3
    if center:
        draw_centered_text(draw,pos,text,font,fill,color=color,lx=lx,ly=ly,adj=adj,underline=True,width=width)
    elif right:
        right_aligned_text(lx,ly,adj,draw,pos,text,font,fill)
    else:
        draw.text(pos, text, fill=color, font=font)
        draw.line((lx, ly+adj, lx + twidth, ly+adj), fill=color, width=width)


def draw_centered_text(draw,pos,text,font,fill,color='blue',width=3,underline=False,lx=0,ly=0,adj=0):
    twidth, theight = draw.textsize(text, font=font)
    new_x = pos[0] - .5*twidth
    draw.text((new_x,pos[1]), text, fill=fill, font=font)
    if underline:
        draw.line((new_x, ly+adj, new_x + twidth, ly+adj), fill=color, width=width)

def right_aligned_text(lx,ly,adj,draw,pos,text,font,fill,color='black'):
    twidth, theight = draw.textsize(text, font=font)
    new_x = pos[0] - twidth
    draw.text((new_x,pos[1]), text, fill=fill, font=font)
    draw.line((new_x, ly+adj, new_x + twidth, ly+adj), fill=color, width=1)


def overlay_heatmap(output_date,forecast_type,index_name,index_ROI,best_performers,horizon,name, dict, chart='im1.png',commodities=False,hebrew=False,sp_chart=False,sp_dir=True,has_sticky=False,top_20=False,short_forecast=False,gold_heatmap=False, bitcoin_chart=False): #edit: add dict input
    '''
    Take heatmap and overlay it on background
    '''
    # print("Putting heatmap on background")
    reverse_month_names_dict = {'Jan': 'January','Feb': 'February','Mar': 'March','Apr': 'April','May': 'May','Jun': 'June',
                    'Jul': 'July','Aug': 'August','Sep': 'September','Oct': 'October','Nov': 'November','Dec': 'December',
                    'January': 'January','February': 'February','March': 'March','April': 'April','May': 'May','June': 'June',
                    'July': 'July','August': 'August','September': 'September','October': 'October','November': 'November','December': 'December'}

    name_info = name.split(' ')
    # 'IKForecast_currencies_24_Mar_2019 3 days short until 27 March 2019'
    end_year = name_info[0][-2:]

    if forecast_type == 'currencies':
        start_date_info = name_info[0].split('_')
    else:
        start_date_info = name_info[0].split('_')
    if name_info[-3][-1] == '1' and (len(name_info[-3]) == 1 or name_info[-3][-2] == '0'):
        end_day = name_info[-3] + 'st'
    elif name_info[-3][-1] == '2' and (len(name_info[-3]) == 1 or name_info[-3][-2] == '0'):
        end_day = name_info[-3] + 'nd'
    elif name_info[-3][-1] == '3' and (len(name_info[-3]) == 1 or name_info[-3][-2] == '0'):
        end_day = name_info[-3] + 'rd'
    else:
        end_day = name_info[-3] + 'th'

    if start_date_info[-3][-1] == '1' and (len(start_date_info[-3]) == 1 or start_date_info[-3][-2] == '0'):
        start_day = start_date_info[-3] + 'st'
    elif start_date_info[-3][-1] == '2' and (len(start_date_info[-3]) == 1 or start_date_info[-3][-2] == '0'):
        start_day = start_date_info[-3] + 'nd'
    elif start_date_info[-3][-1] == '3' and (len(start_date_info[-3]) == 1 or start_date_info[-3][-2] == '0'):
        start_day = start_date_info[-3] + 'rd'
    else:
        start_day = start_date_info[-3] + 'th'

    if start_day[0] == '0':
        start_day = start_day[1:]
    if end_day[0] == '0':
        end_day = end_day[1:]

    try:
        del best_performers['']
    except:
        pass

    date_info = name_info[0].split('_')
    date = date_info[-3] + '_' + reverse_month_names_dict[date_info[-2]] + '_' + date_info[-1]
    hebrew_date = date_info[-1] + '_' + translate(reverse_month_names_dict[date_info[-2]][:3]) + '_' + date_info[-3]
    write_date = name_info[-3] + '_' + name_info[-2] + '_' + name_info[-1][:4]
    if date[0] == '0':
        date = date[1:]
    start_date = reverse_month_names_dict[start_date_info[-2]] + ' ' + start_day
    end_date = reverse_month_names_dict[name_info[-2]] + ' ' + end_day
    hebrew_start_date = translate(reverse_month_names_dict[start_date_info[-2]][:3])+' '+start_day
    hebrew_end_date = translate(reverse_month_names_dict[name_info[-2]][:3])+' '+end_day

    date_to_display = date = date_info[-3] + '_' + date_info[-2][:4] + '_' + date_info[-1]
    if date_to_display[0] == '0':
        date_to_display = date_to_display[1:]

    if hebrew:
        if horizon == 0:
            text_to_draw = translate('Days') +' 3               '+hebrew_date+' '+translate('Updated on')
        elif horizon == 1:
            text_to_draw = translate('Days') +' 7               '+hebrew_date+' '+translate('Updated on')
        elif horizon == 2:
            text_to_draw = translate('Days') +' 14              '+hebrew_date+' '+translate('Updated on')
        elif horizon == 3:
            text_to_draw = translate('Month') +' 1              '+hebrew_date+' '+translate('Updated on')
        elif horizon == 4:
            text_to_draw = translate('Month') +' 3              '+hebrew_date+' '+translate('Updated on')
        elif horizon == 5:
            text_to_draw = translate('Year') +' 1               '+hebrew_date+' '+translate('Updated on')
    else:
        if horizon == 0:
            text_to_draw = '3 Days          Updated on ' + date
        elif horizon == 1:
            text_to_draw = '7 Days          Updated on ' + date
        elif horizon == 2:
            text_to_draw = '14 Days         Updated on ' + date
        elif horizon == 3:
            text_to_draw = '1 Month         Updated on ' + date
        elif horizon == 4:
            text_to_draw = '3 Months        Updated on ' + date
        elif horizon == 5:
            text_to_draw = '1 Year          Updated on ' + date

    #bitcoin_chart = False
    foreground = Image.open(chart)

    width, height = foreground.size
    foreground = foreground.resize((width*2,height*2), Image.ANTIALIAS)

    if gold_heatmap: #gold pictures here are amended by GlebZ
        #pdb.set_trace()
        if len(list(best_performers.keys())) > 4:
            background = Image.open('backgrounds/gld_xau_background_4.png')
        elif len(list(best_performers.keys())) > 3:
            background = Image.open('backgrounds/gld_xau_background_3.png')
        elif len(list(best_performers.keys())) > 2:
            background = Image.open('backgrounds/gld_xau_background_2.png')
        else:
            background = Image.open('backgrounds/gld_xau_background.png')
        basewidth = 1955
        wpercent = (basewidth/float(background.size[0]))
        hsize = int((float(background.size[1])*float(wpercent)))
        background = background.resize((basewidth,hsize), Image.ANTIALIAS)
        background.paste(foreground, (15,222), foreground)

    elif top_20 and not hebrew:
        background = Image.open('backgrounds/english_20.png')
        basewidth = 1955
        wpercent = (basewidth/float(background.size[0]))
        hsize = int((float(background.size[1])*float(wpercent)))
        background = background.resize((basewidth,hsize), Image.ANTIALIAS)

        background.paste(foreground, (8,220), foreground)
    elif bitcoin_chart:#len(list(best_performers.keys())) == 2 and ('BTC' in list(best_performers.keys())[0] or 'BTC' in list(best_performers.keys())[1]):
        print("Bitcoin Chart")
        #bitcoin_chart = True
        if hebrew:
            background = Image.open('backgrounds/hebrew_background.png')
            background.paste(foreground, (1050,222), foreground)
            #basewidth = 1955
            #wpercent = (basewidth/float(background.size[0]))
            #hsize = int((float(background.size[1])*float(wpercent)))
            #background = background.resize((basewidth,hsize), Image.ANTIALIAS)

            #w, h = foreground.size
            #foreground = foreground.crop((0,0,w,360))

            #background.paste(foreground, (1055,250), foreground)
        else:
            background = Image.open('backgrounds/commodities_background.png')
            background.paste(foreground, (15,222), foreground)
            #basewidth = 1955
            #wpercent = (basewidth/float(background.size[0]))
            #hsize = int((float(background.size[1])*float(wpercent)))
            #background = background.resize((basewidth,hsize), Image.ANTIALIAS)

            #w, h = foreground.size
            #foreground = foreground.crop((0,0,w,360))

            #background.paste(foreground, (6,218), foreground)
    elif forecast_type == 'currencies':
        if hebrew:
            background = Image.open('backgrounds/currency_hebrew.png')

            basewidth = 930
            wpercent = (basewidth/float(background.size[0]))
            hsize = int((float(background.size[1])*float(wpercent)))
            background = background.resize((basewidth,hsize), Image.ANTIALIAS)

            background.paste(foreground, (515,105), foreground)
        else:
            background = Image.open('backgrounds/currency_background.png')
            background.paste(foreground, (8,100), foreground)
    elif hebrew:
        if top_20:
            background = Image.open('backgrounds/hebrew_20.png')
            basewidth = 2000
            wpercent = (basewidth/float(background.size[0]))
            hsize = int((float(background.size[1])*float(wpercent)))
            background = background.resize((basewidth,hsize), Image.ANTIALIAS)
            background.paste(foreground, (1105,222), foreground)
        else:
            background = Image.open('backgrounds/hebrew_background.png')
            background.paste(foreground, (1050,222), foreground)
    elif commodities:
        background = Image.open('backgrounds/commodities_background.png')
        background.paste(foreground, (15,222), foreground)
    else:
        background = Image.open('backgrounds/new_background.png')
        background.paste(foreground, (6,218), foreground)
    draw = ImageDraw.Draw(background)


    # Initiliaze fonts
    try:
        # For Mac
        font = ImageFont.truetype('Arial Bold.ttf',42)
        font2 = ImageFont.truetype('Arial Bold.ttf',32)
        font3 = ImageFont.truetype('Arial Bold Italic.ttf',42)
        font4 = ImageFont.truetype('Arial Bold.ttf',55)
        font5 = ImageFont.truetype('Arial Bold.ttf',24)
        font6 = ImageFont.truetype('Arial Bold.ttf',18)
        font7 = ImageFont.truetype('Arial Bold.ttf',16)
        font8 = ImageFont.truetype('Arial Bold.ttf',12)
        font9 = ImageFont.truetype('Arial Bold Italic.ttf',22)
    except:
        # For Windows
        font = ImageFont.truetype(r"C:\Windows\Fonts\\arialbd.ttf",42)
        font2 = ImageFont.truetype(r"C:\Windows\Fonts\\arialbd.ttf",32)
        font3 = ImageFont.truetype(r"C:\Windows\Fonts\\arialbi.ttf",42)
        font4 = ImageFont.truetype(r"C:\Windows\Fonts\\arialbd.ttf",55)
        font5 = ImageFont.truetype(r"C:\Windows\Fonts\\arialbd.ttf",24)
        font6 = ImageFont.truetype(r"C:\Windows\Fonts\\arialbd.ttf",18)
        font7 = ImageFont.truetype(r"C:\Windows\Fonts\\arialbd.ttf",16)
        font8 = ImageFont.truetype(r"C:\Windows\Fonts\\arialbd.ttf",12)
        font9 = ImageFont.truetype(r"C:\Windows\Fonts\\arialbi.ttf",22)

    if forecast_type == 'currencies':
        if hebrew:
            draw.text((540,75),text_to_draw,fill='#000000',font=font6)
        else:
            draw.text((25,68),text_to_draw,fill='#000000',font=font6)
    elif hebrew:
        if top_20:
            draw.text((1220,155),text_to_draw,fill='#000000',font=font)
        else:
            draw.text((1110,155),text_to_draw,fill='#000000',font=font)
    elif commodities or bitcoin_chart:
        if gold_heatmap:
            draw.text((45,140),text_to_draw,fill='#000000',font=font)
        else:
            draw.text((45,155),text_to_draw,fill='#000000',font=font)
    else:
        if top_20:
            push = 20
        else:
            push = 0
        draw.text((45,135+push),text_to_draw,fill='#000000',font=font)

    index = 0
    x_pos = 1140
    y_pos = 265

    if forecast_type == 'currencies':
        x_pos = 520
        y_pos = 109
    elif hebrew:
        if top_20:
            x_pos = 830
            y_pos = 293
        else:
            x_pos = 780
            y_pos = 298
    elif commodities or bitcoin_chart: #new version for bitcoin
        x_pos = 1120
        y_pos = 290
    all_vals = []
    correct_pred = []
    vertices = []
    last_box_win = False
    green_counter = 0


    # Draw Asset names and Rates of Return on Accuracy Chart
    for key, value in best_performers.items():
        if key == '' or key == '^S&P500':
            continue
        if forecast_type == 'currencies':
            if value[1] == 'xkcd:bright lime green' or value[1] == 'xkcd:lightgreen' or value[1] == 'bright lime green' or value[1] == 'lightgreen':
                green_counter += 1
                all_vals.append(value[0])
                if value[0] >= 0:
                    if not last_box_win:
                        last_box_win = True
                        vertices.append(index)
                    correct_pred.append(1)
                else:
                    if last_box_win:
                        last_box_win = False
                        vertices.append(index)
                    correct_pred.append(0)

            else:
                all_vals.append(-value[0])
                if value[0] <= 0:
                    if not last_box_win:
                        last_box_win = True
                        vertices.append(index)
                    correct_pred.append(1)
                else:
                    if last_box_win:
                        last_box_win = False
                        vertices.append(index)
                    correct_pred.append(0)
            value = "%.2f" % value[0] + '%'
            value_width, value_height = draw.textsize(value, font=font)
            value_adj = 1.5*value_width


        elif forecast_type == 'long' or (forecast_type == 'long+short' and index < 5):
            all_vals.append(value)
            if value > 0:
                if not last_box_win:
                    last_box_win = True
                    vertices.append(index)
                correct_pred.append(1)
            else:
                if last_box_win:
                    last_box_win = False
                    vertices.append(index)
                correct_pred.append(0)
            value = "%.2f" % value + '%'
            value_width, value_height = draw.textsize(value, font=font)
            value_adj = .9*value_width
        elif forecast_type == 'short' or (forecast_type == 'long+short' and index > 4):
            all_vals.append(-value)
            if value < 0:
                if not last_box_win:
                    last_box_win = True
                    vertices.append(index)
                correct_pred.append(1)
            else:
                if last_box_win:
                    last_box_win = False
                    vertices.append(index)
                correct_pred.append(0)

            value = "%.2f" % value + '%'
            value_width, value_height = draw.textsize(value, font=font)
            value_adj = .9*value_width

        if forecast_type == 'currencies':
            if hebrew:
                draw_centered_text(draw,(x_pos-135,y_pos+12),str(key),font=font7,fill='#000000')
                y_pos += 30.7
            else:
                draw_centered_text(draw,(x_pos+15,y_pos),str(key),font=font7,fill='#000000')
                draw_underlined_text(draw,(x_pos+278,y_pos),value,font7,fill=0,color='#000000',right=True)
                y_pos += 30.08

        elif hebrew:
            draw_centered_text(draw,(x_pos,y_pos),str(key),font=font3,fill='#000000')
            if top_20:
                y_pos += 89
            else:
                y_pos += 92
        elif commodities or bitcoin_chart:
            if gold_heatmap:
                draw_centered_text(draw,(x_pos+35,y_pos-80),str(key),font=font3,fill='#000000')
                draw_underlined_text(draw,(x_pos+600-value_adj,y_pos-80),value,font,fill=0,color='#000000')
                y_pos += 81
            else:
                draw_centered_text(draw,(x_pos+20,y_pos),str(key),font=font3,fill='#000000')
                draw_underlined_text(draw,(x_pos+600-value_adj,y_pos),value,font,fill=0,color='#000000')
                y_pos += 92
        #elif bitcoin_chart:
         #   draw_centered_text(draw,(x_pos+20,y_pos-5),str(key),font=font3,fill='#000000')
          #  draw_underlined_text(draw,(x_pos+600-value_adj,y_pos-5),value,font,fill=0,color='#000000')
           # y_pos += 87
        else:
            draw_centered_text(draw,(x_pos+15,y_pos),str(key),font=font3,fill='#000000')
            draw_underlined_text(draw,(x_pos+590-value_adj,y_pos),value,font,fill=0,color='#000000')
            if top_20:
                y_pos += 87
            else:
                y_pos += 89
        index += 1

    csv_index_ROI = index_ROI
    index_name_csv = index_name #edit

    if not (forecast_type == 'currencies' or commodities or hebrew or bitcoin_chart):
        # if index_name[0] == '^':
        #     index_name = index_name[1:]
        index_name = get_index_name(index_name)
        index_name_width, index_name_height = draw.textsize(index_name, font=font)
        index_name_adj = .3*index_name_width
        # draw.text((x_pos-18-index_name_adj,y_pos+140),index_name,fill='#000000', font=font3)
        draw_underlined_text(draw,(x_pos-18-index_name_adj,y_pos+145),index_name,font3,fill=0,color='#000000')


        index_ROI = "%.2f" % index_ROI + '%'
        index_ROI_width, index_ROI_height = draw.textsize(index_ROI, font=font)
        index_ROI_adj = .9*index_ROI_width
        draw_underlined_text(draw,(x_pos+590-index_ROI_adj,y_pos+145),index_ROI,font,fill=0,color='#000000')

    if (len(vertices) % 2) != 0:
        vertices.append(index)

    avgROI = round(sum(all_vals)/len(all_vals),2)
    csv_avgROI = avgROI
    if not hebrew:
        hit_ratio_num = (round(100*sum(correct_pred)/len(correct_pred),2))
        y_pos += 25
        avgROI = "%.2f" % avgROI + '%'
        avgROI_width, avgROI_height = draw.textsize(avgROI, font=font)
        avgROI_adj = .9*avgROI_width
        if commodities or bitcoin_chart:
            if gold_heatmap:
                # draw_underlined_text(draw,(x_pos+600-avgROI_adj,y_pos-65),avgROI,font,fill=0,color='#000000')
                draw_underlined_text(draw,(1720-avgROI_adj,680),avgROI,font,fill=0,color='#000000')
            else:
                draw_underlined_text(draw,(x_pos+600-avgROI_adj,y_pos),avgROI,font,fill=0,color='#000000')
        else:
            draw_underlined_text(draw,(x_pos+590-avgROI_adj,y_pos),avgROI,font,fill=0,color='#000000')
    else:
        if hebrew:
            hit_ratio = "%.0f" % (round(100*sum(correct_pred)/len(correct_pred),2)) + '%'
            hit_ratio_num = (round(100*sum(correct_pred)/len(correct_pred),2))
            if top_20:
                draw_underlined_text(draw,(160,2065),hit_ratio,font4,fill=0,color='#000000')
            elif forecast_type == 'currencies':
                # draw_underlined_text(draw,(600,1200),hit_ratio,font4,fill=0,color='#000000')
                pass
            #elif bitcoin_chart:
             #   draw_underlined_text(draw,(125,495),hit_ratio,font4,fill=0,color='#000000')
            else:
                draw_underlined_text(draw,(130,1225),hit_ratio,font4,fill=0,color='#000000')
        else:
            hit_ratio = "%.0f" % (round(100*sum(correct_pred)/len(correct_pred),2)) + '%'
            hit_ratio_num = (round(100*sum(correct_pred)/len(correct_pred),2))

            draw_underlined_text(draw,(1610,445),hit_ratio,font4,fill=0,color='#000000')

    x_pos = 1050
    y_pos = 190
    x_shift1 = 40
    x_shift2 = 35
    x_shift3 = 32
    x_shift4 = 115
    y_shift = 50
    x_inc1 = 230
    x_inc2 = 190
    x_inc3 = 240
    title_font = font2
    adj = 3
    width = 3
    titles = ['Symbol','Forecast',start_date,'% Change',end_date,'Accuracy']
    if top_20:
        push = 15
    else:
        push = 0
    if forecast_type == 'currencies':
        x_pos = 500
        y_pos = 83
        x_shift1 = 0
        x_shift2 = -2
        x_shift3 = 10
        x_shift4 = 26
        y_shift = 16
        x_inc1 = 122
        x_inc2 = 85
        x_inc3 = 105
        title_font = font8
        adj = -1
        width = 1
        if hebrew:
            x_pos -= 440
            y_pos += 7
            x_shift1 = 50
            x_shift2 = 0
            x_shift3 = 15
            x_shift4 = 65
            titles = [translate('Accuracy'),translate('Forecast'),hebrew_start_date[:-2],translate('Symbol'),' ',' ']
    elif hebrew:
        if top_20:
            x_pos = 770
        else:
            x_pos = 730
        y_pos = 205
        x_shift1 = -210
        x_shift2 = -195
        x_shift3 = 0
        x_shift4 = -165
        y_shift = 50
        x_inc1 = -85
        x_inc2 = -190
        x_inc3 = -300
        title_font = font2
        adj = 3
        width = 3
        titles = [translate('Symbol'),translate('Forecast'),hebrew_start_date[:-2],translate('Accuracy'),hebrew_end_date[:-2],' ']
    elif commodities or bitcoin_chart:
        x_pos = 1050
        y_pos = 210
        x_shift1 = 40
        x_shift2 = 35
        x_shift3 = 32
        x_shift4 = 115
        y_shift = 50
        x_inc1 = 220
        x_inc2 = 190
        x_inc3 = 240
        title_font = font2
        adj = 3
        width = 3
        if gold_heatmap:
            x_pos += 20
            y_pos -= 40
    #elif bitcoin_chart:
     #   y_pos = 170
    for x in range(len(titles)):
        if x == 1:
            draw_underlined_text(draw,(x_pos+x_shift1,y_pos-y_shift+push),titles[x],font=title_font,fill=0,color='#ffffff',adj=adj, width=width)
        elif x == 3:
            if forecast_type == 'currencies' and hebrew:
                draw.text((370,90),titles[x],font=title_font,fill='#ffffff',color='#ffffff',adj=adj,width=width)
            else:
                draw_underlined_text(draw,(x_pos+x_shift2,y_pos-y_shift+push),titles[x],font=title_font,fill=0,color='#ffffff', adj=adj,width=width)
        elif x == 0:
            draw.text((x_pos+x_shift3,y_pos+push),titles[x],fill='#ffffff',font=title_font)
            x_pos += x_inc1
        else:
            draw_centered_text(draw,(x_pos+x_shift4,y_pos+push),titles[x],font=title_font,fill='#ffffff')
            if x == 4:
                x_pos += x_inc2
            else:
                x_pos += x_inc3

    if sp_chart and not top_20:
        if sp_dir == True:
            sp_img = Image.open('backgrounds/up_arrow.png')
            basewidth = 45
        else:
            sp_img = Image.open('backgrounds/down_arrow.png')
            basewidth = 40
    if forecast_type == 'long':
        img = Image.open('backgrounds/up_arrow.png')
        basewidth = 45
    elif forecast_type == 'short':
        img = Image.open('backgrounds/down_arrow.png')
        basewidth = 40
    elif forecast_type == 'long+short':
        img1 = Image.open('backgrounds/up_arrow.png')
        basewidth = 45
        wpercent = (basewidth/float(img1.size[0]))
        hsize = int((float(img1.size[1])*float(wpercent)))
        img1 = img1.resize((basewidth,hsize), Image.ANTIALIAS)

        img2 = Image.open('backgrounds/down_arrow.png')
        basewidth = 40
        wpercent = (basewidth/float(img2.size[0]))
        hsize = int((float(img2.size[1])*float(wpercent)))
        img2 = img2.resize((basewidth,hsize), Image.ANTIALIAS)

    elif forecast_type == 'currencies':
        img1 = Image.open('backgrounds/up_arrow.png')
        basewidth = 16
        wpercent = (basewidth/float(img1.size[0]))
        hsize = int((float(img1.size[1])*float(wpercent)))
        img1 = img1.resize((basewidth,hsize), Image.ANTIALIAS)

        img2 = Image.open('backgrounds/down_arrow.png')
        basewidth = 14
        wpercent = (basewidth/float(img2.size[0]))
        hsize = int((float(img2.size[1])*float(wpercent)))
        img2 = img2.resize((basewidth,hsize), Image.ANTIALIAS)



    x_pos = 1370
    y_pos = 245
    if hebrew:
        if top_20:
            x_pos = 520
        else:
            x_pos = 470
        y_pos = 285
    if forecast_type == 'currencies':
        x_pos = 640
        y_pos = 104
        y_increase = 30.08
        if hebrew:
            x_pos = 240
            y_pos = 115
            y_increase = 30.7
        for x in range(green_counter):
            background.paste(img1, (x_pos,round(y_pos)), img1)
            y_pos += y_increase

        for x in range(len(list(best_performers.keys()))-green_counter):
            background.paste(img2, (x_pos+1,round(y_pos-1)), img2)
            y_pos += y_increase

    #elif bitcoin_chart == True:
     #   x_pos += 15
      #  y_pos -= 12
       # if hebrew:
        #    x_pos -= 25
        #wpercent = (basewidth/float(img.size[0]))
        #hsize = int((float(img.size[1])*float(wpercent)))
        #img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        #for x in range(2):
         #   background.paste(img, (x_pos+1,round(y_pos-1)), img)
          #  y_pos += 87
    elif forecast_type == 'long+short':
        if top_20:
            y_pos = 250
            for x in range(10):
                background.paste(img1, (x_pos,y_pos), img1)
                y_pos += 87

            for x in range(10):
                background.paste(img2, (x_pos+4,y_pos), img2)
                y_pos += 87
        else:
            for x in range(5):
                background.paste(img1, (x_pos,y_pos), img1)
                y_pos += 89

            for x in range(5):
                background.paste(img2, (x_pos+4,y_pos), img2)
                y_pos += 89
    else:
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        x_push = 0
        if top_20:
            num = 20
            push = 10
        elif gold_heatmap:
            num = len(list(best_performers.keys()))
            x_push = 15
        else:
            num = 10
            push = 0
        for x in range(num):
            if hebrew:
                background.paste(img, (x_pos-15,int(y_pos)-7), img)
                if top_20:
                    y_pos += 88.25
                else:
                    y_pos += 92
            elif commodities or bitcoin_chart:
                if gold_heatmap:
                    background.paste(img, (x_pos+x_push+5,y_pos-15), img)
                    y_pos += 81
                else:
                    background.paste(img, (x_pos+x_push,y_pos+30), img)
                    y_pos += 92

            else:
                background.paste(img, (x_pos+x_push,y_pos+push), img)
                if top_20:
                    y_pos += 87
                else:
                    y_pos += 89


    if sp_chart and not top_20:
        wpercent = (basewidth/float(sp_img.size[0]))
        hsize = int((float(sp_img.size[1])*float(wpercent)))
        sp_img = sp_img.resize((basewidth,hsize), Image.ANTIALIAS)
        background.paste(sp_img,(1370,1280),sp_img)




    check = Image.open('backgrounds/check.png')
    cross = Image.open('backgrounds/cross.png')
    if forecast_type == 'currencies':
        basewidth = 32
    else:
        basewidth = 80
    wpercent = (basewidth/float(check.size[0]))
    hsize = int((float(check.size[1])*float(wpercent)))
    check = check.resize((basewidth,hsize), Image.ANTIALIAS)

    if forecast_type == 'currencies':
        basewidth = 22
    else:
        basewidth = 52

    wpercent = (basewidth/float(cross.size[0]))
    hsize = int((float(cross.size[1])*float(wpercent)))
    cross = cross.resize((basewidth,hsize), Image.ANTIALIAS)

    if sp_chart and not top_20:
        if (sp_dir and csv_index_ROI > 0) or \
        (not sp_dir and csv_index_ROI < 0):
            background.paste(check, (1790,1280), check)
        else:
            background.paste(cross, (1802,1295), cross)

    x_pos = 1790
    y_pos = 250
    inc = 89
    y_shift = 18
    x_shift = 12
    if top_20 and not hebrew:
        inc = 87

    elif forecast_type == 'currencies':
        x_pos = 825
        y_pos = 102
        inc = 30.1
        y_shift = 7
        x_shift = 5
        if hebrew:
            x_pos = 83
            y_pos = 112
            inc = 30.7
    elif hebrew:
        if top_20:
            inc = 88.25
            x_pos = 155
        else:
            inc = 92
            x_pos = 145
        y_pos = 280
        y_shift = 18
        x_shift = 12
    elif commodities or bitcoin_chart:
        x_pos = 1790
        y_pos = 270
        inc = 92
        y_shift = 18
        x_shift = 12
        if gold_heatmap:
            inc = 81
            x_pos += 20
            y_pos -= 35
    #elif bitcoin_chart:
     #   x_pos += 20
      #  y_pos -= 5
       # inc = 87
    for x in range(len(correct_pred)):
        if correct_pred[x] == 1:
            background.paste(check, (x_pos,int(y_pos)), check)
        else:
            background.paste(cross, (x_pos+x_shift,int(y_pos)+y_shift), cross)

        y_pos += inc

    #Draw blue triangle on middle of heatmap
    if hebrew and not forecast_type == 'currencies':
        if forecast_type == 'long':
            if top_20:
                draw.polygon([(1000,575),(1080,425),(1080,725)],fill='blue')
            elif bitcoin_chart:
                draw.polygon([(1000,515),(1080,365),(1080,665)],fill='blue')
            else:
                draw.polygon([(950,400),(1030,250),(1030,550)],fill='blue')
        elif forecast_type == 'short':
            if top_20:
                draw.polygon([(1000,1090),(1080,940),(1080,1240)],fill='blue')
            elif bitcoin_chart:
                draw.polygon([(950,575),(1030,425),(1030,725)],fill='blue')
            else:
                draw.polygon([(950,1250),(1030,1100),(1030,1400)],fill='blue')
    elif forecast_type == 'long':
        if top_20:
            draw.polygon([(915,430),(915,715),(1000,572.5)],fill='blue')
        elif bitcoin_chart:
            draw.polygon([(915,250),(915,535),(1000,392.5)],fill='blue')
        else:
            draw.polygon([(915,250),(915,535),(1000,392.5)],fill='blue')
    elif forecast_type == 'short':
        if top_20:
            draw.polygon([(915,1090),(915,1375),(1000,1232.5)],fill='blue')
        elif bitcoin_chart:
            draw.polygon([(915,425),(915,715),(1000,567.5)],fill='blue')
        elif short_forecast:
            draw.polygon([(915,600),(915,885),(1000,742.5)],fill='blue')
        else:
            draw.polygon([(915,1090),(915,1375),(1000,1232.5)],fill='blue')
    elif forecast_type == 'long+short':
        draw.polygon([(915,670),(915,955),(1000,812.5)],fill='blue')
    elif forecast_type == 'currencies':
        if hebrew:
            draw.polygon([(505,350),(505,500),(470,425)],fill='blue')
        else:
            draw.polygon([(430,357.5),(430,502.5),(465,430)],fill='blue')
    vertices_points = []
    for x in range(1,len(vertices),2):
        vertices_points.append((vertices[x-1],vertices[x]))

    x_pos = 1028
    y_pos = 240
    step_down = 89
    x_adj = 888
    width = 8
    push = 0
    if top_20 and not hebrew:
        push = 10
        x_pos = 1024
        y_pos = 250
        step_down = 87
        x_adj = 896
        width = 8
    elif forecast_type == 'currencies':
        x_pos = 480
        y_pos = 100
        step_down = 30.15
        x_adj = 397
        width = 3
        if hebrew:
            step_down = 30.7
            x_pos = 20
            y_pos = 115
            x_adj = 430
    elif hebrew:
        if top_20:
            push = 10
            step_down = 89
            x_pos = 35
            x_adj = 942
        else:
            step_down = 92
            x_pos = 19
            x_adj = 892
        y_pos = 265
    elif commodities or bitcoin_chart:
        print('check')
        x_pos = 1014
        y_pos = 260
        step_down = 92
        x_adj = 895
    #elif bitcoin_chart:
     #   x_pos += 8
      #  y_pos -= 12
       # x_adj += 10
        #step_down = 87
        #if hebrew:
         #   step_down = 92
          #  x_pos = 19
           # x_adj = 900
            #y_pos = 265
    for x in range(len(vertices_points)):
        draw.line((x_pos, y_pos + step_down*vertices_points[x][0], x_pos + x_adj, y_pos + step_down*vertices_points[x][0]), fill='blue', width=width)
        draw.line((x_pos, y_pos + step_down*vertices_points[x][0], x_pos, y_pos + step_down*vertices_points[x][1]), fill='blue', width=width)
        draw.line((x_pos, y_pos + step_down*vertices_points[x][1], x_pos + x_adj, y_pos + step_down*vertices_points[x][1]), fill='blue', width=width)
        draw.line((x_pos + x_adj, y_pos + step_down*vertices_points[x][0], x_pos + x_adj, y_pos + step_down*vertices_points[x][1]), fill='blue', width=width)



    if hebrew and not forecast_type == 'currencies':
        draw.text((200,40),translate("Forecast Performance (" + forecast_type + ")"),fill='#000000',font=font4)
        draw.text((1275,40),translate("Algorithmic Stock Forecast"),fill='#000000',font=font4)
    elif forecast_type == 'long+short':
        draw.text((1010,40),"Forecast Performance (" + forecast_type + ")",fill='#000000',font=font4)
        draw.text((90,40),"Algorithmic Stock Forecast",fill='#000000',font=font4)
    elif forecast_type == 'currencies':
        if hebrew:
            draw.text((35,20),translate("Forecast Performance (" + forecast_type + ")"),fill='#000000',font=font3)
            draw.text((560,20),translate("Algorithmic Stock Forecast"),fill='#000000',font=font3)
        else:
            draw.text((560,20),"Forecast Performance",fill='#000000',font=font5)
            draw.text((35,20),"Algorithmic Currency Forecast",fill='#000000',font=font5)

        hit_ratio = "%.2f" % (round(100*sum(correct_pred)/len(correct_pred),2)) + '%'
        '''
        Draw Hit ratio box with x = 35, y = 1100,
        height = 100, length = 350
        '''
        if hebrew:
            # draw.line((32,1102,32,1198), fill='black', width=width)
            # draw.line((32,1198,400,1198), fill='black', width=width)
            # draw.line((400,1198,400,1102), fill='black', width=width)
            # draw.line((400,1102,32,1102), fill='black', width=width)

            x_shift = 500
            y_shift = 60

            draw.rectangle([550,1150,900,1270],fill=None,outline='blue',width=3)

            # draw_underlined_text(draw,(105+x_shift,1110+y_shift),"I Know",font9,fill=0,color='#000000',center=True)
            # draw_underlined_text(draw,(105+x_shift,1135+y_shift),"First",font9,fill=0,color='#000000',center=True)
            draw_underlined_text(draw,(125+x_shift,1135+y_shift),translate("Hit Ratio"),font9,fill=0,color='#000000',center=True)
            draw_underlined_text(draw,(335+x_shift,1130+y_shift),hit_ratio,font2,fill=0,color='#000000',center=True)


            green_arrow = Image.open('backgrounds/green_arrow.png')
            basewidth = 70
            wpercent = (basewidth/float(green_arrow.size[0]))
            hsize = int((float(green_arrow.size[1])*float(wpercent)))
            green_arrow = green_arrow.resize((basewidth,hsize), Image.ANTIALIAS)

            background.paste(green_arrow,(195+x_shift,1115+y_shift),green_arrow)
        else:
            draw.line((32,1102,32,1198), fill='black', width=width)
            draw.line((32,1198,400,1198), fill='black', width=width)
            draw.line((400,1198,400,1102), fill='black', width=width)
            draw.line((400,1102,32,1102), fill='black', width=width)

            draw.line((28,1098,28,1202), fill='blue', width=width)
            draw.line((28,1202,404,1202), fill='blue', width=width)
            draw.line((404,1202,404,1098), fill='blue', width=width)
            draw.line((404,1098,28,1098), fill='blue', width=width)

            draw_underlined_text(draw,(105,1110),"I Know",font9,fill=0,color='#000000',center=True)
            draw_underlined_text(draw,(105,1135),"First",font9,fill=0,color='#000000',center=True)
            draw_underlined_text(draw,(105,1160),"Hit Ratio",font9,fill=0,color='#000000',center=True)
            draw_underlined_text(draw,(335,1130),hit_ratio,font2,fill=0,color='#000000',center=True)


            green_arrow = Image.open('backgrounds/green_arrow.png')
            basewidth = 100
            wpercent = (basewidth/float(green_arrow.size[0]))
            hsize = int((float(green_arrow.size[1])*float(wpercent)))
            green_arrow = green_arrow.resize((basewidth,hsize), Image.ANTIALIAS)

            background.paste(green_arrow,(165,1100),green_arrow)



    else:
        draw.text((1100,40+push),"Forecast Performance (" + forecast_type + ")",fill='#000000',font=font4)

        if 'currencies' in name or 'Currencies' in name:
            draw.text((30,40+push),"Algorithmic Currency Forecast",fill='#000000',font=font4)
        elif 'commodities' in name or 'Commodities' in name:
            draw.text((30,40+push),"Algorithmic Commodity Forecast",fill='#000000',font=font4)
        elif 'ETF' in name:
            draw.text((150,40+push),"Algorithmic ETF Forecast",fill='#000000',font=font4)
        elif ('index' in name or 'Index' in name) and not ('Bovespa' in name or 'bovespa' in name):
            draw.text((120,40+push),"Algorithmic Index Forecast",fill='#000000',font=font4)
        elif bitcoin_chart:
            draw.text((70,40+push),"Algorithmic Bitcoin Forecast",fill='#000000',font=font4)
        else:
            draw.text((90,40+push),"Algorithmic Stock Forecast",fill='#000000',font=font4)


    if True:
        predictor = 1
    elif forecast_type == 'short':
        predictor = -1



    calendar_dates = {'January': '1','February': '2','March': '3','April': '4','May': '5','June': '6',
                    'July': '7','August': '8','September': '9','October': '10','November': '11','December': '12',
                    'Jan': '1','Feb': '2','Mar': '3','Apr': '4','May': '5','Jun': '6',
                    'Jul': '7','Aug': '8','Sep': '9','Oct': '10','Nov': '11','Dec': '12'}

    # Make output folder for csv files and save as file name
    name = name.split('/')[-1]
    if name[-4:] == '.xls':
        name = name[:-4]
    #if hebrew:
     #   output_file = name + '_hebrew.csv'
    #else:
        if has_sticky:
            output_file = name + '_sticky.csv'
        else:
            output_file = name + '.csv'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #if hebrew:
     #   new_dir = os.path.join(script_dir,output_date+'/HEBREW_CSVs_' + write_date)
    #else:
    new_dir = os.path.join(script_dir,output_date+'/CSVs_' + write_date)
    try:
        os.makedirs(new_dir)
    except OSError:
        pass
    path = os.path.join(new_dir,output_file)

    start_date_csv_info = start_date.split(' ')
    end_date_csv_info = end_date.split(' ')
    write_date_start = calendar_dates[start_date_csv_info[0]] + '/' + start_date_csv_info[1][:-2] + '/' + end_year
    print(name_info)
    if has_sticky:
        write_date_end = calendar_dates[end_date_csv_info[0]] + '/' + end_date_csv_info[1][:-2] + '/' + name_info[-1][-6:-4]#'/20'
    else:
        write_date_end = calendar_dates[end_date_csv_info[0]] + '/' + end_date_csv_info[1][:-2] + '/' + name_info[-1][-6:-4]#'/20'

    # Make output csv file
    with open(path.replace(' ','-'), 'w',newline='') as csvFile:
        writer = csv.writer(csvFile,delimiter=',',quotechar =',',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Update Date',write_date_start])
        writer.writerow(['Target Date',write_date_end])
        writer.writerow(['Symbol','Predictor','Return (%)','Accuracy', 'Signal', 'Predictability'])
        counter = 0
        for key, value in best_performers.items():
            if key == '':
                continue
            # if hebrew:
            #   writer.writerow([key,predictor,round(hit_ratio_num,2),correct_pred[counter]])
            if forecast_type == 'currencies':
                if 'green' in value[1]:
                    writer.writerow([key, 1, round(all_vals[counter], 2), correct_pred[counter]])
                else:
                    writer.writerow([key, -1, round(all_vals[counter], 2), correct_pred[counter]])
            else:
                for ticker, num in dict.items(): #edit
                    if ticker == key: # edit
                        writer.writerow([key,predictor,round(all_vals[counter],2),correct_pred[counter], num[0], num[1]]) #edit
            counter += 1



        if forecast_type == 'currencies':
            writer.writerow(['IKNOWFIRST_AVG',' ',hit_ratio_num])
        else:
            writer.writerow(['IKNOWFIRST_AVG',' ',csv_avgROI])
            writer.writerow(['S&P500',' ',csv_index_ROI]) # EDIT writer.writerow([index_name_csv,' ',csv_index_ROI])
    csvFile.close()


    #Make output folder for pics and save as file name
    output_pics = name + '.jpg'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if hebrew:
        new_dir = os.path.join(script_dir,output_date+'/HEBREW_JPGs_' + write_date)
    else:
        new_dir = os.path.join(script_dir,output_date+'/JPGs_' + write_date)

    try:
        os.makedirs(new_dir)
    except OSError:
        pass
    path = os.path.join(new_dir,output_pics)


    # background.save(path)



    '''
    ###########################
    '''

    IMAGE_WIDTH = 2545 # Pizel Height for heatmap images

    '''
    ###########################
    '''



    width, height = background.size
    # background = background.resize((IMAGE_WIDTH,int(height*IMAGE_WIDTH/width)))
    if forecast_type == 'currencies': #ADDED BY GLEB ON 11/16/20 FOR CURRENCIES RENDERING
        mywidth=890
        heb_width=592
    else:
        mywidth = 612
        heb_width = 592
    ###ADDED BY GLEB ZINKOVSKII FOR IMAGE OPTIMIZATION ON JUNE 15 2020###
    if hebrew:
        wpercent = (heb_width / float(background.size[0]))
        hsize = int((float(background.size[1]) * float(wpercent)))
        background = background.resize((heb_width, hsize), PIL.Image.ANTIALIAS)
    else:
        wpercent = (mywidth / float(background.size[0]))
        hsize = int((float(background.size[1]) * float(wpercent)))
        background = background.resize((mywidth, hsize), PIL.Image.ANTIALIAS)
    
    quality_val = 95
    ###END OF OPTIMIZATION###
    if hebrew:
        if has_sticky:
            background = background.convert('RGB')  # Convert image to JPG saveable form
            background.save(path.split('.')[0] + '_sticky_hebrew.jpg','JPEG', quality=quality_val)
        else:
            background = background.convert('RGB')  # Convert image to JPG saveable form
            background.save(path.split('.')[0] + '_hebrew.jpg','JPEG', quality=quality_val)
    else:
        if has_sticky:
            background = background.convert('RGB')  # Convert image to JPG saveable form
            background.save(path.split('.')[0] + '_sticky.jpg','JPEG', quality=quality_val)
        else:
            background = background.convert('RGB')  # Convert image to JPG saveable form
            background.save(path.split('.')[0] + '.jpg','JPEG', quality=quality_val)


        # background.show()

    return path