import os
import json
import numpy as np
import pandas as pd
from celery_connectors.utils import ev
from network_pipeline.log.setup_logging import build_colorized_logger
from network_pipeline.consts import VALID
from network_pipeline.consts import INVALID
from network_pipeline.consts import ERROR
from sklearn.model_selection import train_test_split


name = "training-utils"
log = build_colorized_logger(name=name)


def build_training_request(
        csv_file=ev(
            "CSV_FILE",
            "/tmp/cleaned_attack_scans.csv"),
        meta_file=ev(
            "CSV_META_FILE",
            "/tmp/cleaned_metadata.json"),
        predict_feature=ev(
            "PREDICT_FEATURE",
            "label_value"),
        ignore_features=[
            "label_name",
            "ip_src",   # need to make this an int
            "ip_dst",   # need to make this an int
            "eth_src",  # need to make this an int
            "eth_dst"   # need to make this an int
        ],
        seed=None,
        test_size=float(ev(
            "TEST_SIZE",
            "0.20")),
        preproc_rules=None):
    """build_training_request

    :param csv_file: csv file built with prepare-dataset.py
    :param meta_file: metadata file built with prepare-dataset.py
    :param predict_feature: feature (column) to predict
    :param ignore_features: features to remove from the csv
                            before the split of test + train
                            data
    :param seed: integer to seed
    :param test_size: percent of records to split into test
                      vs train
    :param preproc_rules: future preprocessing rules hooks
    """

    last_step = "not started"
    res = {
        "status": INVALID,
        "err": "",
        "csv_file": csv_file,
        "meta_file": meta_file,
        "meta_data": None,
        "seed": None,
        "test_size": test_size,
        "predict_feature": predict_feature,
        "features_to_process": [],
        "ignore_features": ignore_features,
        "X_train": None,
        "X_test": None,
        "Y_train": None,
        "Y_test": None
    }

    try:

        last_step = ("building seed={}").format(
                        seed)

        log.debug(last_step)

        use_seed = seed
        if not use_seed:
            use_seed = 9

        res["seed"] = np.random.seed(use_seed)

        last_step = ("Loading csv={}").format(
                        csv_file)

        log.info(last_step)

        if not os.path.exists(csv_file):
            res["status"] = ERROR
            res["err"] = ("Unable to find csv_file={}").format(
                            csv_file)
            log.error(res["err"])
            return res
        # end of checking for a valid csv file on disk

        if not os.path.exists(meta_file):
            res["status"] = ERROR
            res["err"] = ("Unable to find meta_file={}").format(
                            meta_file)
            log.error(res["err"])
            return res
        # end of checking for a valid metadata file on disk

        # load csv file into pandas dataframe
        df = pd.read_csv(csv_file)

        features_to_process = []
        meta_data = {}

        try:
            last_step = ("opening metadata={}").format(
                            meta_file)
            log.debug(last_step)
            meta_data = json.loads(
                open(meta_file, "r").read()
            )
            res["meta_data"] = meta_data
            if "post_proc_rules" in meta_data:
                if "drop_columns" in meta_data["post_proc_rules"]:
                    log.debug(("Found drop_columns={}")
                              .format(
                                meta_data["post_proc_rules"]["drop_columns"]
                              ))
                    for ign in meta_data["post_proc_rules"]["drop_columns"]:
                        ignore_features.append(ign)
        except Exception as e:
            res["error"] = ("Failed building ignore_features: "
                            "ignore_features={} meta={} meta_data={} "
                            "last_step='{}' ex='{}'").format(
                                ignore_features,
                                meta_file,
                                meta_data,
                                last_step,
                                e)
            log.error(res["error"])
            res["status"] = ERROR
            return res
        # end of trying to lookup the meta data file
        # for non-int/float features to ignore

        last_step = ("metadata={} df has "
                     "columns={} ignore={}").format(
                        meta_file,
                        df.columns.values,
                        ignore_features)

        log.info(last_step)

        for feature in df.columns.values:
            keep_it = True
            for ign in ignore_features:
                if feature == ign:
                    keep_it = False
            if keep_it:
                if feature != predict_feature:
                    features_to_process.append(feature)
        # end of for all features to process

        last_step = ("Done post-procecessing "
                     "Predicting={} with features={} "
                     "ignore_features={} records={}").format(
                        predict_feature,
                        features_to_process,
                        ignore_features,
                        len(df.index))

        log.info(last_step)

        res["predict_feature"] = predict_feature

        res["ignore_features"] = []
        for k in ignore_features:
            if k not in res["ignore_features"]:
                res["ignore_features"].append(k)
        res["features_to_process"] = []
        for k in features_to_process:
            if k not in res["features_to_process"]:
                if k != predict_feature:
                    res["features_to_process"].append(k)

        # split the data into training
        (res["X_train"],
         res["X_test"],
         res["Y_train"],
         res["Y_test"]) = train_test_split(
                            df[features_to_process],
                            df[predict_feature],
                            test_size=test_size,
                            random_state=res["seed"])

        last_step = ("Done splitting rows={} into "
                     "X_train={} X_test={} "
                     "Y_train={} Y_test={}").format(
                        len(df.index),
                        len(res["X_train"]),
                        len(res["X_test"]),
                        len(res["Y_train"]),
                        len(res["Y_test"]))

        log.info(("Success: {}")
                 .format(last_step))

        res["err"] = ""
        res["status"] = VALID
    except Exception as e:
        res["status"] = ERROR
        res["err"] = ("Failed build_training_request "
                      "step='{}' with ex='{}'").format(
                        last_step,
                        e)
        log.error(("build_training_request: {}")
                  .format(res["err"]))
    # end of try/ex

    return res
# end of build_training_request
