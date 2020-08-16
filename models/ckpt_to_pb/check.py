#打印ckpt或pb模型的tensor

# ckpt模型  
#第一种方法：  
from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file 
checkpoint_path="/your/path"
print_tensors_in_checkpoint_file(checkpoint_path,tensor_name='', all_tensors=True, all_tensor_names=True)

#第二种方法：
from tensorflow.python import pywrap_tensorflow
checkpoint_path = "/your/path"
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()
n=0
for key in var_to_shape_map:
    print("tensor_name: ", key)
    #print("****",reader.get_tensor(key))
    n+=1
print("n:",n)

#pb模型
#打印tensor
import tensorflow as tf
import os
out_pb_path="/your/path"
def create_graph():
    with tf.gfile.FastGFile(out_pb_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')
        
create_graph()
tensor_name_list = [tensor.name for tensor in tf.get_default_graph().as_graph_def().node]
m=0
for tensor_name in tensor_name_list:
    print("pd:",tensor_name,'\n')
    m+=1
print("m:",m)

#获得pb模型的图
import tensorflow as tf
from tensorflow.python.platform import gfile

model = "/your/path"
graph = tf.get_default_graph()
graph_def = graph.as_graph_def()
graph_def.ParseFromString(gfile.FastGFile(model, 'rb').read())
tf.import_graph_def(graph_def, name='graph')
summaryWriter = tf.summary.FileWriter('log/', graph)

#命令tensorboard --logdir=/opt/data/hyh/tboard/tusimple_lanenet/vgg
