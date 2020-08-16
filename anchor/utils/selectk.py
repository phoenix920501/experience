import numpy as np
import os
import matplotlib.pyplot as plt
import random
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

'''sklearn.cluster.KMeans(n_clusters=8,init='k-means++', n_init=10,max_iter=300,tol=0.0001, precompute_distances='auto', verbose=0, random_state=None,copy_x=True, n_jobs=1, algorithm='auto')
n_clusters: 簇的个数，即你想聚成几类
init: 初始簇中心的获取方法
n_init: 获取初始簇中心的更迭次数，为了弥补初始质心的影响，算法默认会初始10个质心，实现算法，然后返回最好的结果。
max_iter: 最大迭代次数（因为kmeans算法的实现需要迭代）
tol: 容忍度，即kmeans运行准则收敛的条件
precompute_distances:是否需要提前计算距离，这个参数会在空间和时间之间做权衡，如果是True 会把整个距离矩阵都放到内存中，auto 会默认在数据样本大于featurs*samples 的数量大于12e6 的时候False,False 时核心实现的方法是利用Cpython 来实现的
verbose: 冗长模式（不太懂是啥意思，反正一般不去改默认值）
random_state: 随机生成簇中心的状态条件。
copy_x: 对是否修改数据的一个标记，如果True，即复制了就不会修改数据。bool 在scikit-learn 很多接口中都会有这个参数的，就是是否对输入数据继续copy 操作，以便不修改用户的输入数据。这个要理解Python 的内存机制才会比较清楚。
n_jobs: 并行设置
algorithm: kmeans的实现算法，有：’auto’, ‘full’, ‘elkan’, 其中 ‘full’表示用EM方式实现
'''


def SelectK(maxK,totalList):
    K = range(1, maxK)
    meandistortions = []
    for k in K:
        print("k",k)
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(totalList)
        meandistortions.append(sum(np.min(cdist(totalList, kmeans.cluster_centers_, 'euclidean'), axis=1)) / np.array(totalList).shape[0])
    plt.plot(K, meandistortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('平均畸变程度')
    plt.xticks(K)
    plt.title('用肘部法则来确定最佳的K值')
    plt.savefig('/opt/data/hyh/yolo_pytorch/yolo/data2/k.jpg')
    # plt.show()


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

if __name__ == '__main__':
    datasetdir="/opt/data/hyh/yolo_pytorch/yolo/data1"
    # savedir="/opt/data/hyh/yolo_pytorch/yolo/data2"
    cropsize=608
    allboxes=[]
    # exit()
    datasetslist=os.listdir(datasetdir)
    print("datasets:",datasetslist)
    print("dataset num:",len(datasetslist))
  
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
                # print("width-height:",width,height)
                allboxes.append([width, height])
    print("allboxes:",len(allboxes))
    maxK=20
    SelectK(maxK,np.array(allboxes))




