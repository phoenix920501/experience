# -*- coding: utf-8 -*
import numpy as np
import os
import matplotlib.pyplot as plt
import random
class Box():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h



def overlap(x1, len1, x2, len2):
    len1_half = len1 / 2
    len2_half = len2 / 2

    left = max(x1 - len1_half, x2 - len2_half)
    right = min(x1 + len1_half, x2 + len2_half)

    return right - left



def box_intersection(a, b):
    w = overlap(a.x, a.w, b.x, b.w)
    h = overlap(a.y, a.h, b.y, b.h)
    if w < 0 or h < 0:
        return 0

    area = w * h
    return area



def box_union(a, b):
    i = box_intersection(a, b)
    u = a.w * a.h + b.w * b.h - i
    return u


def box_iou(a, b):
    return box_intersection(a, b) / box_union(a, b)



def init_centroids(boxes,n_anchors):
    centroids = []
    boxes_num = len(boxes)

    # centroid_index = np.random.choice(boxes_num, 1)#plus=0
    centroid_index = int(np.random.choice(boxes_num, 1))#plus=1
    centroids.append(boxes[centroid_index])

    print(centroids[0].w,centroids[0].h)

    for centroid_index in range(0,n_anchors-1):

        sum_distance = 0
        distance_thresh = 0
        distance_list = []
        cur_sum = 0

        for box in boxes:
            min_distance = 1
            for centroid_i, centroid in enumerate(centroids):
                distance = (1 - box_iou(box, centroid))
                if distance < min_distance:
                    min_distance = distance
            sum_distance += min_distance
            distance_list.append(min_distance)

        distance_thresh = sum_distance*np.random.random()

        for i in range(0,boxes_num):
            cur_sum += distance_list[i]
            if cur_sum > distance_thresh:
                centroids.append(boxes[i])
                print(boxes[i].w, boxes[i].h)
                break

    return centroids



def do_kmeans(n_anchors, boxes, centroids):
    loss = 0
    groups = []
    new_centroids = []
    for i in range(n_anchors):
        groups.append([])
        new_centroids.append(Box(0, 0, 0, 0))

    for box in boxes:
        min_distance = 1
        group_index = 0
        for centroid_index, centroid in enumerate(centroids):
            distance = (1 - box_iou(box, centroid))
            if distance < min_distance:
                min_distance = distance
                group_index = centroid_index
        groups[group_index].append(box)
        loss += min_distance
        new_centroids[group_index].w += box.w
        new_centroids[group_index].h += box.h

    for i in range(n_anchors):
        new_centroids[i].w /= len(groups[i])
        new_centroids[i].h /= len(groups[i])

    return new_centroids, groups, loss

def compute_width_height(temp,keepaspectratio=1):
    if keepaspectratio==1:
                print("keepaspectratio******")
                scale=max((float(temp[1]))/cropsize,(float(temp[2]))/cropsize)
                width=round(float(temp[3])/scale,3)
                height=round(float(temp[4])/scale,3)
    else:
                print("NO keepaspectratio******")
                width=round((float(temp[3])/float(temp[1]))*cropsize,3)
                height=round((float(temp[4])/float(temp[2]))*cropsize,3)
    return width,height

def randomcolor(i):
        print(i)
        colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
        color = ""
        for i in range(6):
            color += colorArr[random.randint(0,14)]
        return "#"+color

def compute_centroids(datasetdir,n_anchors,loss_convergence,iterations_num,plus,cropsize,savedir,labels,keepaspectratio=1):
    
    allboxes={}
    for label in labels:
        allboxes.setdefault(label,[])
    print(allboxes)
    # exit()
    datasetslist=os.listdir(datasetdir)
    print("datasets:",datasetslist)
    print("dataset num:",len(datasetslist))
    savepath=os.path.join(savedir,"clusterresults.txt")
    print("savepath:",savepath)
  
    for i in range(len(datasetslist)):
        datasetname=datasetslist[i]
        print("datasetname:",datasetname)
        datapath=os.path.join(datasetdir,datasetname)
        print("datapath:",datapath)
        #for label_file in label_files:
        f = open(datapath)
        lines= f.readlines()
        #print("lines:",lines)
        for line in lines:
                #print(line)
                temp = line.strip().split(" ")
                print("temp:",temp)
                width,height=compute_width_height(temp,keepaspectratio=0)
                print("width-height:",width,height)
                label=temp[0]
                allboxes[label].append(Box(0, 0, width, height))
        
    
    x=[]
    for label, boxes in allboxes.items():
        print("label:",label)
        print("boxes:",len(boxes))
        if plus:
            centroids = init_centroids(boxes, n_anchors)
            print("init centroids")
        else:
            centroid_indices = np.random.choice(len(boxes), n_anchors)
            centroids = []
            for centroid_index in centroid_indices:
                centroids.append(boxes[centroid_index])

        # iterate k-means
        centroids, groups, old_loss = do_kmeans(n_anchors, boxes, centroids)
        iterations = 1
        while (True):
            centroids, groups, loss = do_kmeans(n_anchors, boxes, centroids)
            iterations = iterations + 1
            print("iterations:",iterations)
            print("loss = %f" % loss)
            if abs(old_loss - loss) < loss_convergence or iterations > iterations_num:
                break
            old_loss = loss

            for centroid in centroids:
                print(centroid.w , centroid.h )
            #print(centroid.w * grid_size, centroid.h * grid_size)

        num=1
        for centroid in centroids:
            x.append([centroid.w,centroid.h])
            aspectratio=round(centroid.w/centroid.h,3)
            text=label+"anchor"+str(num)+" "+str(round(centroid.w,3))+" "+str(round(centroid.h,3))+" "+str(aspectratio)+"\n"
            print(text)
            num+=1
            f = open(savepath,'a')
            f.write(text)
            f.close()
    
    #可视化
    x=np.array(x)
    print(x)

    color=[]
    for i in range(16):
        c=randomcolor(i)
        if c not in color:
            color.append(c)
    print("color:",color)

    colors={}
    for label in labels:
        colors.setdefault(str(labels.index(label)),color[labels.index(label)])
    print("colors:",colors)


    plt.title("scatter points",fontsize=24)
    plt.xlabel("width",fontsize=14)
    plt.ylabel("height",fontsize=14)
    for i in range(16):
        start=i*9
        end=start+8
        print(start,end)
        clr=colors[str(i)]
        print(clr)
        plt.scatter(x[start:end,0], x[start:end,1],  c=clr, label=labels[i], s=40)
    plt.legend(loc='upper right')
    plt.savefig('/opt/data/hyh/yolo_pytorch/yolo/data2/anchors.jpg')


datasetdir="/opt/data/hyh/yolo_pytorch/yolo/data1"
savedir="/opt/data/hyh/yolo_pytorch/yolo/data2"

labels=["person","bike","motorbike","car","truck","tanker","bus","trainroof","train","roadcone","rock","animal","box","tyre","wovenbag","workplate"]

n_anchors = 9
loss_convergence = 1e-6#loss最小变化阈值
grid_size = 13
cropsize=608
iterations_num = 1000
plus = 1#为1是k-means++算法，为0是k-means算法，区别是k-means++算法的初始化时取间隔较大的几个点

compute_centroids(datasetdir,n_anchors,loss_convergence,iterations_num,plus,cropsize,savedir,labels,keepaspectratio=0)