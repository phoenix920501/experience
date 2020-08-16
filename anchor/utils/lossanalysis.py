import re 
import matplotlib.pyplot as plt
import numpy as np
filepath='/your/dir/XXX.log'
title=filepath.split("/")[-1].split(".")[0]
print(title)
savedir="/your/dir"
pattern='# All'
f=open(filepath,"r")
lines=f.readlines()
# print(lines)
num=1
loss=[]
coord=[]
conf=[]
clss=[]

for line in lines:
    text=re.search(pattern,line)
    if text:
        print(num)
        start=text.span()[0]
        ll=line[start:]
        print(ll)
        loss_start=re.search('Loss',ll).span()[1]+1
        loss_end=re.search('Coord',ll).span()[0]-2
        lossvalue=ll[loss_start:loss_end]
        coord_start=re.search('Coord',ll).span()[1]+1
        coord_end=re.search('Conf',ll).span()[0]-1
        coordvalue=ll[coord_start:coord_end]
        conf_start=re.search('Conf',ll).span()[1]+1
        conf_end=re.search('Cls',ll).span()[0]-1
        confvalue=ll[conf_start:conf_end]
        clss_start=re.search('Cls',ll).span()[1]+1
        clss_end=re.search('\n',ll).span()[1]-2
        clssvalue=ll[clss_start:clss_end]
        print("loss:",lossvalue,"coord:",coordvalue,"conf:",confvalue,"cls:",clssvalue)
        loss.append(float(lossvalue))
        coord.append(float(coordvalue))
        conf.append(float(confvalue))
        clss.append(float(clssvalue))
        num+=1
print("Loss:",loss,len(loss))
print("coord:",coord,len(coord))
print("conf:",conf,len(conf))
print("cls:",clss,len(clss))

anchor=7677

total_loss=[]
add_loss=0
total_coord=[]
add_coord=0
total_conf=[]
add_conf=0
total_clss=[]
add_clss=0
num=0
for i in range(1,len(loss)+1):
        if i % anchor == 0 :
            add_loss+=loss[i-1]
            total_loss.append(add_loss)
            add_coord+=coord[i-1]
            total_coord.append(add_coord)
            add_conf+=conf[i-1]
            total_conf.append(add_conf)
            add_clss+=clss[i-1]
            total_clss.append(add_clss)
            add_loss=0
            add_coord=0
            add_conf=0
            add_clss=0
        else:
            add_loss+=loss[i-1]
            add_coord+=coord[i-1]
            add_conf+=conf[i-1]
            add_clss+=clss[i-1]
        num+=1
print("tatal_loss:",total_loss,len(total_loss))
print("tatal_coord:",total_coord,len(total_coord))
print("tatal_conf:",total_conf,len(total_conf))
print("tatal_clss:",total_clss,len(total_clss))
print("num:",num)

x=np.arange(1,len(total_loss)+1)
f1 = np.polyfit(x, total_loss, 2)
p1 = np.poly1d(f1)
pre_total_loss=p1(x)
print("pre_total_loss:",pre_total_loss)

f2 = np.polyfit(x, total_coord, 2)
p2 = np.poly1d(f2)
pre_total_coord=p2(x)
print("pre_total_coord:",pre_total_coord)

f3 = np.polyfit(x, total_conf, 2)
p3 = np.poly1d(f3)
pre_total_conf=p3(x)
print("pre_total_conf:",pre_total_conf)

f4 = np.polyfit(x, total_clss, 2)
p4 = np.poly1d(f4)
pre_total_clss=p4(x)
print("pre_total_clss:",pre_total_clss)

#可视化

# print(x,len(x))
# plt.plot(x,loss,"r")
# plt.scatter(x,total_loss)
plt.plot(x, total_loss, 's',label='original values')
plt.plot(x, pre_total_loss, 'r',label='polyfit values')
plt.xlabel('epoch')
plt.ylabel('total_loss')
plt.legend(loc=1)
plt.title(title)
plt.savefig(savedir+'/{}_total_loss.jpg'.format(title))
plt.close()

# plt.scatter(x,total_coord)
plt.plot(x, total_coord, 's',label='original values')
plt.plot(x, pre_total_coord, 'r',label='polyfit values')
plt.xlabel('epoch')
plt.ylabel('total_coord')
plt.legend(loc=1)
plt.title(title)
plt.savefig(savedir+'/{}_total_coord.jpg'.format(title))
plt.close()

# plt.scatter(x,total_conf)
plt.plot(x, total_conf, 's',label='original values')
plt.plot(x, pre_total_conf, 'r',label='polyfit values')
plt.xlabel('epoch')
plt.ylabel('total_conf')
plt.legend(loc=1)
plt.title(title)
plt.savefig(savedir+'/{}_total_conf.jpg'.format(title))
plt.close()

# plt.scatter(x,total_clss)
plt.plot(x, total_clss, 's',label='original values')
plt.plot(x, pre_total_clss, 'r',label='polyfit values')
plt.xlabel('epoch')
plt.ylabel('total_clss')
plt.legend(loc=1)
plt.title(title)
plt.savefig(savedir+'/{}_total_cls.jpg'.format(title))
plt.close()