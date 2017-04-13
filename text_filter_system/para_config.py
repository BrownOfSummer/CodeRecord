
class Config(object):
    # Model Hyperparameters
    embedding_dim = 128
    filter_sizes = "3,4,5"
    num_filters = 128
    dropout_keep_prob = 0.5

    # Training Parameters
    batch_size = 64
    evaluate_every = 100
    checkpoint_every = 100
    num_checkpoints = 1
    num_epochs = 10
    right_weight = 10.0
    l2_reg_lambda = 10.0
    allow_soft_placement = True
    log_device_placement = False
    max_document_length = 64

    max_vocab_keep = 100000
