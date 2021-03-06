from sumit_training_data import *

"""positive_data to data list"""
positive_data_file="/Users/li_pengju/tensorflow1.0/sample/mission_filter/data/right.txt"
positive_examples = list(open(positive_data_file, "r").readlines())
pos_submit = [{"id":s.strip().split('\t')[0],
              "text":s.strip().split('\t')[-1],
              "result":"TRUE"} for s in positive_examples[1:]]

"""negative_data_file to data list"""
negative_data_file="/Users/li_pengju/tensorflow1.0/sample/mission_filter/data/wrong.txt"
negative_examples = list(open(negative_data_file, "r").readlines())
neg_submit=[{"id":s.strip().split('\t')[0],
            "text":s.strip().split('\t')[-1],
            "result":"FALSE"} for s in negative_examples]

# 测试right部分的输入，写入到data_dir/id/TRUE/untrain
train_data_list=pos_submit
cnn_submit("nothing", train_data_list)

# 测试wrong部分的输入，写入到data_dir/id/TRUE/untrain
train_data_list=neg_submit
cnn_submit("nothing", train_data_list)
