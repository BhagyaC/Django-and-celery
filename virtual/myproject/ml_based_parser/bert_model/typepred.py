import json
import logging
import os
# import random
import pandas as pd

# import GPUtil
import tensorflow as tf
from bert_serving.client import ConcurrentBertClient
from tensorflow.python.estimator.canned.dnn import DNNClassifier
from tensorflow.python.estimator.run_config import RunConfig
# from tensorflow.python.estimator.training import TrainSpec, EvalSpec, train_and_evaluate

# os.environ['CUDA_VISIBLE_DEVICES'] = str(GPUtil.getFirstAvailable()[0])
tf.logging.set_verbosity(tf.logging.INFO)
logger = logging.getLogger(__name__)

if tf.test.is_gpu_available:
    logger.info('No GPU available. Using CPU for execution')
else:
    logger.info('GPU available.')

logger.info('Initialize bert client for LINE TYPE')
bc = ConcurrentBertClient(ip=os.getenv('BERT_SVC_URL', 'bertservice'), port=5555, port_out=5556)
logger.info('Initialize bert client for LINE TYPE completed')


def get_encodes1(x):
    global result
    # x is `batch_size` of lines, each of which is a json object
    samples = [json.loads(l) for l in x]
    text = [s['text'] for s in samples]
    features = bc.encode(text)
    labels = [[str(s['linelabel'])] for s in samples]
    result = text
    # logger.debug(type(result))
    # logger.debug("features--encoded {}".format(result))
    # logger.debug("corresponding--labels {}".format(labels))
    return features, labels


def predict_type(json_input: json) -> pd.DataFrame:
    """
    Predict line type from resume.
    :param json_input: JSON representation of lines in resume.
    :return:
    """
    logger.info('Predicting LINE TYPE...')
    # train_fp = ['data_train.json']
    # eval_fp = ['bertinput.json']

    batch_size = 128
    num_parallel_calls = 4

    num_concurrent_clients = num_parallel_calls * 2  # should be at least greater than `num_parallel_calls`

    line_labels = ['header', 'meta', 'content']
    model_dir = './ml_based_parser/bert_model/model_type/'

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    run_config = RunConfig(model_dir=model_dir,
                           session_config=config,
                           save_checkpoints_steps=None)

    estimator1 = DNNClassifier(
        hidden_units=[512],
        feature_columns=[tf.feature_column.numeric_column('feature', shape=(768,))],
        n_classes=len(line_labels),
        config=run_config,
        label_vocabulary=line_labels,
        dropout=0.1)

    # Transform text into encoding
    input_fn = lambda fp: (tf.data.Dataset.from_tensor_slices(fp)
                           .batch(batch_size)
                           .map(lambda x: tf.py_func(get_encodes1, [x], [tf.float32, tf.string], name='bert_client'),
                                num_parallel_calls=num_parallel_calls)
                           .map(lambda x, y: ({'feature': x}, y))
                           .prefetch(20))

    result1 = list(estimator1.predict(
        input_fn=lambda: input_fn(json_input),
        predict_keys=None,
        hooks=None,
        checkpoint_path=None,
        yield_single_examples=True
    ))

    # logger.debug("***********************resulkt size".format(len(result)))
    predicted_classes1 = [p["classes"] for p in result1]
    # logger.debug("length".format(len(predicted_classes1)))

    # logger.debug("New Samples, Class Predictions: {}\n".format(predicted_classes1))

    # logger.debug(predicted_classes1)
    df = pd.DataFrame(dict({"features": result, "prediction": predicted_classes1}))
    # df.to_csv("typepredicted15.csv", index=False)
    return df
