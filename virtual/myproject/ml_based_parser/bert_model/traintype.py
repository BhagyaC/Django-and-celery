import json
import os
import random

import GPUtil
import tensorflow as tf
from bert_serving.client import ConcurrentBertClient
from tensorflow.python.estimator.canned.dnn import DNNClassifier
from tensorflow.python.estimator.run_config import RunConfig
from tensorflow.python.estimator.training import TrainSpec, EvalSpec, train_and_evaluate

os.environ['CUDA_VISIBLE_DEVICES'] = str(GPUtil.getFirstAvailable()[0])
tf.logging.set_verbosity(tf.logging.INFO)

train_fp = ['data_train.json']
eval_fp = ['data_test.json']

batch_size = 128
num_parallel_calls = 4
num_concurrent_clients = num_parallel_calls * 2  # should be at least greater than `num_parallel_calls`

bc = ConcurrentBertClient(port=5555, port_out=5556)


line_type=['header','meta','content']



def get_encodes2(x):
    # x is `batch_size` of lines, each of which is a json object
    samples = [json.loads(l) for l in x]
    text = [s['text'] for s in samples]
    features = bc.encode(text)
    
    
    type_est=[[str(s['linetype'])] for s in samples]
    return features, type_est

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
run_config = RunConfig(model_dir='./model_type/',
                       session_config=config,
                       save_checkpoints_steps=1000)


estimator2= DNNClassifier(
                          hidden_units=[512],
                          feature_columns=[tf.feature_column.numeric_column('feature', shape=(768,))],
                          n_classes=len(line_type),
                          config=run_config,
                          label_vocabulary=line_type,
                          dropout=0.1)

# Training/Evaluating:
tf.logging.set_verbosity(tf.logging.INFO)


input_fn2 = lambda fp: (tf.data.TextLineDataset(fp)
                        .apply(tf.contrib.data.shuffle_and_repeat(buffer_size=10000))
                        .batch(batch_size)
                        .map(lambda x: tf.py_func(get_encodes2, [x], [tf.float32, tf.string ], name='bert_client'),
                             num_parallel_calls=num_parallel_calls)
                        .map(lambda x, y  : ({'feature': x}, y ))
                        .prefetch(20))


train_spec2 = TrainSpec(input_fn=lambda: input_fn2(train_fp))
eval_spec2 = EvalSpec(input_fn=lambda: input_fn2(eval_fp), throttle_secs=0)


train_and_evaluate(estimator2, train_spec2, eval_spec2)
