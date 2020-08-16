# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np

# 数据集BGR统计信息
'''     args:datasetdir：数据集所在目录
             savedir:保存目录
        return:bgr均值方差统计信息 txt文件
'''

datasetdir="/your/dir/"
savedir="/your/dir/"

datasetslist=os.listdir(datasetdir)
print("datasets:",datasetslist)
print("dataset num:",len(datasetslist))
totaltxtpath=os.path.join(savedir,"total.txt")
dataset_b_mean=[]
dataset_g_mean=[]
dataset_r_mean=[]
for j in range(len(datasetslist)):
        datasetname=datasetslist[j]
        print("datasetname:",datasetname)
        datadir=os.path.join(datasetdir,datasetname)
        print("datasetdir:",datadir)
        xmldir=os.path.join(datadir,"Annotations")
        print("xmldir:",xmldir)
        imgdir=os.path.join(datadir,"JPEGImages")
        print("imgdir:",imgdir)

        imglist=os.listdir(imgdir)
        print("imglist:",imglist)
        print("img num:",len(imglist))
        txtname=datasetname+'.txt'
        txtpath=os.path.join(savedir,txtname)
        print("txtpath:",txtpath)
        all_b_mean=[]
        all_g_mean=[]
        all_r_mean=[]
        for i in range(len(imglist)):
                imgname=imglist[i]
                imgpath=os.path.join(imgdir,imgname)
                #print("imgpath:",imgpath)
                img = cv2.imread(imgpath)
                #print("imgshape:",img.shape)
                b,g,r = cv2.split(img)
                b_mean=round(np.mean(b),3)
                all_b_mean.append(b_mean)
                g_mean=round(np.mean(g),3)
                all_g_mean.append(g_mean)
                r_mean=round(np.mean(r),3)
                all_r_mean.append(r_mean)
                b_std=round(np.std(b),3)             
                g_std=round(np.std(g),3)   
                r_std=round(np.std(r),3)        
                #print(b_mean,g_mean,r_mean)
                text=imgname+' '+str(b_mean)+' '+str(b_std)+' '+str(g_mean)+' '+str(g_std)+' '+str(r_mean)+' '+str(r_std)+'\n'
                print(text)
                f = open(txtpath,'a')
                f.write(text)
                f.close()
        mean_b=round(np.mean(all_b_mean),3)
        dataset_b_mean.append(mean_b)
        mean_g=round(np.mean(all_g_mean),3)
        dataset_g_mean.append(mean_g)
        mean_r=round(np.mean(all_r_mean),3)
        dataset_r_mean.append(mean_r)
        std_b=round(np.std(all_b_mean),3)
        std_g=round(np.std(all_g_mean),3)   
        std_r=round(np.std(all_r_mean),3)     
        datasettext=datasetname+' '+str(mean_b)+' '+str(std_b)+' '+str(mean_g)+' '+str(std_g)+' '+str(mean_r)+' '+str(std_r)+'\n'
        print(datasettext)
        print("imgnum:",len(all_b_mean))
        f = open(totaltxtpath,'a')
        f.write(datasettext)
        f.close()
total_b_mean=round(np.mean(dataset_b_mean),3)     
total_g_mean=round(np.mean(dataset_g_mean),3) 
total_r_mean=round(np.mean(dataset_r_mean),3) 
total_b_std=round(np.std(dataset_b_mean),3)     
total_g_std=round(np.std(dataset_g_mean),3) 
total_r_std=round(np.std(dataset_r_mean),3) 
print("b_mean:",total_b_mean,"b_std:",total_b_std)
print("g_mean:",total_g_mean,"g_std:",total_g_std)
print("r_mean:",total_r_mean,"r_std:",total_r_std)
print("datasetnum:",len(dataset_b_mean))
bgrtext="total:"+' b:'+str(total_b_mean)+' '+str(total_b_std)+' g:'+str(total_g_mean)+' '+str(total_g_std)+' r:'+str(total_r_mean)+' '+str(total_r_std)+'\n'
f = open(totaltxtpath,'a')
f.write(bgrtext)
f.close()
print("*****finished*****")
