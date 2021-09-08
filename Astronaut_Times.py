# -*- coding: utf-8 -*-
"""
Spyder Editor
"""
from dateutil import parser
import datetime
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.font_manager as fm
import operator 
from matplotlib import cm
from colorspacious import cspace_converter
from collections import OrderedDict
import matplotlib.ticker as tck
cmaps = OrderedDict()
class Astronaut:
    def __init__(self, name, uid, gender, DOB):
        self.name = name
        self.uid = uid
        self.gender = gender
        self.DOB = parser.parse(DOB)
        self.missions = []
        self.mission_time = []
        self.total_time = 0
        self.num_of_missions = len(self.missions)
        self.age = (datetime.datetime.utcnow()+datetime.timedelta(hours=8)-self.DOB).days/365.2425
        self.EVAs = []  
        self.EVA_time =[]
    def getDetails(self):
        print("Name: ", self.name)
        print("Gender: ",self.gender)
        print("Date of Birth: ",self.DOB)        
        print("Age: ",round(self.age,1)," Years Old")
        print("Number of Missions: ",self.num_of_missions)

        for mission in self.missions:
            print(mission.name)
        
    def addMission(self,mission):
        self.missions.append(mission)
        self.num_of_missions=len(self.missions)
        self.mission_time.append(mission.duration)
        self.total_time = sum(self.mission_time)
        
    def addEVA(self, EVA):
        self.EVAs.append(EVA)
        
class Mission:
    def __init__(self,name,mid,start,end,crews):
        self.name = name
        self.mid = mid
        self.start_date = parser.parse(start)
        if end==0:
            self.status = "Ongoing"
            self.end_date = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        else:
            self.status = "Completed"
            self.end_date = parser.parse(end)
        self.crews = crews
        self.duration = (self.end_date-self.start_date).total_seconds()/24/3600
        for crew in crews:
            crew.addMission(self)            
        self.number_of_crew = len(self.crews)
        
class EVA:
    def __init__(self, eva_id,start_time, end_time, crew, mission):
        self.eva_id = eva_id
        self.start_time = parser.parse(start_time)
        self.end_time = parser.parse(end_time)
        self.duration = self.end_time-self.start_time
        

#%% Add Astronauts
# Name, uid, gender, date of birth
ylw = Astronaut('杨利伟','ylw','Male', '1965/06/1')
nhs = Astronaut('聂海胜','nhs','Male', '1964/09/1')
fjl = Astronaut('费俊龙','fjl','Male', '1965/5/1')
zzg = Astronaut('翟志刚','zzg','Male', '1966/10/1')
jhp = Astronaut('景海鹏','jhp','Male', '1966/10/1')
lbm = Astronaut('刘伯明','lbm','Male','1966/9/1')
lw = Astronaut('刘旺','lw','Male','1969/3/1')
ly = Astronaut('刘洋','ly','Female','1978/10/01')
zxg = Astronaut('张晓光','zxg','Male','1966/5/1')
wyp = Astronaut('王亚平','wyp','Female','1980/01/01')
cd = Astronaut('陈冬','cd','Male','1978/12/01')
thb = Astronaut('汤洪波','thb','Male','1975/10/1')
astro = [ylw,nhs,fjl,zzg,jhp,lbm,lw,ly,zxg,wyp,cd,thb]

# Add Missions
# Name, MID, Start, End,[crew1, crew2, crew3]
sz5 = Mission("神舟五号",'sz5','2003/10/15 9:00:00','2003/10/16 6:22:00',[ylw])
sz6 = Mission("神舟六号",'sz6','2005/10/12 9:00:00','2005/10/17 4:33:00',[fjl,nhs])
sz7 = Mission("神舟七号",'sz7','2008/09/25 21:10:00','2008/09/28 17:37:00',[zzg,lbm,jhp])
sz9 = Mission("神舟九号",'sz9','2012/06/16 18:37:00','2012/06/29 10:03:00',[jhp,lw,ly])
sz10 = Mission("神舟十号",'sz10','2013/06/11 17:38:00','2013/06/26 8:07:00',[nhs,zxg,wyp])
sz11= Mission("神舟十一号",'sz11','2016/10/17 7:30:00','2016/11/18 13:59:00',[jhp,cd])
sz12= Mission("神舟十二号",'sz12','2021/06/17 9:22:00',0,[nhs,lbm,thb])

missions = [sz5,sz6,sz7,sz9,sz10,sz11,sz12]
# Add EVAs
sz7eva1 = EVA("cz7eva1",'2008/9/27 16:35','2008/9/27 17:01',[zzg,lbm],sz7)
sz12eva1 = EVA("sz12eva1",'2021/7/5 8:11','2021/7/5 14:57',[lbm,thb],sz12)
sz12eva2 = EVA("sz12eva2",'2021/8/21 8:38','2021/8/21 14:33',[nhs,lbm],sz12)
EVAs = [sz7eva1,sz12eva1,sz12eva2]

#%% Prepare Data for plot
sorted_astro = sorted(astro,key = operator.attrgetter("num_of_missions"))
fprop = fm.FontProperties(fname='font/NotoSansSC-Regular.otf')
y_names,x_vals = zip(*[(i.name,float(i.num_of_missions)) for i in sorted_astro])
y_pos = np.arange(len(sorted_astro))

#%% plot different missions
# plot bars in stack manner
c = np.zeros((len(missions),len(astro)))
figx,axx = plt.subplots(figsize=(16,12),dpi=300)
astro_names = [hty.name for hty in astro]
legend_names =[sz.name for sz in missions]
astro_total = [hty.total_time for hty in astro]
bottom = 0
for sz in missions:
    idx_sz = missions.index(sz)
    for crew in sz.crews:
        idx_crew = astro.index(crew)
        c[idx_sz,idx_crew] = sz.duration
    ptt = plt.bar(astro_names,c[idx_sz],bottom=bottom)
    #axx.bar_label(ptt,label_type='center',fmt='%.2f')
    bottom +=c[idx_sz]
plt.legend(legend_names,prop=fprop,loc='upper center',ncol=len(astro))
plt.plot(astro_names,astro_total,'.k')
# add data labels
for rect in axx.patches:
    height = rect.get_height()
    width = rect.get_width()
    x = rect.get_x()
    y = rect.get_y()
    label_text = f'{height:.2f}'
    label_x = x+width/2
    label_y = y+height/2
    if height>0:
        axx.text(label_x,label_y,label_text, color='white',ha = 'center', va = 'center',fontsize = 8)
#make labels
for i in range(len(astro)):
    datastr = "{:.2f}".format(astro_total[i])
    plt.annotate(datastr,xy=(astro_names[i],astro_total[i]),ha='center',va='bottom')
plt.xlabel("中国航天员", fontproperties=fprop)
axx.set_xticklabels(astro_names,fontproperties=fprop)
#data labels
plt.ylabel("在轨时间（天）", fontproperties=fprop)
plt.ylim(0,np.amax(astro_total)+10)
plt.title("中国航天员在轨时间统计",fontproperties=fprop,fontsize=20)
now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
#axx.tick_params(axis='y',which='minor',bottom=True)
axx.yaxis.set_minor_locator(tck.AutoMinorLocator())
axx.text(.4, 0.95,"截至北京时间："+ now.strftime("%Y/%m/%d %H:%M:%S.%f"), fontproperties=fprop,color="gray",transform=axx.transAxes,va='center')
axx.text(.45, 0.92,"绘制：@Vony7", fontproperties=fprop,color="gray", transform=axx.transAxes)
plt.savefig('mission-time-stacked.png')
#%% plot person by person

""" #%% Plot Number of Missions
fig, ax = plt.subplots(figsize=(8,6),dpi=300)
ax.barh(y_pos, x_vals)
ax.set_yticks(y_pos)
ax.set_yticklabels(y_names,fontproperties=fprop,fontsize=16,rotation=0)
ax.bar_label(ax.containers[0],fmt='%.0f')
rlim = max(x_vals)+1
xtick = np.arange(rlim)
ax.set_xticks(xtick)
ax.set_xlim(right=rlim)  # adjust xlim to fit labels
ax.set_xlabel('任务次数（次）',fontproperties=fprop,fontsize=16,rotation=0)
now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
ax.text(.64, 0.05,"截至北京时间："+ now.strftime("%Y/%m/%d %H:%M:%S"), fontproperties=fprop,transform=ax.transAxes,va='center')
#plt.tight_layout()
plt.savefig("number_of_missions.png")

#%% Plot Mission Time
# color map
#colours = {'FIRST':'#FC6238','SECOND':'#FFD872','THIRD':'#F2D4CC','FORTH':'#E77577','FIFTH':'#6C88C4'}
colours = {'FIRST':'#173F5F','SECOND':'#20639B','THIRD':'#3CAEA3','FORTH':'#F6D55C','FIFTH':'#ED553B'}

def next_key(dict, key):
    keys = iter(dict)
    key in keys
    return next(keys, False)

sorted1 = sorted(astro,key = operator.attrgetter("total_time"))
y_names,x_vals = zip(*[(i.name,float(i.total_time)) for i in sorted1])

fig2,ax2 = plt.subplots(figsize=(8,6), dpi=300)
for k in range(len(sorted1)):
    bt = 0
    hbar = ax2.barh(k,sorted1[k].missions[0].duration,color=colours['FIRST'])
    key = next_key(colours,'FIRST')
    h = 1
    while h<len(sorted1[k].missions):
        bt+=sorted1[k].missions[h-1].duration
        hbar = ax2.barh(k,sorted1[k].missions[h].duration,left=bt,color=colours[key])
        key = next_key(colours,key)
        h+=1
    ax2.bar_label(hbar,fmt='%.2f')    
ax2.set_yticks(y_pos)
ax2.set_yticklabels(y_names,fontproperties=fprop,fontsize=16,rotation=0)
rlim = max(x_vals)+8
ax2.set_xlim(right=rlim)  # adjust xlim to fit labels
ax2.text(.62, 0.1,"截至北京时间："+ now.strftime("%Y/%m/%d %H:%M:%S"), fontproperties=fprop,transform=ax.transAxes,va='center')
ax2.text(.62,0.05,"制图：@Vony7", fontproperties=fprop,transform=ax.transAxes,va='center')
ax2.set_xlabel('任务时间（天）',fontproperties=fprop,fontsize=16,rotation=0)
#plt.tight_layout()     
plt.savefig("total mission time.png") """

#%% Plot different color for each mission
# plot bars in stack manner
""" fig3,ax3 = plt.subplots(figsize=(8,6),dpi=300)
for k in range(len(sorted1)):
    bt = 0
    hbar = ax3.barh(k,sorted1[k].missions[0].duration,color=colours['FIRST'])
    key = next_key(colours,'FIRST')
    h = 1
    while h<len(sorted1[k].missions):
        bt+=sorted1[k].missions[h-1].duration
        hbar = ax3.barh(k,sorted1[k].missions[h].duration,left=bt)
        key = next_key(colours,key)
        h+=1
    ax3.bar_label(hbar,fmt='%.2f')    
ax3.set_yticks(y_pos)
ax3.set_yticklabels(y_names,fontproperties=fprop,fontsize=16,rotation=0)
rlim = max(x_vals)+8
ax3.set_xlim(right=rlim)  # adjust xlim to fit labels
ax3.text(.62, 0.1,"截至北京时间："+ now.strftime("%Y/%m/%d %H:%M:%S"), fontproperties=fprop,transform=ax.transAxes,va='center')
ax3.text(.62,0.05,"制图：@Vony7", fontproperties=fprop,transform=ax.transAxes,va='center')
ax3.set_xlabel('任务时间（天）',fontproperties=fprop,fontsize=16,rotation=0)
#plt.tight_layout()     
#plt.legend(loc='lower right')
plt.savefig("total mission time stacked all.png") """


#%% Plot based on EVA time
