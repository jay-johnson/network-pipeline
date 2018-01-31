#!/usr/bin/env python

import logging
import pandas as pd
import glob
import copy
import random
from network_pipeline.consts import VALID
from network_pipeline.consts import INVALID
from network_pipeline.utils import ppj
from network_pipeline.utils import rnow
from network_pipeline.log.setup_logging import setup_logging
from celery_connectors.utils import ev


setup_logging(config_name="builders.json")
name = "builder"
log = logging.getLogger(name)
log.info("start - {}".format(name))


def find_all_headers(pipeline_files=[],
                     label_rules=None):
    log.info("find_all_headers - START")

    headers = ["src_file"]
    headers_dict = {"src_file": None}

    if label_rules:
        headers = ["src_file", "label_value", "label_name"]
        headers_dict = {"src_file": None,
                        "label_value": None,
                        "label_name": None}

    for c in pipeline_files:
        df = pd.read_csv(c)
        for h in df.columns.values:
            if h not in headers_dict:
                headers_dict[h] = "{}_{}".format(
                                    c,
                                    h)
                headers.append(h)
        # end for all headers in the file
    # end for all files to find common_headers

    log.info(("headers={}")
             .format(len(headers)))

    log.info("find_all_headers - END")
    return headers, headers_dict
# end of find_all_headers


def build_csv(
        pipeline_files=[],
        merge_file=None,
        output_file=None,
        post_proc_rules=None,
        label_rules=None,
        headers_filename="headers.json"):

    save_node = {
        "status": INVALID,
        "pipeline_files": pipeline_files,
        "post_proc_rules": post_proc_rules,
        "label_rules": label_rules,
        "merge_file": merge_file,
        "merge_header_file": None,
        "output_file": output_file,
        "output_header_file": None,
        "features_to_process": [],
        "feature_to_predict": None,
        "ignore_features": [],
        "df_json": {}
    }

    if not merge_file:
        log.error("missing merge_file - stopping")
        save_node["status"] = INVALID
        return save_node
    if not output_file:
        log.error("missing output_file - stopping")
        save_node["status"] = INVALID
        return save_node

    log.info("build_csv - START")

    common_headers, \
        headers_dict = find_all_headers(
                            pipeline_files=pipeline_files)

    log.info(("num common_headers={} headers={}")
             .format(len(common_headers),
                     common_headers))

    # since the headers can be different we rebuild a new one:

    hdrs = {}
    for h in common_headers:
        hdrs[h] = None

    features_to_process = []
    feature_to_predict = None
    ignore_features = []

    set_if_above = None
    labels = []
    label_values = []
    if label_rules:
        set_if_above = label_rules["set_if_above"]
        labels = label_rules["labels"]
        label_values = label_rules["label_values"]

    all_rows = []
    num_done = 0
    total_files = len(pipeline_files)
    for c in pipeline_files:
        log.info(("merging={}/{} csv={}")
                 .format(num_done,
                         total_files,
                         c))
        cf = pd.read_csv(c)
        log.info((" processing rows={}")
                 .format(len(cf.index)))
        for index, row in cf.iterrows():
            valid_row = True
            new_row = copy.deepcopy(hdrs)
            new_row["src_file"] = c
            for k in hdrs:
                if k in row:
                    new_row[k] = row[k]
            # end of for all headers to copy in

            if label_rules:
                test_rand = random.randint(0, 100)
                if test_rand > set_if_above:
                    new_row["label_value"] = label_values[1]
                    new_row["label_name"] = labels[1]
                else:
                    new_row["label_value"] = label_values[0]
                    new_row["label_name"] = labels[0]
            # end of applying label rules

            if valid_row:
                all_rows.append(new_row)
        # end of for all rows in this file

        num_done += 1
    # end of building all files into one list

    log.info(("merged rows={} generating df")
             .format(len(all_rows)))
    df = pd.DataFrame(all_rows)
    log.info(("df rows={} headers={}")
             .format(len(df.index),
                     df.columns.values))

    if output_file:
        log.info(("writing merge_file={}")
                 .format(merge_file))
        df.to_csv(merge_file,
                  sep=',',
                  encoding='utf-8',
                  index=False)
        log.info(("done writing merge_file={}")
                 .format(merge_file))

        merge_header_file = "{}/merge_{}".format(
            "/".join(merge_file.split("/")[:-1]),
            headers_filename)
        log.info(("dropping merge headers file={}")
                 .format(merge_header_file))
        header_data = {"headers": list(df.columns.values),
                       "output_type": "merge",
                       "pipeline_files": pipeline_files,
                       "post_proc_rules": post_proc_rules,
                       "label_rules": label_rules,
                       "created": rnow()}
        with open(merge_header_file, "w") as otfile:
            otfile.write(str(ppj(header_data)))

        save_node["merge_file"] = merge_file
        save_node["merge_header_file"] = merge_header_file

        save_node["df_json"] = df.to_json()

        if post_proc_rules:

            output_header_file = ""

            feature_to_predict = "label_name"
            features_to_process = []
            ignore_features = []
            if label_rules:
                ignore_features = [feature_to_predict]

            if "drop_columns" in post_proc_rules:
                for p in post_proc_rules["drop_columns"]:
                    if p in headers_dict:
                        ignore_features.append(p)
                # post proce filter more features out
                # for non-int/float types

                for d in df.columns.values:
                    add_this_one = True
                    for i in ignore_features:
                        if d == i:
                            add_this_one = False
                            break
                    if add_this_one:
                        features_to_process.append(d)
                # for all df columns we're not ignoring...
                # add them as features to process

                log.info(("writing DROPPED output_file={} "
                          "features_to_process={}"
                          "ignore_features={}"
                          "predict={}")
                         .format(output_file,
                                 features_to_process,
                                 ignore_features,
                                 feature_to_predict))

                df.drop(
                    columns=ignore_features
                ).to_csv(output_file,
                         header=False,
                         sep=',',
                         encoding='utf-8',
                         index=False)

                output_header_file = "{}/output_{}".format(
                    "/".join(output_file.split("/")[:-1]),
                    headers_filename)
                log.info(("dropping headers file={}")
                         .format(output_header_file))
                header_data = {"headers": list(df.columns.values),
                               "output_type": "output",
                               "pipeline_files": pipeline_files,
                               "post_proc_rules": post_proc_rules,
                               "label_rules": label_rules,
                               "features_to_process": features_to_process,
                               "feature_to_predict": feature_to_predict,
                               "ignore_features": ignore_features,
                               "created": rnow()}
                with open(output_header_file, "w") as otfile:
                    otfile.write(str(ppj(header_data)))
            else:

                for d in df.columns.values:
                    add_this_one = True
                    for i in ignore_features:
                        if d == i:
                            add_this_one = False
                            break
                    if add_this_one:
                        features_to_process.append(d)
                # for all df columns we're not ignoring...
                # add them as features to process

                log.info(("writing output_file={} "
                          "features_to_process={}"
                          "ignore_features={}"
                          "predict={}")
                         .format(output_file,
                                 features_to_process,
                                 ignore_features,
                                 feature_to_predict))

                df.to_csv(output_file,
                          header=False,
                          sep=',',
                          encoding='utf-8',
                          index=False)

                output_header_file = "{}/output_{}".format(
                    "/".join(output_file.split("/")[:-1]),
                    headers_filename)
                log.info(("dropping headers file={}")
                         .format(output_header_file))
                header_data = {"headers": list(df.columns.values),
                               "output_type": "output",
                               "pipeline_files": pipeline_files,
                               "post_proc_rules": post_proc_rules,
                               "label_rules": label_rules,
                               "features_to_process": features_to_process,
                               "feature_to_predict": feature_to_predict,
                               "ignore_features": ignore_features,
                               "created": rnow()}
                with open(output_header_file, "w") as otfile:
                    otfile.write(str(ppj(header_data)))

            # end of if/else

            save_node["output_file"] = output_file
            save_node["output_header_file"] = output_header_file

            log.info(("done writing output_file={}")
                     .format(output_file))
        # end of post_proc_rules

        save_node["status"] = VALID
    # end of writing the file

    save_node["features_to_process"] = features_to_process
    save_node["feature_to_predict"] = feature_to_predict
    save_node["ignore_features"] = ignore_features

    log.info("build_csv - END")

    return save_node
# end of build_csv


def find_all_pipeline_csvs(
        csv_glob_path="/opt/datasets/**/*.csv"):

    log.info("finding pipeline csvs in dir={}".format(csv_glob_path))

    pipeline_files = []

    for csv_file in glob.iglob(csv_glob_path,
                               recursive=True):
        log.info(("adding file={}")
                 .format(csv_file))
        pipeline_files.append(csv_file)
    # end of for all csvs

    log.info(("pipeline files={}")
             .format(len(pipeline_files)))

    return pipeline_files
# end of find_all_pipeline_csvs


output_dir = ev(
                "OUTPUT_DIR",
                "/tmp")
output_file = ev(
                "OUTPUT_FILE",
                "{}/only_attack_scans.csv".format(
                    output_dir))
merge_file = ev(
                "MERGE_FILE",
                "{}/merge_only_attack_scans.csv".format(
                    output_dir))
dataset_dir = ev(
                "DS_DIR",
                "/opt/datasets")
csv_glob_path = ev(
                "DS_GLOB_PATH",
                "{}/*/*.csv".format(
                    dataset_dir))

pipeline_files = find_all_pipeline_csvs(
                    csv_glob_path=csv_glob_path)

post_proc_rules = {
    "drop_columns": [
        "src_file",
        "raw_id",
        "raw_load",
        "raw_hex_load",
        "raw_hex_field_load",
        "pad_load"
    ],
    "predict_feature": "label_name"
}

label_rules = {
    "set_if_above": 85,
    "labels": ["not_attack", "attack"],
    "label_values": [0, 1]
}

log.info("building csv")

save_node = build_csv(
    pipeline_files=pipeline_files,
    merge_file=merge_file,
    output_file=output_file,
    post_proc_rules=post_proc_rules,
    label_rules=label_rules)

if save_node["status"] == VALID:
    log.info("Successfully process datasets:")

    if ev("SHOW_SUMMARY",
          "1") == "1":
        log.info(("Merge csv: {}")
                 .format(save_node["merge_file"]))
        log.info(("Merge headers: {}")
                 .format(save_node["merge_header_file"]))
        log.info(("Output csv: {}")
                 .format(save_node["output_file"]))
        log.info(("Output headers: {}")
                 .format(save_node["output_header_file"]))
        log.info("------------------------------------------")
        log.info(("Predicting Feature: {}")
                 .format(save_node["feature_to_predict"]))
        log.info(("Features to Process: {}")
                 .format(ppj(save_node["features_to_process"])))
        log.info(("Ignored Features: {}")
                 .format(ppj(save_node["ignore_features"])))
        log.info("------------------------------------------")
    # end of show summary

    log.info("")
    log.info("done saving csv:")
    log.info("{}".format(save_node["merge_file"]))
    log.info("")
else:
    log.info("Failed to process datasets")
# end if/else
