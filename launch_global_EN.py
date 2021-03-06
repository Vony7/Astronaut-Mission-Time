#global launch 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from pathlib import Path
from dateutil import parser
from datetime import datetime,timedelta
from pylab import *
import pytz
import matplotlib.font_manager as fm
import matplotlib.ticker as tck
datatxt = '2022'
token = open(datatxt + '.txt','r',encoding = 'utf8')
linestoken=token.readlines()
launch_time = []
launch_country = []
launch_results = []
launch_sites = []
launch_vehicles_family = []
launch_rockets = []
launch_pads = []
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
        launch_pads.append(x.split()[6])
token.close()

# Process Data
rockets = np.array(launch_vehicles_family)
# Launch countries
countries = np.unique(launch_country)
# Launch Sites
L_sites = np.unique(launch_sites)
# Launch vechicles
L_vehicles = np.unique(launch_vehicles_family)
# Launch rockets
L_rockets = np.unique(launch_rockets)
# country dictionary EN => CN
c_dict = {'CHN':'China','ESA':'ESA','IND':'India','IRN':'Iran','JPN':'Japan','RUS':'Russia','SKO':'S. Korea','USA':'USA'}
# color code by country
color_country = np.array(['#A30000','#194852','#3989b9','cyan','#fcc9b9','#0033A0','#FFA500','#002868'])
cc_dict = {'CHN':'#A30000','ESA':'#194852','IND':'#3989b9','IRN':'cyan','JPN':'#fcc9b9','RUS':'#0033A0','SKO':'#FFA500','USA':'#002868'}
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
#%% Print out
print(datatxt+ ' Total Launches: ', len(launch_time))
print(countries)
print('Total: ')
print(launch_overall)
print('Success: ')
print(launch_success)
print('Failure: ')
print(launch_failure)

#%% Step PLOT by Country
x_value = launch_time.copy()
time_init = datetime(int(datatxt),1,1,0,0,0)
launches_init = np.zeros((1,1),dtype=int)
time_moment = datetime.now()+timedelta(hours=15)
x_value.append(time_moment)
x_value.insert(0,time_init)
fig,ax = plt.subplots(1,figsize=(12,8),dpi=300)
for j in np.arange(0,countries.size):
    y_value = launch_total[:,j]
    y_value=np.append(y_value,y_value[-1])
    y_value = np.insert(y_value,0,launches_init,axis=0) # start from day 1 of the year
    plt.step(x_value,y_value,where='post',color = cc_dict[countries[j]],label=c_dict[countries[j]],linewidth=3)
plt.legend()
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_minor_locator(MultipleLocator(1))
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
ax.text(.3, 0.95,"Produced at: "+ time_now + " (UTC+8)", color="gray",transform=ax.transAxes,va='center')
ax.text(.3, 0.90,"Produced by: @Vony7", color="gray", transform=ax.transAxes)
plt.title('Orbital Launch Attempt in '+datatxt, fontsize = 20)
plt.xlabel('Time (UTC+8)')
plt.ylabel('Launches')
plt.ylim(ymin=0)
#plt.xlim(datetime(int(datatxt),1,8,0,0),xmax=max(x_value))
ax.yaxis.tick_right()
ax.yaxis.set_label_position('right')
plt.savefig('EN_launch_'+datatxt+'_step.png')

#%% Bar By Country
x_idx = np.argsort(launch_overall)
xaxis_labels = []
ftsz = 10
for country in countries[x_idx]:
    xaxis_labels.append(c_dict[country])
fig,ax = plt.subplots(1,figsize=(12,8),dpi=300)
plt.bar(countries, launch_overall[x_idx])
ax.xaxis.set_ticks(np.arange(0,len(countries)))
ax.xaxis.set_ticklabels(xaxis_labels,fontsize=ftsz)
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
        fontsize=ftsz,
        xytext=(0,space),
        textcoords = "offset points",
        ha = 'center',
        va = va
    )    
plt.bar(countries,launch_failure[x_idx],color = '#d21404',label='Failure')
plt.bar(countries, launch_success[x_idx],bottom = launch_failure[x_idx], color = '#007500',label='Success')
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
ax.text(.3, 0.93,"Produced at: "+ time_now + " (UTC+8)", color="gray",transform=ax.transAxes,va='center')
ax.text(.3, 0.88,"Produced by: @Vony7", color="gray", transform=ax.transAxes)
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_minor_locator(MultipleLocator(1))
yaxis_labels=np.arange(0,max(launch_overall),step=10,dtype=int)
ax.yaxis.set_ticklabels(yaxis_labels,fontsize=ftsz)
plt.ylabel('Launch', fontsize=ftsz)
plt.title('Orbital Launch Attempt in '+datatxt, fontsize = 30)
plt.legend(loc='upper center', ncol=2,frameon=False)
plt.savefig('EN_launch_'+datatxt+'_barplot.png')

#%% By Launch Site
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

fig=plt.figure(figsize=(12,8),dpi=300)
axes1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
axes1.yaxis.set_major_locator(MultipleLocator(5))
axes1.yaxis.set_minor_locator(MultipleLocator(1))
axes1.xaxis.set_ticklabels(L_sites[sites_idx])
plt.title('Orbital Launch Attempt in '+datatxt, fontsize = 30)
plt.ylabel('Launches')
plt.xlabel('Launch Site/Center')
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
axes1.text(.3, 0.95,"Produced at: "+ time_now + " (UTC+8)", color="gray",transform=ax.transAxes,va='center')
axes1.text(.3, 0.90,"Produced by: @Vony7",color="gray", transform=ax.transAxes)
axes1.bar(L_sites[sites_idx],launch_Bysites[sites_idx],color = site_colors[sites_idx])
import matplotlib.patches as mpatches
handles = []
for country in countries:
    handle = mpatches.Patch(color=cc_dict[country],label=c_dict[country])
    handles.append(handle)
axes1.legend(handles = handles,loc='upper center',ncol=len(countries))
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
# axis 2 pie plot
#sizes = launch_overall[x_idx]/len(launch_time)*100
sizes = launch_Bysites[sites_idx]/sum(launch_Bysites[sites_idx])*100
explode = np.zeros(len(sizes))
axes2 = fig.add_axes([.15, 0.3, 0.5, 0.5]) # inset axes
countries=np.array(countries)
cnt = countries[x_idx]
axes2_colors=[]
from matplotlib import cm
n_lv1 = len(sites_idx)
cs1=cm.jet(np.arange(n_lv1)/n_lv1)
for cont in cnt:
    axes2_colors.append(cc_dict[cont])
#patches,p_text=axes2.pie(sizes, explode=explode, shadow=False, startangle=90)
axes2.pie(sizes,labels=L_sites[sites_idx],colors=cs1)
plt.savefig('EN_launch_'+datatxt+'_by_sites.png')

#%% By Launch Vehicle
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
# plot
fig=plt.figure(figsize=(12,8),dpi=300)
# Axis 1
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
plt.setp(axes1.get_xticklabels(),rotation=0,ha="center",rotation_mode="anchor")
axes1.yaxis.set_major_locator(MultipleLocator(5))
axes1.yaxis.set_minor_locator(MultipleLocator(1))
plt.title('Orbital Launch Attempt in '+datatxt, fontsize = 30)
plt.ylabel('Launch')
plt.xlabel('Launch Vehicle')
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
axes1.text(.3, 0.95,"Produced at: "+ time_now + " (UTC+8)", color="gray",transform=ax.transAxes,va='center')
axes1.text(.3, 0.90,"Produced by: @Vony7", color="gray", transform=ax.transAxes)
# add legend for bar plot
import matplotlib.patches as mpatches
handles = []
for country in countries:
    handle = mpatches.Patch(color=cc_dict[country],label=c_dict[country])
    handles.append(handle)
plt.legend(handles = handles,loc='upper center',ncol=len(countries))
# save
#plt.tight_layout()
# axis 2 pie plot
#sizes = launch_overall[x_idx]/len(launch_time)*100
sizes = launch_Byvehicles[lv_idx]/sum(launch_Byvehicles[lv_idx])*100
explode = np.zeros(len(sizes))
axes2 = fig.add_axes([.15, 0.25, 0.5, 0.5]) # inset axes
#patches,p_text=axes2.pie(sizes, explode=explode, shadow=False, startangle=90)
#axes2.legend(launch_Byvehicles[lv_idx],labels=L_vehicles[lv_idx],loc='center right',bbox_to_anchor=(1.3,0.5))
from matplotlib import cm
n_lv = len(lv_idx)
cs=cm.jet(np.arange(n_lv)/n_lv)
axes2.pie(sizes,labels=L_vehicles[lv_idx],colors=cs)
plt.savefig('EN_launch_'+datatxt+'_by_lv.png')
""" 
# add axes 2, soyuz 
axes2 = fig.add_axes([0.0,0.36,0.5,0.5])
rocket_series = np.array(launch_vehicles_family)
all_rockets = np.array(launch_rockets)
cz_3a_idx = np.where(rocket_series=='Soyuz-2')
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
axes2.legend(cz_3as_unq,loc='center left',bbox_to_anchor=(.9,0.5))

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
axes5 = fig.add_axes([0.52,0.65,0.2,0.2])
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


#%%  Plot rockets launched by country (sites, launch vehicles)
fname = 'IND'
launch_country = np.array(launch_country)
# Launch by XXX 2021
country_idx = np.where(launch_country==fname)
dict_sites = {'Baikonur':'????????????', 'Semnan':'??????', 'JSLC':'??????', 'CC':'??????','CCK':'?????????', 'Kodaik':'?????????', 'Kourou':'??????', 'Mahia':'?????????', 'Mojave':'?????????', 'Naro':'??????','Plesetsk':'???????????????', 'SDSC':'?????????','TSLC':'??????','Tanegashima':'?????????','USC':'?????????','Vandenberg':'?????????','Vostochny':'??????','WSLS':'??????','Wallops':'?????????','XSLC':'??????'}
rs_dict={'CZ-2C':'?????????', 'CZ-2D':'?????????', 'CZ-2F':'??????F', 'CZ-3A':'???????????????', 'CZ-4':'???????????????', 'CZ-5':'????????????', 
'CZ-6':'??????', 'CZ-7':'????????????', 'Ceres-1':'???????????????','Hyperbola-1':'???????????????', 'Kuaizhou-1A':'???????????????',
'Vega':'?????????','Ariane-5':'???????????????','Soyuz-2':'??????-2','Proton-M':'??????-M','Angara-A5':'?????????A5',
'Pegasus-XL':'?????????XL','Minotar-1':'???????????????','Firefly-Alpha':'?????????-?????????','Delta-IV':'??????????????????','Antares':'????????????','Rocket-3':'??????-3','LauncherOne':'???????????????','Atlas-V':'???????????????','Electron':'?????????','Falcon-9':'????????????',
'H-IIA':'H-IIA','Epsilon':'????????????',
'Simorgh':'??????','PSLV-DL':'PSLV-DL','KSLV-II':'KSLV-2','GSLV-MKII':'GSLV-MK2'}
# launch sites and rockets
all_launch_sites = np.array(launch_sites)
country_sites =all_launch_sites[country_idx]
sites_uniq = np.unique(country_sites)
rocket_series = np.array(launch_vehicles_family)
country_rockets = rocket_series[country_idx]
country_rockets_uniq = np.unique(country_rockets)
rockets_fm_sites = np.zeros((len(country_rockets_uniq),len(sites_uniq)))
for r in np.arange(0,len(country_rockets_uniq)):
    r_idx = np.where(rocket_series==country_rockets_uniq[r])
    for s in np.arange(0,len(sites_uniq)):
        s_idx = np.where(all_launch_sites==sites_uniq[s])
        interaction = np.intersect1d(r_idx,s_idx)
        rockets_fm_sites[r,s]=len(interaction)

# if single launch site, use pie plot, else stack
fig,ax=plt.subplots(1,figsize=(12,8),dpi=300)
if len(sites_uniq)==1:
    ar=rockets_fm_sites.flatten()
    def pie_chart_labels(data):
        total = int(np.sum(data))
        percentages = [100.0 * x / total for x in data]
        fmt_str = "{:.0f}%\n({:.0f})"
        return [fmt_str.format(p,i) for p,i in zip(percentages, data)]
    wedges, texts,  = ax.pie(ar,labels=pie_chart_labels(ar))
    # shrink label positions to be inside the pie
    for t in texts:
        x,y = t.get_position()
        t.set_x(0.5 * x)
        t.set_y(0.5 * y)
    plt.setp(texts, size=10, weight="bold", color="w", ha='center')
    lg_labels=[]
    for rkt in country_rockets_uniq:
        lg_labels.append(rs_dict[rkt])
    ax.legend(lg_labels,prop=fprop)
    plt.title('2021???'+c_dict[fname]+'??????????????????????????????',fontproperties=fprop_title,fontsize=30)
    # author info
    from datetime import datetime
    time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
    ax.text(.35, .98,"??????????????????: "+ time_now, fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
    ax.text(.35, .94,"??????: @Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
    plt.savefig('2021_'+fname+'_by_rockets_pie.png')
else: # multiple launch sites
    # stack plot
    wd = 0.5
    btm = np.zeros((len(sites_uniq)))
    for rkt in np.arange(0,len(country_rockets_uniq)):
        ax.bar(sites_uniq, rockets_fm_sites[rkt],width=wd, bottom=btm,label=rs_dict[country_rockets_uniq[rkt]])
        btm+=rockets_fm_sites[rkt]
    x_labels=[]
    for site in sites_uniq:
        x_labels.append(dict_sites[site])
    ax.xaxis.set_ticks(np.arange(0,len(sites_uniq)))
    ax.xaxis.set_ticklabels(x_labels,fontproperties=fprop)
    lgd_cn=[]
    for lgd_en in country_rockets_uniq:
        lgd_cn.append(rs_dict[lgd_en])
    plt.title('2021???'+c_dict[fname]+'????????????????????????????????????',fontproperties=fprop_title,fontsize=30)
    plt.legend(lgd_cn,prop=fprop,loc='upper center',facecolor='black',ncol=3,frameon=False)
    plt.xlabel('?????????????????????',fontproperties=fprop,fontsize=12)
    plt.ylabel('????????????',fontproperties=fprop,fontsize=12)
    # data labels
    for rect in ax.patches:
        height=rect.get_height()
        width=rect.get_width()
        x=rect.get_x()
        y=rect.get_y()
        label_text=f'{height:.0f}'
        label_x=x+width/2
        label_y=y+height/2
        if height>0:
            ax.text(label_x,label_y,label_text,color='white',ha='center',va='center',fontsize=10)
    # author info
    from datetime import datetime
    time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
    ax.text(.35, .74,"??????????????????: "+ time_now, fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
    ax.text(.35, .7,"??????: @Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
    # data label overall
    ymax = 0
    for i in range(len(sites_uniq)):
        site_total=np.sum(rockets_fm_sites[:,i])
        datastr='{:.0f}'.format(site_total)
        ymax=max([ymax,site_total])
        plt.annotate(datastr,xy=(sites_uniq[i],site_total),ha='center',va='bottom',color='black')
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    plt.ylim([0,ymax+1])
    plt.savefig('2021_'+fname+'_by_sites_stacked.png')
    ## by rocket family
    xx_launches = rocket_series[country_idx]
    xx_rockets_2021,xx_rockets_2021_count = np.unique(xx_launches,return_counts=True)
    xx_count_idx = np.argsort(xx_rockets_2021_count)
    rkt_frm_sites = rockets_fm_sites.transpose()
    rkt_frm_sites = rkt_frm_sites[:,xx_count_idx]
    # data label overall
    rkt_2021_names= xx_rockets_2021[xx_count_idx]
    rkt_2021_total = xx_rockets_2021_count[xx_count_idx]
    rkt_labels=[]
    for rkt in rkt_2021_names:
        rkt_labels.append(rs_dict[rkt])
    fig,ax = plt.subplots(1,figsize=(12,8),dpi=300)
    btm = np.zeros((len(country_rockets_uniq)))
    for rkt in np.arange(0,len(sites_uniq)):
        ax.bar(rkt_2021_names, rkt_frm_sites[rkt], bottom=btm,label=dict_sites[sites_uniq[rkt]])
        btm+=rkt_frm_sites[rkt]
    plt.setp(ax.get_xticklabels(),rotation=0,ha="center",rotation_mode="anchor")
    # data labels
    for rect in ax.patches:
        height=rect.get_height()
        width=rect.get_width()
        x=rect.get_x()
        y=rect.get_y()
        label_text=f'{height:.0f}'
        label_x=x+width/2
        label_y=y+height/2
        if height>0:
            ax.text(label_x,label_y,label_text,color='white',ha='center',va='center',fontsize=10)
    # author info
    from datetime import datetime
    time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
    ax.text(.35, .74,"??????????????????: "+ time_now, fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
    ax.text(.35, .7,"??????: @Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
    plt.legend(x_labels,prop=fprop,loc='upper center',facecolor='black',ncol=4,frameon=False)
    plt.title('2021???'+c_dict[fname]+'?????????????????????????????????',fontproperties=fprop_title,fontsize=30)
    #plt.xlabel('????????????',fontproperties=fprop,fontsize=12)
    plt.ylabel('????????????',fontproperties=fprop,fontsize=12)
    ymax = 0
    for i in range(len(xx_rockets_2021[xx_count_idx])):
        datastr='{:.0f}'.format(rkt_2021_total[i])
        ymax=max([ymax,rkt_2021_total[i]])
        plt.annotate(datastr,xy=(rkt_2021_names[i],rkt_2021_total[i]),ha='center',va='bottom',color='black')
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.set_ticks(np.arange(0,len(rkt_2021_names)))
    ax.xaxis.set_ticklabels(rkt_labels,fontproperties=fprop)
    plt.ylim([0,ymax+1])
    plt.savefig('2021_'+fname+'_by_Rockest.png')
 """