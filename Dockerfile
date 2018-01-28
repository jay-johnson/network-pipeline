FROM jayjohnson/celery-connectors:latest

RUN apk add --update \
  gcc \
  linux-headers

ENV START_SCRIPT /opt/networkpipeline/network_pipeline/scripts/start-container.sh
ENV LOG_CFG /opt/networkpipeline/network_pipeline/log/colors-logging.json

RUN mkdir -p -m 777 /opt/networkpipeline

COPY network-pipeline-latest.tgz /opt/networkpipeline

RUN cd /opt/networkpipeline \
  && tar xvf network-pipeline-latest.tgz \
  && ls /opt/networkpipeline \
  && cd /opt/networkpipeline \
  && ls -l /opt/networkpipeline \
  && source /opt/celery_connectors/venv/bin/activate \
  && pip install -e . \
  && pip list --format=columns

WORKDIR /opt/networkpipeline

ENTRYPOINT /opt/networkpipeline/network_pipeline/scripts/start-container.sh
