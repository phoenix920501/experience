# ckpt模型转成pb模型  

ckpt模型转成pb模型有两种思路：   
1、读ckpt中的meta文件构造图，然后加载参数值，最后固化形成pb模型   
2、直接调用模型，然后加载参数值，最后固化形成pb模型   

## 参考
1、第一种思路：[tensorflow实现将ckpt转pb文件](https://blog.csdn.net/guyuealian/article/details/82218092)     
2、[用于TensorFlow Serving部署生产环境的saved_model 模块](https://blog.csdn.net/loveliuzz/article/details/81128024)     

## 代码   
3、convert_ckpt_to_pb.py用于转换模型     
4、check.py用于检查ckpt和pb模型的节点和tensor(工具)   

## 经验
第二种思路：
参考freeze_lanenet_model.py是如何将ckpt模型转成pb模型  
1、初始化模型，这一步需要调用整个模型，并且知道整个模型的输入和输出，如果不知道，可以通过tf.variable_scope重新定义输入输出节点的名字，不然之后调用pb模型时会不知道pb模型的输入输出的tensorname   
2、加载ckpt参数，给模型加载ckpt中保存模型参数   
3、保存为pb模型，模型持久化，变量值固定，最后序列化输出即可   