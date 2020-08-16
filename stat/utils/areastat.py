# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET

# 统计大中小目标信息
'''     args:datasetdir：数据集所在目录
             savedir:保存目录
        return: 数据集中大中小目标统计信息 txt文件
'''

datasetdir="/your/dir/"
savedir="/your/dir/"

datasetslist=os.listdir(datasetdir)
print("datasets:",datasetslist)
print("dataset num:",len(datasetslist))
txtname='total.txt'
txtpath=os.path.join(savedir,txtname)
print("txtpath:",txtpath)
totalsmall=0
totalmedium=0
totallarge=0
total=0
for i in range(len(datasetslist)):
        datasetname=datasetslist[i]
        print("datasetname:",datasetname)
        datadir=os.path.join(datasetdir,datasetname)
        print("datasetdir:",datadir)
        xmldir=os.path.join(datadir,"Annotations")
        print("xmldir:",xmldir)
        imgdir=os.path.join(datadir,"JPEGImages")
        print("imgdir:",imgdir)

        xmllist=os.listdir(xmldir)
        print("xmllist:",xmllist)
        print("xml num:",len(xmllist))
        small=0
        medium=0
        large=0
        for i in range(len(xmllist)):
                xmlname=xmllist[i]
                xmlpath=os.path.join(xmldir,xmlname)
                #print("xmlpath:",xmlpath)
                in_file = open(xmlpath,'r',encoding='utf-8')
                tree=ET.parse(in_file)
                root = tree.getroot()
                size=root.find("size")
                #print("size:",size)
                picwidth=float(size.find('width').text)
                picheight=float(size.find('height').text)
                #print("picsize:",picwidth,picheight)
                for child in root.iter('object'):
                        classname = child.find('name').text
                        #print("object:",classname)
                        xmlbox = child.find('bndbox')
                        box = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text),int(xmlbox.find('xmax').text),  int(xmlbox.find('ymax').text))
                        #print("box:",box,(type(box)))
                        width=box[2]-box[0]
                        height=box[3]-box[1]
                        area=width*height
                        if area < 1024 :
                            small+=1
                            totalsmall+=1
                        elif 1024 <= area < 9216 :
                            medium+=1
                            totalmedium+=1
                        else:
                            large+=1
                            totallarge+=1
        text=datasetname+": "+"picnum:"+str(len(xmllist))+" "+"large:"+str(large)+" "+"medium:"+str(medium)+" "+"small:"+str(small)+"\n"
        print(text)
        f = open(txtpath,'a')
        f.write(text)
        f.close()     
        print("*****finish*****",datasetname)
        total+=len(xmllist)
text="total:"+str(total)+" "+"large:"+str(totallarge)+" "+"medium:"+str(totalmedium)+" "+"small:"+str(totalsmall)+"\n"
print(text)
f = open(txtpath,'a')
f.write(text)
f.close()
print("*****finish*****")