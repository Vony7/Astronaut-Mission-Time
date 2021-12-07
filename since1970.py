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
datatxt = 'since1970'
token = open(datatxt + '.txt','r')
linestoken=token.readlines()
tokens_column_number = 1
year_time = []
num_launches = []
success = []
failure = []
failure_partial = []
for x in linestoken:
    if not x.startswith("#"):
        year_time.append(int(x.split()[0]))
        num_launches.append(int(x.split()[1]))
        success.append(int(x.split()[2]))
        failure.append(int(x.split()[3]))
        failure_partial.append(int(x.split()[4]))
token.close()
total_launches = sum(num_launches)
print(total_launches,sum(success),sum(failure),sum(failure_partial))
# PLOT
fig,ax = plt.subplots(1,figsize=(10,8),dpi=300)
plt.bar(year_time,failure,color = '#e22030')
plt.bar(year_time,failure_partial,bottom=failure,color='orange')
bt = [a+b for a,b in zip(failure,failure_partial)]
plt.bar(year_time,success,bottom = bt ,color = '#00aeac')
ax.legend(['失败','部分成功','成功'],prop = fprop)
plt.xlabel('时间（年）', fontproperties = fprop)
plt.ylabel('数量', fontproperties = fprop)
plt.title('1970年以来我国航天发射统计',fontproperties = fprop_title, fontsize = 30)
for i in range(len(year_time)):
    datastr = "{:.0f}".format(num_launches[i])
    plt.annotate(datastr,xy=(year_time[i],num_launches[i]),ha='center',va='bottom',color='black',fontsize=8)
from datetime import datetime
time_now = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y/%m/%d %H:%M:%S')
ax.text(.3, 0.95,"截至北京时间："+ time_now, fontproperties=fprop,color="gray",transform=ax.transAxes,va='center')
ax.text(.42, 0.90,"绘制：@Vony7", fontproperties=fprop,color="gray", transform=ax.transAxes)
plt.xticks(np.arange(1970,max(year_time),5), rotation = 0,fontsize=8)
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.yaxis.set_minor_locator(MultipleLocator(1))
plt.xlim([1970-1,max(year_time)+1])
plt.savefig('since_1970.png')
