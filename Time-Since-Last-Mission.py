#!/usr/bin/env python
# coding: utf-8

# In[10]:


# -*- coding: utf-8 -*-
from dateutil import parser
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
import pytz
import datetime


# In[11]:


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


# In[12]:


#%% Add Astronauts
# Name, uid, gender, date of birth
ylw = Astronaut('杨利伟','ylw','Male', '1965/06/21')
nhs = Astronaut('聂海胜','nhs','Male', '1964/10/16')
fjl = Astronaut('费俊龙','fjl','Male', '1965/5/5')
zzg = Astronaut('翟志刚','zzg','Male', '1966/10/10')
jhp = Astronaut('景海鹏','jhp','Male', '1966/10/24')
lbm = Astronaut('刘伯明','lbm','Male','1966/9/17')
lw = Astronaut('刘旺','lw','Male','1969/3/25')
ly = Astronaut('刘洋','ly','Female','1978/10/06')
zxg = Astronaut('张晓光','zxg','Male','1966/5/1')
wyp = Astronaut('王亚平','wyp','Female','1980/01/01')
cd = Astronaut('陈冬','cd','Male','1978/12/01')
thb = Astronaut('汤洪波','thb','Male','1975/10/1')
ygf = Astronaut('叶光富','ygf','Male', '1980/9/1')
cxz = Astronaut('蔡旭哲','cxz','Male','1976/5/1')
astro = [ylw,nhs,fjl,zzg,lbm,jhp,lw,ly,zxg,wyp,cd,thb,ygf,cxz]


# In[13]:


# Add Missions
# Name, MID, Start, End,[crew1, crew2, crew3]
sz5 = Mission("神舟五号",'sz5','2003/10/15 9:00:00','2003/10/16 6:22:00',[ylw])
sz6 = Mission("神舟六号",'sz6','2005/10/12 9:00:00','2005/10/17 4:33:00',[fjl,nhs])
sz7 = Mission("神舟七号",'sz7','2008/09/25 21:10:00','2008/09/28 17:37:00',[zzg,lbm,jhp])
sz9 = Mission("神舟九号",'sz9','2012/06/16 18:37:00','2012/06/29 10:03:00',[jhp,lw,ly])
sz10 = Mission("神舟十号",'sz10','2013/06/11 17:38:00','2013/06/26 8:07:00',[nhs,zxg,wyp])
sz11= Mission("神舟十一号",'sz11','2016/10/17 7:30:00','2016/11/18 13:59:00',[jhp,cd])
sz12= Mission("神舟十二号",'sz12','2021/06/17 9:22:00','2021/09/17 13:34:00',[nhs,lbm,thb])
sz13 = Mission("神舟十三号",'sz13','2021/10/16 00:23:56','2022/04/16 09:56:00',[zzg,wyp,ygf])
sz14 = Mission('神舟十四号','sz14','2022/06/05 10:44:10',0,[cd,ly,cxz])
missions = [sz5,sz6,sz7,sz9,sz10,sz11,sz12,sz13,sz14]


# In[14]:


# Add EVAs
#EID,start, end,[crew1,crew2],mission
sz7eva1 = EVA("神舟七号第一次",'2008/9/27 16:35','2008/9/27 17:01',[zzg,lbm],sz7)
sz12eva1 = EVA("神舟十二号第一次",'2021/7/5 8:11','2021/7/5 14:57',[lbm,thb],sz12)
sz12eva2 = EVA("神舟十二号第二次",'2021/8/21 8:38','2021/8/21 14:33',[nhs,lbm],sz12)
sz13eva1 = EVA('神舟十三号第一次','2021/11/07 18:51','2021/11/08 01:16',[zzg,wyp],sz13)
sz13eva2 = EVA('神舟十三号第二次','2021/12/26 18:44','2021/12/27 00:55',[zzg,ygf],sz13)
EVAs = [sz7eva1,sz12eva1,sz12eva2,sz13eva1,sz13eva2]


# In[15]:


#%% Prepare Data for plot
sorted_astro = sorted(astro,key = operator.attrgetter("num_of_missions"))
fprop_title = fm.FontProperties(fname='font/ZhiMangXing-Regular.ttf')
fprop = fm.FontProperties(fname='font/NotoSansSC-Regular.otf')
y_names,x_vals = zip(*[(i.name,float(i.num_of_missions)) for i in sorted_astro])
y_pos = np.arange(len(sorted_astro))

#%% color palettes
color_eva= ['#1e295b','#193852','#3989b9','#79a49e','#161c37','#c6ca74','#1a425b']


# In[16]:


from dateutil import relativedelta
from matplotlib import cm
n_astro=len(astro)
cmast = cm.jet(np.arange(n_astro)/n_astro)#colors


# In[17]:


import datetime
# plot time since last mission for each crew
astro_names = [hty.name for hty in astro]
time_now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
time_since = []
for astr in astro:
    #last mission
    nm=astr.num_of_missions
    mission=astr.missions[nm-1]
    time_since_last = (time_now-mission.end_date)
    diff=relativedelta.relativedelta(time_now,mission.end_date)
    print(astr.name,diff.years, '年', diff.months,'月', diff.days, '天')
    time_since.append(diff.years+(diff.months)/12+(diff.days)/365)
ymax = np.amax(time_since)


# In[36]:


import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
txtcolor='black'
data_x = np.arange(0,len(astro))
data_hight = time_since
data_color = time_since
data_color = [x / (max(data_color)-min(data_color)) for x in data_color]
fig, ax3 = plt.subplots(figsize=(16, 6))
my_cmap = plt.cm.get_cmap('RdBu_r')
colors = my_cmap(data_color)
rects = ax3.bar(data_x, data_hight, color=colors)

sm = ScalarMappable(cmap=my_cmap)
sm.set_array(time_since)
cbar = plt.colorbar(sm)
cbar.set_label('', rotation=270,labelpad=25)

plt.xticks(data_x)   
ax3.xaxis.set_ticklabels(astro_names,fontproperties=fprop,fontsize=14,color=txtcolor)
plt.ylabel("距上一次任务结束（年）", fontproperties=fprop,fontsize=14,color=txtcolor)
#make labels
for i in range(len(astro)):
    datastr = "{:.2f}".format(time_since[i])
    plt.annotate(datastr,xy=(i,time_since[i]),ha='center',va='bottom',color=txtcolor)
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
ax3.text(.45, 0.95,"截至北京时间: "+ time_now, fontproperties=fprop,color="gray",transform=ax3.transAxes,va='center')
ax3.text(.45, .9,"绘制: @Vony7", fontproperties=fprop,color="gray", transform=ax3.transAxes)
plt.title('航天员任务间隔时间统计',fontproperties = fprop_title, fontsize = 30,color=txtcolor)
plt.savefig('time-since-last-mission.png')


# In[ ]:




