from filter_common import *
from search_train_data import *
app_config = {"DATA_DIR":"/tmp/data_dir/", 
        "MODEL_DIR":"/tmp/model_dir/"}

query_record = {"id":"84e3374c-a8d6-11de-a71c-0024e869955c",
        "text":"Modern Family - Season 8 Episode 10 Ringmaster Keifth"}

#Modern Family - Season 8 Episode 10 "Ringmaster Keifth"
#84e3374c-a8d6-11de-a71c-0024e869955c MF - A NESTING, VERY MATERNAL...PRIMAL THING, WHERE IT RETAINS NUTRIENTS 2/2 ;)
#American Dad The Episodes Begin To The End || New American Dad Episodes 2016
result, prob = query_cnnfilter(app_config, query_record)
print(result, prob)
