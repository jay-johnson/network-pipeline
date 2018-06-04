Prepare Dataset
===============

This is a guide for building training datasets from the recorded csvs in the `network pipeline datasets`_ repository. Once a dataset is prepared locally, you can use the `modelers`_ to build and tune machine learning and AI models.

.. _network pipeline datasets: https://github.com/jay-johnson/network-pipeline-datasets
.. _modelers: https://github.com/jay-johnson/network-pipeline/network_pipeline/scripts/modelers

Install
-------

This will make sure your virtual environment is using the latest ``pandas`` pip and install the latest ML/AI pips. Please run it from the repository's base directory.

::

    source /tmp/netpipevenv/bin/activate
    pip install --upgrade -r ./network_pipeline/scripts/builders/requirements.txt

Overview
========

I have not uploaded a local recording from my development stacks, so for now this will prepare a training dataset by randomly applying ``non-attack - 0`` and ``attack - 1`` labels for flagging records as **attack** and **non-attack** records.

Setup 
=====

Please export the path to the datasets repository on your host:

::

    export DS_DIR=<path_to_datasets_base_directory>

Or clone the repository to the default value for the environment variable (``DS_DIR=/opt/antinex/datasets``) with:

::

    mkdir -p -m 777 /opt/antinex
    git clone https://github.com/jay-johnson/network-pipeline-datasets.git /opt/antinex/datasets

Build Dataset
=============

This will take a few moments to prepare the csv files.

::

    prepare_dataset.py
    2018-01-31 23:38:04,298 - builder - INFO - start - builder
    2018-01-31 23:38:04,298 - builder - INFO - finding pipeline csvs in dir=/opt/antinex/datasets/*/*.csv
    2018-01-31 23:38:04,299 - builder - INFO - adding file=/opt/antinex/datasets/react-redux/netdata-2018-01-29-13-36-35.csv
    2018-01-31 23:38:04,299 - builder - INFO - adding file=/opt/antinex/datasets/spring/netdata-2018-01-29-15-00-12.csv
    2018-01-31 23:38:04,299 - builder - INFO - adding file=/opt/antinex/datasets/vue/netdata-2018-01-29-14-12-44.csv
    2018-01-31 23:38:04,299 - builder - INFO - adding file=/opt/antinex/datasets/django/netdata-2018-01-28-23-12-13.csv
    2018-01-31 23:38:04,299 - builder - INFO - adding file=/opt/antinex/datasets/django/netdata-2018-01-28-23-06-05.csv
    2018-01-31 23:38:04,299 - builder - INFO - adding file=/opt/antinex/datasets/flask-restplus/netdata-2018-01-29-11-30-02.csv

Verify Dataset and Tracking Files
=================================

By default the environment variable ``OUTPUT_DIR`` writes the dataset csv files to ``/tmp``:

::

    ls -lrth /tmp/*.csv
    -rw-rw-r-- 1 jay jay  26M Jan 31 23:38 /tmp/fulldata_attack_scans.csv
    -rw-rw-r-- 1 jay jay 143K Jan 31 23:38 /tmp/cleaned_attack_scans.csv

Additionally, there are data governance, metadata and tracking files created as well:

::

    ls -lrth /tmp/*.json
    -rw-rw-r-- 1 jay jay 2.7K Jan 31 23:38 /tmp/fulldata_metadata.json
    -rw-rw-r-- 1 jay jay 1.8K Jan 31 23:38 /tmp/cleaned_metadata.json
