import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from overlayPNGs import overlay

def plot_chart(dates,prices,asset_name):

    if len(dates) >= 300:
        grid_line_num = 7
    elif len(dates) >= 90:
        grid_line_num = 4
    elif len(dates) >= 30:
        grid_line_num = 4
    elif len(dates) >= 14:
        grid_line_num = 3
    else:
        grid_line_num = 4

    if prices[-1] > prices[0]:
        asset_return = True
        graph_color = 'xkcd:jade green'
    else:
        asset_return = False
        # asset_return = True
        graph_color = 'xkcd:red'

    ROI = round(100*(prices[-1]/prices[0] -1),2)
    if ROI > 0:
        ROI = '+' + "%.2f" % ROI + '%'
    else:
        ROI = "%.2f" % ROI + '%'

    text_move_length = len(ROI)/1000
    max_price = np.max(prices)
    min_price = np.min(prices)

    SMALL_SIZE = 15
    MEDIUM_SIZE = 20
    BIGGER_SIZE = 50

    plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

    fig, ax = plt.subplots(figsize=(19,7.2))

    x_step_val = int(len(dates)/grid_line_num)
    y_step_val = int((max_price-min_price)/3)
    y_adj = False
    if y_step_val == 0:
        y_step_val = round((max_price-min_price)/3,2)
        y_adj = True


    if y_adj:
        if '/' in asset_name:
            tick = mtick.StrMethodFormatter('{x:,.2f}')
        else:
            tick = mtick.StrMethodFormatter('${x:,.2f}')
    else:
        if '/' in asset_name:
            tick = mtick.StrMethodFormatter('{x:,.0f}')
        else:
            tick = mtick.StrMethodFormatter('${x:,.0f}')
    ax.yaxis.set_major_formatter(tick)
    # ax = fig.add_axes([0, 0, 1, 1])
    # ax.axis('off')
    # ax.plot(prices,c='xkcd:jade green',linewidth=1)
    plt.plot(prices,graph_color,linewidth=4)

    plt.title(asset_name + ' Historical Price')



    date_list = []
    month_names = {'1': 'Jan','2': 'Feb','3': 'Mar','4': 'Apr','5': 'May','6': 'Jun',
                    '7': 'Jul','8': 'Aug','9': 'Sep','10': 'Oct','11': 'Nov','12': 'Dec'}

    num_list = np.linspace(0,len(dates)-1,grid_line_num)
    for x in range(len(num_list)):
        date_list.append(dates[int(num_list[x])].split('/')[1] + '-' + month_names[dates[int(num_list[x])].split('/')[0]] + '-' + dates[int(num_list[x])].split('/')[2])

    date_list = tuple(date_list)
    plt.tick_params(top=False, bottom=False, left=False, right=False, labelleft=True, labelbottom=True)
    plt.xticks(num_list,date_list,rotation=45,ha="right")
    plt.xlim([0,len(prices)-1])
    if y_adj:
        plt.yticks(np.arange(min_price-.05*(max_price-min_price),max_price+.05*(max_price-min_price),step=y_step_val))
        plt.ylim([min_price-.05*(max_price-min_price),max_price+.04*(max_price-min_price)])
        # if asset_return:
        #     plt.text(len(prices)*(.883-text_move_length),min_price-.01*(max_price-min_price),ROI,color='white',fontweight='bold')
        # else:
        #     plt.text(len(prices)*(.9-text_move_length),max_price-.14*(max_price-min_price),ROI,color='white',fontweight='bold')

    else:
        plt.yticks(np.arange(min_price-.05*(max_price-min_price),max_price+.05*(max_price-min_price),step=y_step_val))
        plt.ylim([min_price-.05*(max_price-min_price),max_price+.01*(max_price-min_price)])
        # if asset_return:
        #     plt.text(len(prices)*(.883-.8*text_move_length),min_price-.0*(max_price-min_price),ROI,color='white',fontweight='bold')
        # else:
        #     plt.text(len(prices)*(.9-text_move_length),max_price-.16*(max_price-min_price),ROI,color='white',fontweight='bold')


    plt.grid(True,linewidth=1.5)

    # plt.grid(True,linewidth=1.5)



    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.subplots_adjust(bottom=.2)

    fig.savefig('demo.png',transparent=True)
    # plt.show()

    overlay(ROI,chart='demo.png',positive=asset_return)
