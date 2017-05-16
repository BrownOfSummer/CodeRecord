from excute_training import *
from filter_common import *
app_config = {"DATA_DIR":"/tmp/data_dir/", "MODEL_DIR":"/tmp/model_dir/"}
same_id = [{"id":"057459d8-bdca-11de-8097-0024e869955c"},
            {"id":"84e3374c-a8d6-11de-a71c-0024e869955c"},
            {"id":"b970643a-87bb-11e3-91bd-90b11c12f2b5"},
            {"id":"057459d8-bdca-11de-8097-0024e869955c"}]
train_data_list=[same_id[1]]
print(train_data_list)
excute_cnn_train(app_config, train_data_list)
