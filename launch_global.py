#global launch 
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
fprop_title = fm.FontProperties(fname='font/ZhiMangXing-Regular.ttf')
fprop = fm.FontProperties(fname='font/NotoSansSC-Regular.otf')
datatxt = 'launchglobal'
token = open(datatxt + '.txt','r',encoding = 'utf8')
linestoken=token.readlines()
launch_time = []
launch_country = []
launch_results = []
launch_sites = []
launch_rockets = []
for x in linestoken:
    if not x.startswith("#"):
        from datetime import datetime
        time_liftoff = datetime.strptime(x.split()[0],'%m/%d/%YT%H:%M')
        launch_time.append(time_liftoff)
        launch_country.append(x.split()[1])
        launch_results.append(int(x.split()[2]))
        launch_sites.append(x.split()[3])
        launch_rockets.append(x.split()[4])
token.close()

# Process Data
rockets = np.unique(launch_rockets)
# Launch countries
countries = np.unique(launch_country)
# Launch Sites
L_sites = np.unique(launch_sites)
print(L_sites)
c_dict = {'CHN':'中国','ESA':'欧空局','IND':'印度','IRN':'伊朗','JPN':'日本','RUS':'俄罗斯','SKO':'韩国','USA':'美国'}

# Launch countries x time
launch_total = np.zeros((len(launch_time),countries.size),dtype=int)
color_country = ['#FF0000','#194852','#3989b9','cyan','#fcc9b9','#0033A0','#FFA500','#002868']
launch_success = np.zeros(len(countries),dtype=int)
launch_failure = np.zeros(len(countries),dtype=int)
launch_overall = np.zeros(len(countries),dtype=int)
for i in np.arange(0,len(launch_time)):
    country = launch_country[i]
    idx = [i for i,x in enumerate(countries) if x ==country]
    if(launch_results[i]>0):
        launch_success[idx]+=1
    else:
        launch_failure[idx]+=1
    launch_total[i][idx]=1
    launch_overall[idx] +=1
    if(i>0):
        launch_total[i]=launch_total[i-1]
        launch_total[i][idx]=launch_total[i-1][idx]+1 
# Step PLOT by Country
fig,ax = plt.subplots(1,figsize=(12,8),dpi=200)
for j in np.arange(0,countries.size):
    x_value = launch_time
    y_value = launch_total[:,j]
    plt.step(x_value,y_value,'-',color = color_country[j],label=c_dict[countries[j]],linewidth=4)
plt.legend(prop =fprop)
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_minor_locator(MultipleLocator(1))
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
ax.text(.3, 0.95,"截至北京时间："+ time_now, fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
ax.text(.32, 0.90,"绘制：@Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
plt.title('2021年全球航天入轨发射统计',fontproperties = fprop_title, fontsize = 30)
plt.xlabel('时间',fontproperties=fprop)
plt.ylabel('发射次数',fontproperties=fprop)
plt.ylim(ymin=0)
plt.xlim(datetime(2021,1,8,0,0),xmax=max(x_value))
ax.yaxis.tick_right()
ax.yaxis.set_label_position('right')
plt.savefig('launch_2021_step.png')

#%% Bar By Country
x_idx = np.argsort(launch_overall)
xaxis_labels = []
for country in countries[x_idx]:
    xaxis_labels.append(c_dict[country])
fig,ax = plt.subplots(1,figsize=(8,6),dpi=300)
plt.bar(countries, launch_overall[x_idx])
ax.xaxis.set_ticks(np.arange(0,len(countries)))
ax.xaxis.set_ticklabels(xaxis_labels,fontproperties = fprop)
# Data Labels
for rect in ax.patches:
    y_value = rect.get_height()
    x_value = rect.get_x()+rect.get_width()/2
    space = 0
    va = 'bottom'
    if y_value<0:
        space*=-1
        va='top'
    label="{:.0f}".format(y_value)
    ax.annotate(
        label,
        (x_value,y_value),
        xytext=(0,space),
        textcoords = "offset points",
        ha = 'center',
        va = va
    )    
plt.bar(countries,launch_failure[x_idx],color = '#e22030',label='失败')
plt.bar(countries, launch_success[x_idx],bottom = launch_failure[x_idx], color = '#053047',label='成功')
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
ax.text(.3, 0.92,"截至北京时间："+ time_now, fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
ax.text(.42, 0.87,"绘制：@Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_minor_locator(MultipleLocator(1))
plt.ylabel('发射次数', fontproperties = fprop)
plt.title('2021年全球航天入轨发射统计',fontproperties = fprop_title, fontsize = 30)
plt.legend(loc='upper center', prop =fprop,ncol=2,frameon=False)
plt.savefig('launch_2021_barplot.png')

#%% Print out
print('Total Launches: ', len(launch_time))
print(countries)
print(launch_overall)
print(launch_success)
print(launch_failure)

#%% Pie Chart
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
fig,ax = plt.subplots(1,figsize=(12,8),dpi=200)
sizes = launch_overall/len(launch_time)*100
explode = (0, 0,0,0,0,0,0,0)
l_text,p_text=plt.pie(sizes, labels=xaxis_labels,colors = color_country,explode=explode, shadow=False, startangle=90)
for font in p_text:
    font.set_fontproperties(fprop)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.savefig('launch_2021_piechart.png')

#%% By Launch Site

#%% By Launch Vehicle