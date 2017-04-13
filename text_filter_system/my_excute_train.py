from excute_training import *
from filter_common import *

Id = "ffa991b0-463d-11e4-91bd-90b11c12f2b5"
Id2 = "24ce6a88-9014-11e2-8e1e-90b11c12f2b5"
# 8b64df017d39758ad6e01061a86c02b3
Md5 = get_md5_value(Id2)
print(Md5)

train_data_list=[{"id":Id2}]
excute_cnn_train("nothing", train_data_list)
