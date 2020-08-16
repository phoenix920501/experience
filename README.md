# 检测算法经验分享    

## want to do                
### 1、基础神经元
如何理解神经网络是一个最基本的问题？目前的神经网络是一种由数据驱动的模型，所以数据的质量至关重要，其实神经网络并不能准确的定义为“智能”，更准确的理解应该定义为一种记忆力，这种记忆力的能力的强弱是一方面由数据中信息的数量和多样性决定的，另一方面由网络本身所能包容的信息的能力决定，也就是说，当数据包含的信息量远大于网络最大的信息包容量时，模型就废掉了。所以构造神经网络最重要的是如何提高神经网络的信息包容能力，更具体的说是如何提高单个神经元的能力  
目前神经元可以理解为一个开关，达到阈值，开关开，未达到阈值，开关闭，只能控制两种状态。增加激活函数可以引入非线性，那么神经元的最后输出可以理解为一种特殊的分布.那这种分布可不可以用高斯分布或其他分布代替，从而获得更好的表达能力.再进一步，神经元这个开关控制两种状态，那能不能设计为三种状态或者更多的状态来提高单个神经元的信息的包容能力

### 2、channel
如何理解目标检测中的channel？一般解释为，在降低特征图大小时，需要提高channel数量来保持模型的复杂度.但对channel的期待不仅仅是为了提高模型的复杂度，而是寄希望于channel能学习到图片中的景深信息.通俗理解为，类似于CT中各个切面的图片，希望channel可以把图片的平面信息还原到图片的立体信息，例如有个大象，现在有大象六个面的图片，通过channel学习到了大象的立体信息，现在这时候给一张大象的任何角度的图片，模型都可以实现对大象的准确识别，这时候channel就能使模型能力极大提升.现在的关键的是如何学习图片中物体的立体信息.能否用核函数代替神经元把图片还原到高维中学习特征，又或者直接设计特殊的网络结构学习这种立体信息

## yolo results    

1、[数据集统计信息](stat/readme.md)       
2、[anchor实验结果](anchor/readme.md)（一阶段）  
3、[anchor分层聚类统计信息](groupstat/readme.md)   
4、[anchor实验结果](anchor/lastresults.md)（二阶段）    
5、[anchor实验结果](anchor/last.md)（三阶段）    
6、[loss分析结果](anchor/lossanalysis.md)   
7、[yolov3 anchor优化及darknet迁移实验结果](yolo_pytorch/README.md)   
8、[yolov4 实验结果](yolov4/readme.md)

## centernet results

1、[centernet网络结构优化](centernet/optimization.md)

## 模型转换

1、[ckpt_to_pb](models/ckpt_to_pb/readme.md)             
2、[hdf5_to_pb](models/hdf5_to_pb/readme.md)     
    

## 论文研读    
1、[ratinanet读书报告](paper/ratinanet/ratinanet.md)     
2、[Yolo读书报告](paper/yolo/Yolov3.docx)       
3、[centernet读书报告](paper/centernet/readme.md)(国科大)      
5、[centernet读书报告](paper/center/readme.md)(得大)      
6、[其他](paper/note/readme.md)     

## 工具（utils）        
[工具](utils/readme.md)    

# 注意：实验结果普遍高于论文结果可能的原因是：在训练数据集中除了voc、coco和object365等公开数据集外还加入了自己制作的数据集，这些数据集场景高度单一而且在训练集和测试集中占据很大的比例
