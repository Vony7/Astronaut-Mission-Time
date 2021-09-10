# -*- coding: utf-8 -*-
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
        self.total_eva_time = 0
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
        
    def addEVA(self,EVA):
        self.EVAs.append(EVA)
        self.num_of_evas = len(self.EVAs)
        self.EVA_time.append(EVA.duration)
        self.total_eva_time = sum(self.EVA_time)
        
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
    def __init__(self, eva_id,start_time, end_time, crews, mission):
        self.eva_id = eva_id
        self.crews = crews
        self.start_time = parser.parse(start_time)
        self.end_time = parser.parse(end_time)
        self.duration = (self.end_time-self.start_time).total_seconds()/3600
        for crew in crews:
            crew.addEVA(self)

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
#EID,start, end,[crew1,crew2],mission
sz7eva1 = EVA("sz7eva1",'2008/9/27 16:35','2008/9/27 17:01',[zzg,lbm],sz7)
sz12eva1 = EVA("sz12eva1",'2021/7/5 8:11','2021/7/5 14:57',[lbm,thb],sz12)
sz12eva2 = EVA("sz12eva2",'2021/8/21 8:38','2021/8/21 14:33',[nhs,lbm],sz12)
EVAs = [sz7eva1,sz12eva1,sz12eva2]

#%% Prepare Data for plot
sorted_astro = sorted(astro,key = operator.attrgetter("num_of_missions"))
fprop_title = fm.FontProperties(fname='font/ZhiMangXing-Regular.ttf')
fprop = fm.FontProperties(fname='font/NotoSansSC-Regular.otf')
y_names,x_vals = zip(*[(i.name,float(i.num_of_missions)) for i in sorted_astro])
y_pos = np.arange(len(sorted_astro))
#%% EVA Time
eva_total = [hty.total_eva_time for hty in astro]
c = np.zeros((len(EVAs),len(astro)))
fig1,ax = plt.subplots(figsize=(16,12),dpi=300)
astro_names = [hty.name for hty in astro]
legend_names =[eva.eva_id for eva in EVAs]
bottom = 0
for eva in EVAs:
    idx_eva = EVAs.index(eva)
    for crew in eva.crews :
        idx_crew = astro.index(crew)
        c[idx_eva,idx_crew] = eva.duration
    ptt = plt.bar(astro_names,c[idx_eva],bottom=bottom)
    #axx.bar_label(ptt,label_type='center',fmt='%.2f')
    bottom +=c[idx_eva]
I=plt.legend(legend_names,prop=fprop,loc='upper center',facecolor='black',ncol=len(astro),frameon=False)
plt.plot(astro_names,eva_total,'.r')
for text in I.get_texts():
    text.set_color('white')
# add data labels
for rect in ax.patches:
    height = rect.get_height()
    width = rect.get_width()
    x = rect.get_x()
    y = rect.get_y()
    label_text = f'{height:.2f}'
    label_x = x+width/2
    label_y = y+height/2
    if height>0:
        ax.text(label_x,label_y,label_text, color='white',ha = 'center', va = 'center',fontsize = 8)
#make labels
for i in range(len(astro)):
    datastr = "{:.2f}".format(eva_total[i])
    plt.annotate(datastr,xy=(astro_names[i],eva_total[i]),ha='center',va='bottom',color='white')
plt.xlabel("航天员", fontproperties=fprop,fontsize=20,color='white')
ymax = np.amax(eva_total)
ax.set_xticklabels(astro_names,fontproperties=fprop,fontsize=16,color='white')
ax.set_yticks(np.arange(0,ymax+10,step=1))
ax.set_yticklabels(np.arange(0,ymax+10,step=1),fontproperties=fprop,fontsize=16,color='white')
#data labels
plt.ylabel("出舱时间（小时）", fontproperties=fprop,fontsize=20,color='white')
plt.ylim(0,np.amax(eva_total)+2)
plt.title("中国航天员出舱时间统计",fontproperties=fprop_title,fontsize=40,color='white')
now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
ax.text(.4, 0.95,"截至北京时间："+ now.strftime("%Y/%m/%d %H:%M:%S.%f"), fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
ax.text(.45, 0.92,"绘制：@Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
ax.set_facecolor("black")
plt.rcParams['savefig.facecolor']='black'
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', which='both',colors='white')
plt.savefig('eva-time-stacked.png')

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
I=plt.legend(legend_names,prop=fprop,loc='upper center',facecolor='black',ncol=len(astro),frameon=False)
plt.plot(astro_names,astro_total,'.r')
for text in I.get_texts():
    text.set_color('white')
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
    plt.annotate(datastr,xy=(astro_names[i],astro_total[i]),ha='center',va='bottom',color='white')
plt.xlabel("航天员", fontproperties=fprop,fontsize=20,color='white')
ymax = np.amax(astro_total)
print(np.arange(0,ymax+10,step=10))
axx.set_xticklabels(astro_names,fontproperties=fprop,fontsize=16,color='white')
axx.set_yticks(np.arange(0,ymax+10,step=10))
axx.set_yticklabels(np.arange(0,ymax+10,step=10),fontproperties=fprop,fontsize=16,color='white')
#data labels
plt.ylabel("在轨时间（天）", fontproperties=fprop,fontsize=20,color='white')
plt.ylim(0,np.amax(astro_total)+10)
plt.title("中国航天员在轨时间统计",fontproperties=fprop_title,fontsize=40,color='white')
now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
axx.yaxis.set_minor_locator(tck.AutoMinorLocator())
axx.text(.4, 0.95,"截至北京时间："+ now.strftime("%Y/%m/%d %H:%M:%S.%f"), fontproperties=fprop,color="gray",transform=axx.transAxes,va='center')
axx.text(.45, 0.92,"绘制：@Vony7", fontproperties=fprop,color="gray", transform=axx.transAxes)
axx.set_facecolor("black")
plt.rcParams['savefig.facecolor']='black'
axx.spines['bottom'].set_color('white')
axx.spines['top'].set_color('white') 
axx.spines['right'].set_color('white')
axx.spines['left'].set_color('white')
axx.tick_params(axis='x', colors='white')
axx.tick_params(axis='y', which='both',colors='white')
plt.savefig('mission-time-stacked.png')

