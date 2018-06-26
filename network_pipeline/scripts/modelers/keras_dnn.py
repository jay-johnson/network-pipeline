#!/usr/bin/env python

import os
import sys
from spylunking.log.setup_logging import console_logger
from celery_connectors.utils import ev
from network_pipeline.consts import VALID
from network_pipeline.build_training_request import build_training_request
from keras.models import Sequential
from keras.layers import Dense


name = 'keras-dnn'
log = console_logger(
    name=name)


log.info("start - {}".format(name))


def build_new_deep_neural_network_from_env_variables():
    """build_new_deep_neural_network_from_env_variables

    Build a new deep neural network from environment variables:

    ``CSV_FILE`` - file to process created during prepare dataset
    ``CSV_META_FILE`` - metadata header file created during prepare dataset
    ``PREDICT_FEATURE`` - column to predict
    ``TEST_SIZE`` - split data into percentage of test to training
    """

    csv_file = ev(
        "CSV_FILE",
        "/tmp/cleaned_attack_scans.csv")
    meta_file = ev(
        "CSV_META_FILE",
        "/tmp/cleaned_metadata.json")
    predict_feature = ev(
        "PREDICT_FEATURE",
        "label_value")
    test_size = float(ev(
        "TEST_SIZE",
        "0.20"))

    if not os.path.exists(csv_file):
        log.error(("missing csv_file={}")
                  .format(csv_file))
        sys.exit(1)

    res = build_training_request(
            csv_file=csv_file,
            meta_file=meta_file,
            predict_feature=predict_feature,
            test_size=test_size)

    if res["status"] != VALID:
        log.error(("Stopping for status={} "
                   "errors: {}")
                  .format(
                    res["status"],
                    res["err"]))
        sys.exit(1)
    else:
        log.info(("built_training_request={} "
                  "features={} ignore={}")
                 .format(
                    res["status"],
                    res["features_to_process"],
                    res["ignore_features"]))
    # end of validating the training request

    log.info("ready for training")

    log.info("creating Keras - sequential model")

    # create the model
    model = Sequential()
    model.add(Dense(8,
                    input_dim=len(res["features_to_process"]),
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
    model.compile(
        loss="binary_crossentropy",
        optimizer="adam",
        metrics=["accuracy"])

    log.info("fitting model - please wait")

    # fit the model
    model.fit(
        res["X_train"],
        res["Y_train"],
        validation_data=(res["X_test"],
                         res["Y_test"]),
        epochs=50,
        batch_size=2,
        verbose=1)

    # evaluate the model
    scores = model.evaluate(
        res["X_test"],
        res["Y_test"])

    log.info(("Accuracy: {}")
             .format(
                scores[1] * 100))

# end of build_new_deep_neural_network_from_env_variables


if __name__ == "__main__":
    build_new_deep_neural_network_from_env_variables()
