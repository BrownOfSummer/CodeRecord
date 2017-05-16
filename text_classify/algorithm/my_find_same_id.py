from sumit_training_data import *
"""Get same ids"""
positive_data_file="./data/new_right.txt"
positive_examples = list(open(positive_data_file, "r").readlines())
positive_ids = [s.strip().split('\t')[0] for s in positive_examples[1:]]
pos_id_dicts={}
for pos_id in positive_ids:
    if pos_id in pos_id_dicts:
        pos_id_dicts[pos_id] += 1
    else:
        pos_id_dicts[pos_id] = 1
print("pos data ids:",len(pos_id_dicts))
#sorted(pos_id_dicts.items(),key=lambda d:d[1])
#print(pos_id_dicts)

negative_data_file="./data/new_wrong.txt"
negative_examples = list(open(negative_data_file, "r").readlines())
negative_ids=[s.strip().split('\t')[0] for s in negative_examples[1:]]
neg_id_dicts={}
for neg_id in negative_ids:
    if neg_id in neg_id_dicts:
        neg_id_dicts[neg_id] += 1
    else:
        neg_id_dicts[neg_id] = 1
print("neg data ids:", len(neg_id_dicts))

count = 0
for pos_id in pos_id_dicts:
    if pos_id in neg_id_dicts:
        print("{} -> pos:{}; neg:{}".format(pos_id, pos_id_dicts[pos_id], neg_id_dicts[pos_id]))
        count += 1
print("total {} same ids".format(count))
