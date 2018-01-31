#!/usr/bin/env python

import os
import sys
import logging
import json
import numpy as np
import pandas as pd
from celery_connectors.utils import ev
from network_pipeline.log.setup_logging import setup_logging
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split


setup_logging(config_name="modelers.json")
name = "keras-dnn"
log = logging.getLogger(name)
log.info("start - {}".format(name))


# seed for reproducing same results
seed = 9
np.random.seed(seed)

csv_file = ev(
    "CSV_FILE",
    "/tmp/merge_only_attack_scans.csv")
meta_file = ev(
    "CSV_META_FILE",
    "/tmp/merge_headers.json")

if not os.path.exists(csv_file):
    log.error(("missing csv_file={}")
              .format(csv_file))
    sys.exit(1)

predict_feature = ev(
    "PREDICT_FEATURE",
    "label_value")

log.info(("Loading csv={}")
         .format(csv_file))

# load csv file into pandas dataframe
df = pd.read_csv(csv_file)

# set up the test to train ratio
test_size = float(ev(
    "TEST_SIZE",
    "0.20"))
train_size = 1.0 - test_size

feature_to_process = []
ignore_features = [
    "label_name",
    "ip_src",   # need to make this an int
    "ip_dst",   # need to make this an int
    "eth_src",  # need to make this an int
    "eth_dst"   # need to make this an int
]
meta_data = {}

try:
    meta_data = json.loads(
        open(meta_file, "r").read()
    )
    if "post_proc_rules" in meta_data:
        if "drop_columns" in meta_data["post_proc_rules"]:
            for ign in meta_data["post_proc_rules"]["drop_columns"]:
                ignore_features.append(ign)
except Exception as e:
    log.error(("Failed building ignore_features: "
               "ignore_features={} meta={} meta_data={} "
               "ex={}")
              .format(ignore_features,
                      meta_file,
                      meta_data,
                      e))
# end of trying to lookup the meta data file
# for non-int/float features to ignore

for feature in df.columns.values:
    keep_it = True
    for ign in ignore_features:
        if feature == ign:
            keep_it = False
    if keep_it:
        feature_to_process.append(feature)
# end of for all features to process

log.info(("Predicting={} with features={} "
          "ignore_features={} records={}")
         .format(predict_feature,
                 feature_to_process,
                 ignore_features,
                 len(df.index)))

# split the data into training
(X_train, X_test, Y_train, Y_test) = \
        train_test_split(df[feature_to_process],
                         df[predict_feature],
                         test_size=test_size,
                         random_state=seed)

log.info(("splitting rows={} into "
          "X_train={} X_test={}"
          "Y_train={} Y_test={}")
         .format(len(df.index),
                 len(X_train),
                 len(X_test),
                 len(Y_train),
                 len(Y_test)))

log.info("creating sequential model")

# create the model
model = Sequential()
model.add(Dense(8,
                input_dim=len(feature_to_process),
                kernel_initializer="uniform",
                activation="relu"))
model.add(Dense(6,
                kernel_initializer="uniform",
                activation="relu"))
model.add(Dense(1,
                kernel_initializer="uniform",
                activation="sigmoid"))

log.info("compiling model")

# compile the model
model.compile(loss="binary_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

log.info("fitting model - please wait")

# fit the model
model.fit(X_train,
          Y_train,
          validation_data=(X_test, Y_test),
          epochs=200,
          batch_size=5,
          verbose=0)

# evaluate the model
scores = model.evaluate(X_test, Y_test)
log.info(("Accuracy: {}")
         .format(scores[1] * 100))
