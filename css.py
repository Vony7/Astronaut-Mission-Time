import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from pathlib import Path
from dateutil import parser
#from datetime import timedelta
from datetime import datetime
from pylab import *
import pytz
import matplotlib.font_manager as fm
def css_func():
    fprop_title = fm.FontProperties(fname='font/ZhiMangXing-Regular.ttf')
    fprop = fm.FontProperties(fname='font/NotoSansSC-Regular.otf')
    datatxt = 'css_datalist'
    token = open(datatxt + '.txt','r')
    linestoken=token.readlines()
    tokens_column_number = 1
    missions_task = []
    missions_type = []
    missions_start = []
    missions_end = []
    missions_duration = []
    for x in linestoken:
        mission_task = x.split()[0]
        mission_type = x.split()[1]
        mission_start = x.split()[2]
        from datetime import datetime
        mission_start = datetime.strptime(mission_start,'%Y/%m/%dT%H:%M:%S')
        mission_end = x.split()[3]
        missions_task.append(mission_task)
        missions_type.append(mission_type)
        missions_start.append(mission_start)
        if mission_end=='0':
            mission_end = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%dT%H:%M:%S')
            mission_end = datetime.strptime(mission_end,'%Y/%m/%dT%H:%M:%S')
            missions_end.append(mission_end)
        else:
            mission_end = datetime.strptime(mission_end,'%Y/%m/%dT%H:%M:%S')
            missions_end.append(mission_end)
        missions_duration.append(mission_end-mission_start)
    token.close()
    data = {'Task':missions_task,'Type':missions_type,'Start':missions_start,'End':missions_end}
    df = pd.DataFrame(data)
    # start date
    proj_start = df.Start.min()
    # duration
    df['start_num'] = (pd.to_datetime(df.Start)-pd.to_datetime(proj_start)).astype('timedelta64[s]')/24/3600
    df['end_num'] = (pd.to_datetime(df.End)-pd.to_datetime(proj_start)).astype('timedelta64[s]')/24/3600
    df['days_start_to_end']=(df.end_num -df.start_num)
    dfs = df.sort_values('Start',ascending=False)
    idx = []
    for k in df.start_num:
        idx.append(k)
    for k in df.end_num:
        idx.append(k)
    x_tk_labels = []
    for h in missions_start:
        x_tk_labels.append(h)
    for h in missions_end:
        x_tk_labels.append(h)
    # create a column with the color for each department
    def color(row):
        c_dict = {'core':'#3d7c43', 'cargo':'#f79804', 'crew':'#e30000','clep':'#36454f','pec':'#d6723b'}
        return c_dict[row['Type']]
    dfs['color'] = dfs.apply(color, axis=1)
    #%% PLOT
    from matplotlib.patches import Patch
    fig, ax = plt.subplots(1, figsize=(12,6),dpi=300)
    ax.set_facecolor('black')
    I=plt.legend(loc='upper center', prop=fprop, ncol=5,frameon=False)
    for text in I.get_texts():
        text.set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white') 
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    plt.rcParams['savefig.facecolor']='black'
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', which='both',colors='white')
    ax.barh(dfs.Task, dfs.days_start_to_end, left=dfs.start_num,height=0.5, color=dfs.color)
    ##### add data labels #####
    for rect in ax.patches:
        height = rect.get_height()
        width = rect.get_width()
        x = rect.get_x()
        y = rect.get_y()
        label_text = f'{width:.1f}'
        label_x = x + width/2
        label_y = y + height/2
        if height>0:
            ax.text(label_x,label_y,label_text,color='white',ha='center',va='center',fontsize=12)
    plt.title('中国空间站建设工程',fontproperties = fprop_title,fontsize =30,color='white')
    ### Y axis labes###
    y_axis_labels = ['天和一号','天舟二号','神舟十二号','天舟三号','神舟十三号']
    y_labels = reversed(y_axis_labels)
    ax.set_yticklabels(y_labels, fontproperties = fprop,fontsize = 16)
    time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
    ax.text(.01, 0.1,"截至北京时间："+ time_now, fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
    ax.text(.01, 0.03,"绘制：@Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
    ##### TICKS #####
    ax.set_xticks(idx)
    ax.set_xticklabels(x_tk_labels,rotation=10)
    ax.set_xlabel('北京时间（UTC+8)',fontproperties = fprop)
    fig.autofmt_xdate()
    plt.savefig('css_mission_timeline.png')
if __name__=='__main__':
    css_func()