# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET

# 数据集宽高统计信息
'''     args:datasetdir：数据集所在目录
             savedir:保存目录
        return:数据集中目标的宽、高、宽高比统计信息 txt文件
'''

datasetdir="/your/dir/"
savedir="/your/dir/"

datasetslist=os.listdir(datasetdir)
print("datasets:",datasetslist)
print("dataset num:",len(datasetslist))

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
        txtname=datasetname+'.txt'
        txtpath=os.path.join(savedir,txtname)
        print("txtpath:",txtpath)

        for i in range(len(xmllist)):
                xmlname=xmllist[i]
                xmlpath=os.path.join(xmldir,xmlname)
                print("xmlpath:",xmlpath)
                #in_file = open(xmlpath,'r',encoding='utf-8')
                in_file = open(xmlpath,'r')
                tree=ET.parse(in_file)
                root = tree.getroot()
                size=root.find("size")
                #print("size:",size)
                picwidth=int(size.find('width').text)
                picheight=int(size.find('height').text)
                print("picsize:",picwidth,picheight)
                for child in root.iter('object'):
                        classname = child.find('name').text
                        #print("object:",classname)
                        xmlbox = child.find('bndbox')
                        box = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text),int(xmlbox.find('xmax').text),  int(xmlbox.find('ymax').text))
                        #print("box:",box,(type(box)))
                        width=box[2]-box[0]
                        height=box[3]-box[1]
                        aspectratio=round(width/(height+0.01),3)
                        #print("width:",width,"height:",height,"aspectratio:",aspectratio)
                        text=classname+" "+str(picwidth)+" "+ str(picheight)+" "+str(width)+" "+str(height)+" "+str(aspectratio)+"\n"
                        print(text)
                        f = open(txtpath,'a')
                        f.write(text)
                        f.close()
                print("*****finish*****",xmlname)
        print("*****finish*****",datasetname)
