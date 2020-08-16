# -*- cooding: utf-8 -*-
#h5_to_pb.py

from keras.models import load_model
import tensorflow as tf
import os 
import os.path as osp
from keras import backend as K
from tensorflow.python.framework import graph_util,graph_io
from tensorflow.python.tools import import_pb_to_tensorboard
#路径参数
#路径
input_path = '/'
#hdf5模型
weight_file = 'xxx.hdf5'

weight_file_path = osp.join(input_path,weight_file)
#模型保存命名
output_graph_name = weight_file[:-5] +"_xxx.pb"
#转换函数
def h5_to_pb(h5_model,output_dir,model_name,out_prefix = "pb_",log_tensorboard = True):
    if osp.exists(output_dir) == False:
        os.mkdir(output_dir)
    out_nodes = []
    for i in range(len(h5_model.outputs)):
        out_nodes.append(out_prefix + str(i + 1))
        tf.identity(h5_model.output[i],out_prefix + str(i + 1))
    print("out_nodes:",out_nodes)
    sess = K.get_session()
    
    init_graph = sess.graph.as_graph_def()
    main_graph = graph_util.convert_variables_to_constants(sess,init_graph,out_nodes)
    graph_io.write_graph(main_graph,output_dir,name = model_name,as_text = False)
    if log_tensorboard:
        import_pb_to_tensorboard.import_to_tensorboard(osp.join(output_dir,model_name),output_dir)
#输出路径
output_dir = os.getcwd()
#加载模型
h5_model = load_model(weight_file_path)
h5_to_pb(h5_model,output_dir = output_dir,model_name = output_graph_name)
print('model saved')