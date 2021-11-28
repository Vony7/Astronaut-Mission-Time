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
launch_vehicles_family = []
launch_rockets = []
for x in linestoken:
    if not x.startswith("#"):
        from datetime import datetime
        time_liftoff = datetime.strptime(x.split()[0],'%m/%d/%YT%H:%M')
        launch_time.append(time_liftoff)
        launch_country.append(x.split()[1])
        launch_results.append(int(x.split()[2]))
        launch_sites.append(x.split()[3])
        launch_vehicles_family.append(x.split()[4])
        launch_rockets.append(x.split()[5])
token.close()

# Process Data
rockets = np.unique(launch_vehicles_family)
# Launch countries
countries = np.unique(launch_country)
# Launch Sites
L_sites = np.unique(launch_sites)
# Launch vechicles
L_vehicles = np.unique(launch_vehicles_family)
# Launch rockets
L_rockets = np.unique(launch_rockets)
# country dictionary EN => CN
c_dict = {'CHN':'中国','ESA':'欧空局','IND':'印度','IRN':'伊朗','JPN':'日本','RUS':'俄罗斯','SKO':'韩国','USA':'美国'}
# color code by country
color_country = np.array(['#A30000','#194852','#3989b9','cyan','#fcc9b9','#0033A0','#FFA500','#002868'])

# Launch countries x time
launch_total = np.zeros((len(launch_time),countries.size),dtype=int)
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
    lv_idx = [id for id,x in enumerate(L_vehicles) if x ==launch_vehicles_family[i]]
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
plt.savefig('launch_2021_by_sites.png')

#%% By Launch Vehicle
cc_dict = {'CHN':'#A30000','ESA':'#194852','IND':'#3989b9','IRN':'cyan','JPN':'#fcc9b9','RUS':'#0033A0','SKO':'#FFA500','USA':'#002868'}
vehicles_colors = []
launch_country = np.array(launch_country)
for vehicle in L_vehicles:
    v_idx = launch_vehicles_family.index(vehicle)
    v_country = launch_country[v_idx]
    v_bar_color = cc_dict[v_country]
    vehicles_colors.append(v_bar_color)
    #print(site,s_country,s_bar_color)
vehicles_colors = np.array(vehicles_colors)
# Launch Vehicles
launch_Byvehicles = np.array(launch_Byvehicles)
L_vehicles = np.array(L_vehicles)
lv_idx = argsort(launch_Byvehicles)
fig=plt.figure(figsize=(12,8),dpi=300)
axes1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
axes1.bar(L_vehicles[lv_idx],launch_Byvehicles[lv_idx],color = vehicles_colors[lv_idx])
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
plt.setp(axes1.get_xticklabels(),rotation=45,ha="right",rotation_mode="anchor")
axes1.yaxis.set_major_locator(MultipleLocator(5))
axes1.yaxis.set_minor_locator(MultipleLocator(1))
plt.title('2021年全球航天入轨按火箭统计',fontproperties = fprop_title, fontsize = 30)
plt.ylabel('发射次数',fontproperties=fprop)
plt.xlabel('运载火箭',fontproperties=fprop)
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
axes1.text(.92, 1.30,"截至北京时间："+ time_now, fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
axes1.text(.92, 1.26,"绘制：@Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
# add legend for bar plot
import matplotlib.patches as mpatches
handles = []
for country in countries:
    handle = mpatches.Patch(color=cc_dict[country],label=c_dict[country])
    handles.append(handle)
plt.legend(handles = handles,loc='upper center',ncol=len(countries),prop=fprop)

# add axes 2, soyuz 
axes2 = fig.add_axes([0.0,0.36,0.5,0.5])
rocket_series = np.array(launch_vehicles_family)
all_rockets = np.array(launch_rockets)
cz_3a_idx = np.where(rocket_series=='Soyuz-2.1')
cz_3as = all_rockets[cz_3a_idx]
cz_3as_unq,cz_3as_count = np.unique(cz_3as,return_counts=True)
def pie_chart_labels(data):
    total = int(np.sum(data))
    percentages = [100.0 * x / total for x in data]
    fmt_str = "{:.0f}%\n({:d})"
    return [fmt_str.format(p,i) for p,i in zip(percentages, data)]
wedges, texts,  = axes2.pie(cz_3as_count, labels=pie_chart_labels(cz_3as_count))
# shrink label positions to be inside the pie
for t in texts:
    x,y = t.get_position()
    t.set_x(0.5 * x)
    t.set_y(0.5 * y)
plt.setp(texts, size=10, weight="bold", color="w", ha='center')
axes2.legend(cz_3as_unq,bbox_to_anchor=(.9, 1.0))

# add, CZ-4
axes3 = fig.add_axes([0.08,0.18,0.2,0.2])
rocket_series = np.array(launch_vehicles_family)
all_rockets = np.array(launch_rockets)
cz_3a_idx = np.where(rocket_series=='CZ-4')
cz_3as = all_rockets[cz_3a_idx]
cz_3as_unq,cz_3as_count = np.unique(cz_3as,return_counts=True)
def pie_chart_labels(data):
    total = int(np.sum(data))
    percentages = [100.0 * x / total for x in data]
    fmt_str = "{:.0f}%\n({:d})"
    return [fmt_str.format(p,i) for p,i in zip(percentages, data)]
wedges, texts,  = axes3.pie(cz_3as_count, labels=pie_chart_labels(cz_3as_count))
# shrink label positions to be inside the pie
for t in texts:
    x,y = t.get_position()
    t.set_x(0.5 * x)
    t.set_y(0.5 * y)
plt.setp(texts, size=10, weight="bold", color="w", ha='center')
axes3.legend(cz_3as_unq,bbox_to_anchor=(.9, 1.0))

# add CZ-3A
axes4 = fig.add_axes([0.52,0.32,0.2,0.2])
rocket_series = np.array(launch_vehicles_family)
all_rockets = np.array(launch_rockets)
cz_3a_idx = np.where(rocket_series=='CZ-3A')
cz_3as = all_rockets[cz_3a_idx]
cz_3as_unq,cz_3as_count = np.unique(cz_3as,return_counts=True)
def pie_chart_labels(data):
    total = int(np.sum(data))
    percentages = [100.0 * x / total for x in data]
    fmt_str = "{:.0f}%\n({:d})"
    return [fmt_str.format(p,i) for p,i in zip(percentages, data)]
wedges, texts,  = axes4.pie(cz_3as_count, labels=pie_chart_labels(cz_3as_count))
# shrink label positions to be inside the pie
for t in texts:
    x,y = t.get_position()
    t.set_x(0.5 * x)
    t.set_y(0.5 * y)
plt.setp(texts, size=10, weight="bold", color="w", ha='center')
axes4.legend(cz_3as_unq,bbox_to_anchor=(.9, 1.0))

# add CZ-2C
axes5 = fig.add_axes([0.52,0.55,0.2,0.2])
rocket_series = np.array(launch_vehicles_family)
all_rockets = np.array(launch_rockets)
cz_3a_idx = np.where(rocket_series=='CZ-2C')
cz_3as = all_rockets[cz_3a_idx]
cz_3as_unq,cz_3as_count = np.unique(cz_3as,return_counts=True)
def pie_chart_labels(data):
    total = int(np.sum(data))
    percentages = [100.0 * x / total for x in data]
    fmt_str = "{:.0f}%\n({:d})"
    return [fmt_str.format(p,i) for p,i in zip(percentages, data)]
wedges, texts,  = axes5.pie(cz_3as_count, labels=pie_chart_labels(cz_3as_count))
# shrink label positions to be inside the pie
for t in texts:
    x,y = t.get_position()
    t.set_x(0.5 * x)
    t.set_y(0.5 * y)
plt.setp(texts, size=10, weight="bold", color="w", ha='center')
axes5.legend(cz_3as_unq,bbox_to_anchor=(.9, 1.0))

# add CZ-7
axes6 = fig.add_axes([0.28,0.18,0.2,0.2])
rocket_series = np.array(launch_vehicles_family)
all_rockets = np.array(launch_rockets)
cz_3a_idx = np.where(rocket_series=='CZ-7')
cz_3as = all_rockets[cz_3a_idx]
cz_3as_unq,cz_3as_count = np.unique(cz_3as,return_counts=True)
def pie_chart_labels(data):
    total = int(np.sum(data))
    percentages = [100.0 * x / total for x in data]
    fmt_str = "{:.0f}%\n({:d})"
    return [fmt_str.format(p,i) for p,i in zip(percentages, data)]
wedges, texts,  = axes6.pie(cz_3as_count, labels=pie_chart_labels(cz_3as_count))
# shrink label positions to be inside the pie
for t in texts:
    x,y = t.get_position()
    t.set_x(0.5 * x)
    t.set_y(0.5 * y)
plt.setp(texts, size=10, weight="bold", color="w", ha='center')
axes6.legend(cz_3as_unq,bbox_to_anchor=(.9, 1.0))
# save
#plt.tight_layout()
plt.savefig('launch_2021_by_lv.png')

#%% CZ3A series Piechart
# find all CZ-3A launches
cz_3a_idx = np.where(rocket_series=='CZ-3A')
cz_3as = all_rockets[cz_3a_idx]
cz_3as_unq,cz_3as_count = np.unique(cz_3as,return_counts=True)
def pie_chart_labels(data):
    total = int(np.sum(data))
    percentages = [100.0 * x / total for x in data]
    fmt_str = "{:.0f}%\n({:d})"
    return [fmt_str.format(p,i) for p,i in zip(percentages, data)]
fig3as,ax3as = plt.subplots(1,figsize=(12,8),dpi=200)
wedges, texts,  = ax3as.pie(cz_3as_count, labels=pie_chart_labels(cz_3as_count))
# shrink label positions to be inside the pie
for t in texts:
    x,y = t.get_position()
    t.set_x(0.5 * x)
    t.set_y(0.5 * y)
plt.setp(texts, size=10, weight="bold", color="w", ha='center')
ax3as.legend(cz_3as_unq)
plt.savefig('count-cz-3a.png')

#%% Soyuz 2.1 series Piechart
cz_3a_idx = np.where(rocket_series=='Soyuz-2.1')
cz_3as = all_rockets[cz_3a_idx]
cz_3as_unq,cz_3as_count = np.unique(cz_3as,return_counts=True)
def pie_chart_labels(data):
    total = int(np.sum(data))
    percentages = [100.0 * x / total for x in data]
    fmt_str = "{:.0f}%\n({:d})"
    return [fmt_str.format(p,i) for p,i in zip(percentages, data)]
fig3as,ax3as = plt.subplots(1,figsize=(12,8),dpi=200)
wedges, texts,  = ax3as.pie(cz_3as_count, labels=pie_chart_labels(cz_3as_count))
# shrink label positions to be inside the pie
for t in texts:
    x,y = t.get_position()
    t.set_x(0.5 * x)
    t.set_y(0.5 * y)
plt.setp(texts, size=10, weight="bold", color="w", ha='center')
ax3as.legend(cz_3as_unq,bbox_to_anchor=(.9, 1.0))
plt.savefig('count-Soyuz-2.1.png')

#%% CZ7 series Pie chart
cz_3a_idx = np.where(rocket_series=='CZ-7')
cz_3as = all_rockets[cz_3a_idx]
cz_3as_unq,cz_3as_count = np.unique(cz_3as,return_counts=True)
def pie_chart_labels(data):
    total = int(np.sum(data))
    percentages = [100.0 * x / total for x in data]
    fmt_str = "{:.0f}%\n({:d})"
    return [fmt_str.format(p,i) for p,i in zip(percentages, data)]
fig3as,ax3as = plt.subplots(1,figsize=(12,8),dpi=200)
wedges, texts,  = ax3as.pie(cz_3as_count, labels=pie_chart_labels(cz_3as_count))
# shrink label positions to be inside the pie
for t in texts:
    x,y = t.get_position()
    t.set_x(0.5 * x)
    t.set_y(0.5 * y)
plt.setp(texts, size=10, weight="bold", color="w", ha='center')
ax3as.legend(cz_3as_unq)
plt.savefig('count-cz-7.png')
#%% CZ-4 series Piechart
cz_3a_idx = np.where(rocket_series=='CZ-4')
cz_3as = all_rockets[cz_3a_idx]
cz_3as_unq,cz_3as_count = np.unique(cz_3as,return_counts=True)
def pie_chart_labels(data):
    total = int(np.sum(data))
    percentages = [100.0 * x / total for x in data]
    fmt_str = "{:.0f}%\n({:d})"
    return [fmt_str.format(p,i) for p,i in zip(percentages, data)]
fig3as,ax3as = plt.subplots(1,figsize=(12,8),dpi=200)
wedges, texts,  = ax3as.pie(cz_3as_count, labels=pie_chart_labels(cz_3as_count))
# shrink label positions to be inside the pie
for t in texts:
    x,y = t.get_position()
    t.set_x(0.5 * x)
    t.set_y(0.5 * y)
plt.setp(texts, size=10, weight="bold", color="w", ha='center')
ax3as.legend(cz_3as_unq)
plt.savefig('count-cz-4.png')