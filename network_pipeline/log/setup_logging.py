import os
import json
import logging.config


def setup_logging(default_level=logging.INFO,
                  default_path="{}/logging.json".format(
                      os.getenv(
                          "LOG_DIR",
                          os.path.dirname(os.path.realpath(__file__)))),
                  env_key="LOG_CFG",
                  config_name=None):

    """
    Setup logging configuration
    """
    path = default_path
    file_name = default_path.split("/")[-1]
    if config_name:
        file_name = config_name

    path = "{}/{}".format(
                "/".join(default_path.split("/")[:-1]),
                file_name)

    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        return

    else:
        cwd_path = os.getcwd() + "/network_pipeline/log/{}".format(
                                    file_name)
        if os.path.exists(cwd_path):
            with open(cwd_path, "rt") as f:
                config = json.load(f)
            logging.config.dictConfig(config)
            return
        rels_path = os.getcwd() + "/../log/{}".format(
                                    file_name)
        if os.path.exists(rels_path):
            with open(rels_path, "rt") as f:
                config = json.load(f)
            logging.config.dictConfig(config)
            return
        else:
            logging.basicConfig(level=default_level)
            return
# end of setup_logging
