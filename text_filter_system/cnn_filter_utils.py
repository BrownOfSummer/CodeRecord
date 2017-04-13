# -*- coding=utf8 -*-
import os
import numpy as np
import time
from datetime import datetime
import traceback

import data_helpers
import tensorflow as tf
from text_cnn import TextCNN
from tensorflow.contrib import learn
from tensorflow.python.platform import gfile
from para_config import Config as config_

from tqdm import tqdm

def split_text(path_untrain_r, path_untrain_w):
    """
    Para: files from submit
    path_untrain_r: the positive_data_file
    path_untrain_w: the negative_data_file
    append never_trained file, and generate file for train
    """
    dir_for_right = os.path.dirname(path_untrain_r)
    dir_for_wrong = os.path.dirname(path_untrain_w)
    #assert os.path.exists(dir_for_right) and os.path.exists(dir_for_wrong)
    r_raw = np.array(open(path_untrain_r, "r").readlines())
    w_raw = np.array(open(path_untrain_w, "r").readlines())
    r_len = len(r_raw)
    w_len = len(w_raw)
    if r_len < w_len:
        shuffle_indices = np.random.permutation(np.arange(w_len))
        w_raw = w_raw[shuffle_indices]
        never_trained_w = w_raw[r_len:]
        w_raw = w_raw[:r_len]
        # Save to never_trained file
        time_filename = datetime.now().strftime('%Y%m%d%H%M%S%f')
        never_trained_path = os.path.join(dir_for_wrong, time_filename + ".never_trained")
        with open(never_trained_path, "a") as fp:
            for line in never_trained_w:
                fp.write("%s\n" % line.strip())
    else:
        # No need to cut the wrong data
        pass
    # Write to file training
    path_for_training_r = os.path.join(dir_for_right, "training")
    with open(path_for_training_r, "w") as fp:
        for line in r_raw:
            fp.write("%s\n" % line.strip())
    path_for_training_w = os.path.join(dir_for_wrong, "training")
    with open(path_for_training_w, "w") as fp:
        for line in w_raw:
            fp.write("%s\n" % line.strip())

def generate_vocab(path_untrain_r, path_untrain_w):
    VOCAB_DIR = os.path.join(os.path.dirname(path_untrain_r),"..")
    assert os.path.exists(VOCAB_DIR)
    x_r, x_w, _, _ = data_helpers.load_data_and_labels(path_untrain_r, path_untrain_w)
    vocab_processor = learn.preprocessing.VocabularyProcessor(config_.max_document_length)
    vocab_processor.fit_transform(x_r + x_w)
    # Write vocabulary
    vocab_processor.save(os.path.join(VOCAB_DIR, "vocab"))

def append_vocab(model_dir, path_untrain_r, path_untrain_w):
    """
    Load the vocab and append the vocab
    Paras:
    path_untrain_r, path_untrain_w: submit untrain
    model_dir:  model_dir/vocab
    """
    assert os.path.exists(path_untrain_r) and os.path.exists(path_untrain_w)
    VOCAB_DIR = model_dir
    x_train_r, x_train_w, y_train_r, y_train_w = data_helpers.load_data_and_labels(
            path_untrain_r, path_untrain_w)
    # Restore dictionary
    print("Restoring and add new word to vocab...")
    vocab_path = os.path.join(VOCAB_DIR, "vocab")
    try:
        assert os.path.exists(vocab_path)
        vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
        vocab_processor.vocabulary_.freeze(False)
        vocab_processor.fit(x_train_r + x_train_w)
        if len(vocab_processor.vocabulary_) < config_.max_vocab_keep:
            vocab_processor.save(vocab_path)
            print("dict_lenght:",len(vocab_processor.vocabulary_))
        else:
            print("Warning, new words Failed to append in order not to be out of range the embedding\n")
    except Exception as e:
        print("Failed to append vocab")
        traceback.print_exc()

def get_checkpoint_file(MODEL_DIR):
    checkpoint_dir = os.path.join(MODEL_DIR,"runs/checkpoints/")
    assert os.path.exists(checkpoint_dir)
    try:
        # If the path unchanged
        checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir)
        #save_step = checkpoint_file.split('/')[-1].split('-')[-1]
        print('checkpoint_file:',checkpoint_file)
        return checkpoint_file
    except:
        # If the checkpoint path changed
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        if ckpt and ckpt.model_checkpoint_path:
            latest_checkpoint = ckpt.model_checkpoint_path.split('/')[-1]
            #save_step = latest_checkpoint.split('-')[-1] # 1350
            checkpoint_file = os.path.join(checkpoint_dir, latest_checkpoint) # path + model-1350
            print('checkpoint_file:',checkpoint_file)
            return checkpoint_file
        else:
            print('No checkpoint file found!')
            return None
        
def cnn_train(training_r, training_w):
    assert os.path.exists(training_r) and os.path.exists(training_w)
    VOCAB_DIR = os.path.join(os.path.dirname(training_r),"..")
    MODEL_DIR = os.path.join(os.path.dirname(training_r),"..","runs")
    print("Loading data...")
    x_train_r, x_train_w, y_train_r, y_train_w = data_helpers.load_data_and_labels(
            training_r, training_w)
    # Restore dictionary
    print("Restoring vocab...")
    vocab_path = os.path.join(VOCAB_DIR, "vocab")
    try:
        assert os.path.exists(vocab_path)
        vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
        print("vocab_lenght:", len(vocab_processor.vocabulary_))
    except Exception as e:
        print("Failed to restore vocab")
        traceback.print_exc()

    print("PreProcessing data...")
    # Map words to int vector
    x_train_r = np.array(list(vocab_processor.transform(x_train_r)))
    y_train_r = np.array(y_train_r)
    x_train_w = np.array(list(vocab_processor.transform(x_train_w)))
    y_train_w = np.array(y_train_w)
    print("Positive/Negative {:d}/{:d}".format(len(y_train_r), len(y_train_w)))
    
    # Add priority for right data
    y_train_r = y_train_r * config_.right_weight # multiply the weight of the right data
    # Training data
    x_train = np.array(list(x_train_r) + list(x_train_w))
    y_train = np.array(list(y_train_r) + list(y_train_w))

    # Training
    # ==================================================
    print("Start training...")
    start_train = time.time()
    with tf.Graph().as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=config_.allow_soft_placement,
          log_device_placement=config_.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            cnn = TextCNN(
                sequence_length=x_train_r.shape[1],
                num_classes=y_train_r.shape[1],
                vocab_size=max(config_.max_vocab_keep, len(vocab_processor.vocabulary_)),
                embedding_size=config_.embedding_dim,
                filter_sizes=list(map(int, config_.filter_sizes.split(","))),
                num_filters=config_.num_filters,
                l2_reg_lambda=config_.l2_reg_lambda)

            # Define Training procedure
            global_step = tf.Variable(0, name="global_step", trainable=False)
            optimizer = tf.train.AdamOptimizer(1e-3)
            grads_and_vars = optimizer.compute_gradients(cnn.loss)
            train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)
            tf.add_to_collection('train_op', train_op)

            # Output directory for models and summaries
            out_dir = os.path.abspath(MODEL_DIR)
            #if os.path.exists(out_dir):
            #    gfile.DeleteRecursively(out_dir)
            print("Writing to {}\n".format(out_dir))

            # Summaries for loss and accuracy
            loss_summary = tf.summary.scalar("loss", cnn.loss)
            acc_summary = tf.summary.scalar("accuracy", cnn.accuracy)

            # Train Summaries
            train_summary_op = tf.summary.merge([loss_summary, acc_summary])
            train_summary_dir = os.path.join(out_dir, "summaries", "train")
            train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)
            
            # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
            checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
            checkpoint_prefix = os.path.join(checkpoint_dir, "model")
            if not os.path.exists(checkpoint_dir):
                os.makedirs(checkpoint_dir)
            saver = tf.train.Saver(tf.global_variables(), max_to_keep=config_.num_checkpoints)
            # Write vocabulary
            #vocab_processor.save(os.path.join(out_dir, "vocab"))

            # Initialize all variables
            sess.run(tf.global_variables_initializer())

            def train_step(x_batch, y_batch):
                """
                A single training step
                """
                feed_dict = {
                  cnn.input_x: x_batch,
                  cnn.input_y: y_batch,
                  cnn.dropout_keep_prob: config_.dropout_keep_prob,
                }
                _, step, summaries, loss, accuracy = sess.run(
                    [train_op, global_step, train_summary_op, cnn.loss, cnn.accuracy],
                    feed_dict)
                time_str = datetime.now().isoformat()
                print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
                train_summary_writer.add_summary(summaries, step)
            
            # Generate batches
            batches = data_helpers.batch_iter(
                    list(zip(x_train, y_train)), config_.batch_size, config_.num_epochs)
            # Training loop. For each batch...
            for batch in batches:
                x_batch, y_batch = zip(*batch)
                train_step(x_batch, y_batch)
                current_step = tf.train.global_step(sess, global_step)
                if current_step % config_.checkpoint_every == 0:
                    path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                    print("Saved model checkpoint to {}\n".format(path))
    end_train = time.time()
    print('Train costs', end_train - start_train)


def cnn_retrain(model_dir, training_r, training_w):
    """
    Load the model and retrain the network with new data
    Paras:
    training_r, training_w: spliting from submit untrain
    model_dir: model_dir/runs, model_dir/vocab
    """
    start_retrain = time.time()
    assert os.path.exists(training_r) and os.path.exists(training_w)
    VOCAB_DIR = model_dir
    MODEL_DIR = model_dir
    print("Loading data...")
    x_train_r, x_train_w, y_train_r, y_train_w = data_helpers.load_data_and_labels(
            training_r, training_w)
    # Restore dictionary
    print("Restoring word to vocab...")
    vocab_path = os.path.join(VOCAB_DIR, "vocab")
    try:
        assert os.path.exists(vocab_path)
        vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
        #vocab_processor.vocabulary_.freeze(False)
        #vocab_processor.fit(x_train_r + x_train_w)
        #if len(vocab_processor.vocabulary_) > config_.max_vocab_keep:
        #    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    except Exception as e:
        print("Failed to restore vocab")
        traceback.print_exc()

    print("PreProcessing data...")
    # Map words to int vector
    x_train_r = np.array(list(vocab_processor.transform(x_train_r)))
    y_train_r = np.array(y_train_r)
    x_train_w = np.array(list(vocab_processor.transform(x_train_w)))
    y_train_w = np.array(y_train_w)
    print("Positive/Negative {:d}/{:d}".format(len(y_train_r), len(y_train_w)))
    
    # Add priority for right data
    y_train_r = y_train_r * config_.right_weight # multiply the weight of the right data
    # Training data
    x_train = np.array(list(x_train_r) + list(x_train_w))
    y_train = np.array(list(y_train_r) + list(y_train_w))

    print("Get checkpoint_file...")
    checkpoint_file = get_checkpoint_file(MODEL_DIR)

    # Training
    # ==================================================
    print("Start training...")
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=config_.allow_soft_placement,
          log_device_placement=config_.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file)) # load model-1350-meta
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to retrain
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]
            loss = graph.get_operation_by_name("loss/loss").outputs[0]
            accuracy = graph.get_operation_by_name("accuracy/accuracy").outputs[0]
            global_step = graph.get_operation_by_name("global_step").outputs[0]
            #print(global_step, sess.run(global_step))
            save_step = sess.run(global_step)

            # Get the train_op
            train_op = tf.get_collection('train_op')[0]

            # Define the one train operation
            def train_step(x_batch, y_batch):
                """
                A single training step
                """
                feed_dict = {
                  input_x: x_batch,
                  input_y: y_batch,
                  dropout_keep_prob: config_.dropout_keep_prob,
                }
                _, step, summaries, batch_loss, batch_accuracy = sess.run(
                    [train_op, global_step, train_summary_op, loss, accuracy],
                    feed_dict)
                time_str = datetime.now().isoformat()
                print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, batch_loss, batch_accuracy))
                train_summary_writer.add_summary(summaries, step)

            # Collect the predictions here
            all_predictions = []
            # Output directory for models and summaries
            out_dir = os.path.join(MODEL_DIR,"runs")

            print("Writing to {}\n".format(out_dir))
            # Summaries for loss and accuracy
            loss_summary = tf.summary.scalar("loss", loss)
            acc_summary = tf.summary.scalar("accuracy", accuracy)
            # Train Summaries
            train_summary_op = tf.summary.merge([loss_summary, acc_summary])
            train_summary_dir = os.path.join(out_dir, "summaries", "train")
            train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)

            # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
            checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
            checkpoint_prefix = os.path.join(checkpoint_dir, "model")
            if not os.path.exists(checkpoint_dir):
                os.makedirs(checkpoint_dir)
            saver = tf.train.Saver(tf.global_variables(), max_to_keep=config_.num_checkpoints)

            # Write vocabulary
            #vocab_processor.save(os.path.join(VOCAB_DIR, "vocab"))

            # Generate batches for one epoch
            batches = data_helpers.batch_iter(list(zip(x_train, y_train)), config_.batch_size, config_.num_epochs, shuffle=True)
            for batch in batches:
                x_batch, y_batch = zip(*batch)
                train_step(x_batch, y_batch)
                current_step = tf.train.global_step(sess, global_step)
                if (current_step - int(save_step)) % config_.checkpoint_every == 0:
                    path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                    print("Saved model checkpoint to {}\n".format(path))
            
            # Delete the last model
            os.remove("{}.data-00000-of-00001".format(checkpoint_file))
            os.remove("{}.index".format(checkpoint_file))
            os.remove("{}.meta".format(checkpoint_file))
        # Need to write the raw data to trained
    end_retrain = time.time()
    print("retrain_time:", end_retrain - start_retrain)

def cnn_query(model_dir, query_file_path):
    """
    Query the new data file, return predictions and probability
    model_dir: model_dir/runs, model_dir/vocab
    query_file_path: test file
    """
    start_eval = time.time()
    x_raw = data_helpers.load_data_and_labels_for_eval(query_file_path)
    # Map data into vocabulary
    VOCAB_DIR = model_dir
    vocab_path = os.path.join(VOCAB_DIR,"vocab")
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    x_test = np.array(list(vocab_processor.transform(x_raw)))

    # Evaluation
    """Get the checkpoint file"""
    checkpoint_file = get_checkpoint_file(model_dir)
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file)) # load model-1350-meta
            saver.restore(sess, checkpoint_file)
            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]
            probability = graph.get_operation_by_name("output/probability").outputs[0]
            # Generate batches for one epoch
            batches = data_helpers.batch_iter(list(x_test), config_.batch_size, 1, shuffle=False)
            # Collect the predictions here
            count_right = 0
            count_wrong = 0
            for x_test_batch in tqdm(batches):
                batch_predictions, batch_probability = sess.run([predictions, probability],{input_x: x_test_batch, dropout_keep_prob: 1.0})
                for i in np.arange(len(batch_predictions)):
                    if batch_predictions[i] > 0:
                        #print("result:{}, prob:{}".format("TRUE", batch_probability[i][1]))
                        count_right += 1
                    else:
                        #print("result:{}, prob:{}".format("FALSE", batch_probability[i][0]))
                        count_wrong += 1
    eval_time = time.time() - start_eval
    print("query time:",eval_time)
    print("count_right, count_wrong", count_right, count_wrong)
