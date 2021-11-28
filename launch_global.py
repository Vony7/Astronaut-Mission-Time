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
launch_vehicles = []
for x in linestoken:
    if not x.startswith("#"):
        from datetime import datetime
        time_liftoff = datetime.strptime(x.split()[0],'%m/%d/%YT%H:%M')
        launch_time.append(time_liftoff)
        launch_country.append(x.split()[1])
        launch_results.append(int(x.split()[2]))
        launch_sites.append(x.split()[3])
        launch_vehicles.append(x.split()[4])
token.close()

# Process Data
rockets = np.unique(launch_vehicles)
# Launch countries
countries = np.unique(launch_country)
# Launch Sites
L_sites = np.unique(launch_sites)
# Launch vechicles
L_vehicles = np.unique(launch_vehicles)
c_dict = {'CHN':'中国','ESA':'欧空局','IND':'印度','IRN':'伊朗','JPN':'日本','RUS':'俄罗斯','SKO':'韩国','USA':'美国'}
# Launch countries x time
launch_total = np.zeros((len(launch_time),countries.size),dtype=int)
color_country = np.array(['#A30000','#194852','#3989b9','cyan','#fcc9b9','#0033A0','#FFA500','#002868'])
launch_success = np.zeros(len(countries),dtype=int)
launch_failure = np.zeros(len(countries),dtype=int)
launch_overall = np.zeros(len(countries),dtype=int)
launch_Bysites = np.zeros(len(L_sites),dtype=int)
launch_Byvehicles = np.zeros(len(L_vehicles),dtype=int)
for i in np.arange(0,len(launch_time)):
    #launch sites
    site_idx = [id for id,x in enumerate(L_sites) if x ==launch_sites[i]]
    launch_Bysites[site_idx]+=1
    #launch vehicles
    lv_idx = [id for id,x in enumerate(L_vehicles) if x ==launch_vehicles[i]]
    launch_Byvehicles[lv_idx]+=1
    #launch country
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
plt.bar(countries,launch_failure[x_idx],color = '#d21404',label='失败')
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

#%% By Launch Site
dict_sites = {'Baikonur':'拜科努', 'Semnan':'森南', 'JSLC':'酒泉', 'KSC':'肯尼迪', 'Kodaik':'柯迪科', 'Kourou':'库鲁', 'Mahia':'玛西亚', 'Mojave':'莫哈维', 'Naro':'罗老','Plesetsk':'普列谢', 'SDSC':'萨第什','TSLC':'太原','Tanegashima':'种子岛','USC':'内之浦','Vandenberg':'范登堡','Vostochny':'东方','WSLS':'文昌','Wallops':'沃乐普','XSLC':'西昌'}
cc_dict = {'CHN':'#A30000','ESA':'#194852','IND':'#3989b9','IRN':'cyan','JPN':'#fcc9b9','RUS':'#0033A0','SKO':'#FFA500','USA':'#002868'}
sites_idx = np.argsort(launch_Bysites)
site_colors = []
launch_country = np.array(launch_country)
for site in L_sites:
    s_idx = launch_sites.index(site)
    s_country = launch_country[s_idx]
    s_bar_color = cc_dict[s_country]
    site_colors.append(s_bar_color)
    #print(site,s_country,s_bar_color)
site_colors = np.array(site_colors)
x_labels=[]
for site in L_sites:
    x_labels.append(dict_sites[site])
x_labels = np.array(x_labels)

fig=plt.figure(figsize=(12,8),dpi=300)
axes1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
axes1.xaxis.set_ticks(np.arange(0,len(dict_sites)))
axes1.xaxis.set_ticklabels(x_labels[sites_idx],fontproperties = fprop)
axes1.yaxis.set_major_locator(MultipleLocator(5))
axes1.yaxis.set_minor_locator(MultipleLocator(1))
plt.title('2021年全球航天入轨各发射场统计',fontproperties = fprop_title, fontsize = 30)
plt.ylabel('发射次数',fontproperties=fprop)
plt.xlabel('航天发射场/中心名称',fontproperties=fprop)
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
axes1.text(.9, 1.35,"截至北京时间："+ time_now, fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
axes1.text(.9, 1.30,"绘制：@Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
axes2 = fig.add_axes([-.05, 0.25, 0.7, 0.7]) # inset axes
axes1.bar(L_sites[sites_idx],launch_Bysites[sites_idx],color = site_colors[sites_idx])
for rect in axes1.patches:
    y_value = rect.get_height()
    x_value = rect.get_x()+rect.get_width()/2
    space = 0
    va = 'bottom'
    if y_value<0:
        space*=-1
        va='top'
    label="{:.0f}".format(y_value)
    axes1.annotate(
        label,
        (x_value,y_value),
        xytext=(0,space),
        textcoords = "offset points",
        ha = 'center',
        va = va
    )  
sizes = launch_overall[x_idx]/len(launch_time)*100
explode = (0, 0,0,0,0,0,0,0)
patches,p_text=axes2.pie(sizes,colors = color_country[x_idx],explode=explode, shadow=False, startangle=90)
axes2.legend(patches,xaxis_labels,loc='center right',bbox_to_anchor=(1.1, 0.5),prop =fprop)
for font in p_text:
    font.set_fontproperties(fprop)
plt.savefig('launch_2021_by_sites2.png')

#%% By Launch Vehicle
dict_vehicles = {'Antares' 'Ariane-5' 'Atlas-V' 'CZ-2C' 'CZ-2C/YZ-1S' 'CZ-2D' 'CZ-2F'
 'CZ-3B/E' 'CZ-3C/E' 'CZ-4B' 'CZ-4C' 'CZ-5B' 'CZ-6' 'CZ-7' 'CZ-7A'
 'Delta-IVH' 'Electron' 'Epsilong' 'Falcon-9B5' 'Firefly-Alpha'
 'GSLV-MKII' 'H-IIA' 'Hyperbola-1' 'KSLV-II' 'Kuaizhou-1A' 'LauncherOne'
 'Minotar-1' 'PSLV-DL' 'Pegasus-XL' 'Proton-M' 'Rocket-3.3' 'Simorgh'
 'Soyuz-2.1a' 'Soyuz-2.1a/Fregat' 'Soyuz-2.1b' 'Soyuz-2.1b/Fregat'
 'Soyuz-2.1v/Volga' 'Vega'}
cc_dict = {'CHN':'#A30000','ESA':'#194852','IND':'#3989b9','IRN':'cyan','JPN':'#fcc9b9','RUS':'#0033A0','SKO':'#FFA500','USA':'#002868'}
vehicles_colors = []
launch_country = np.array(launch_country)
for vehicle in L_vehicles:
    v_idx = launch_vehicles.index(vehicle)
    v_country = launch_country[v_idx]
    v_bar_color = cc_dict[v_country]
    vehicles_colors.append(v_bar_color)
    #print(site,s_country,s_bar_color)
vehicles_colors = np.array(vehicles_colors)
# Launch Vehicles
launch_Byvehicles = np.array(launch_Byvehicles)
L_vehicles = np.array(L_vehicles)
lv_idx = argsort(launch_Byvehicles)
fig4,ax4 = plt.subplots(1,figsize=(12,8),dpi=300)
plt.bar(L_vehicles[lv_idx],launch_Byvehicles[lv_idx],color = vehicles_colors[lv_idx])
for rect in ax4.patches:
    y_value = rect.get_height()
    x_value = rect.get_x()+rect.get_width()/2
    space = 0
    va = 'bottom'
    if y_value<0:
        space*=-1
        va='top'
    label="{:.0f}".format(y_value)
    ax4.annotate(
        label,
        (x_value,y_value),
        xytext=(0,space),
        textcoords = "offset points",
        ha = 'center',
        va = va
    )  
plt.setp(ax4.get_xticklabels(),rotation=45,ha="right",rotation_mode="anchor")
ax4.yaxis.set_major_locator(MultipleLocator(5))
ax4.yaxis.set_minor_locator(MultipleLocator(1))
plt.title('2021年全球航天入轨按火箭统计',fontproperties = fprop_title, fontsize = 30)
plt.ylabel('发射次数',fontproperties=fprop)
plt.xlabel('运载火箭',fontproperties=fprop)
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
ax4.text(.9, 1.35,"截至北京时间："+ time_now, fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
ax4.text(.9, 1.30,"绘制：@Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
plt.tight_layout()
plt.savefig('launch_2021_by_lv.png')

# CZ3A series Piechart

# Soyuz 2.1 series Piechart

# CZ-4 series Piechart

# CZ7 series Pie chart
