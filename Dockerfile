FROM jayjohnson/ai-core:latest

RUN echo "creating project directories" \
  && mkdir -p -m 777 /var/log/antinex/pipeline \
  && mkdir -p -m 777 /opt/antinex \
  && chmod 777 //var/log/antinex/pipeline \
  && touch /var/log/antinex/pipeline/latest-packets-redis.log \
  && touch /var/log/antinex/pipeline/latest-packets-rabbitmq.log \
  && chmod 777 /var/log/antinex/pipeline/latest-packets-redis.log \
  && chmod 777 /var/log/antinex/pipeline/latest-packets-rabbitmq.log \
  && echo "updating repo" \
  && cd /opt/antinex/pipeline \
  && git checkout master \
  && git pull \
  && echo "checking repos in container" \
  && ls -l /opt/antinex/pipeline \
  && echo "activating venv" \
  && . /opt/venv/bin/activate \
  && cd /opt/antinex/pipeline \
  && echo "installing pip upgrades" \
  && pip install --upgrade -e . \
  && echo "building docs" \
  && cd /opt/antinex/pipeline/docs \
  && ls -l \
  && make html

ENV PROJECT_NAME="pipeline" \
    SHARED_LOG_CFG="/opt/antinex/core/antinex_core/log/debug-openshift-logging.json" \
    DEBUG_SHARED_LOG_CFG="0" \
    LOG_LEVEL="DEBUG" \
    LOG_FILE="/var/log/antinex/pipeline/latest-packets-redis.log" \
    USE_ENV="drf-dev" \
    USE_VENV="/opt/venv" \
    API_DEBUG="false" \
    USE_FILE="false" \
    SILENT="-s"

WORKDIR /opt/antinex/pipeline

# set for anonymous user access in the container
RUN find /opt/antinex/pipeline -type d -exec chmod 777 {} \;
RUN find /var/log/antinex -type d -exec chmod 777 {} \;

ENTRYPOINT . /opt/venv/bin/activate \
  && /opt/antinex/pipeline/network_pipeline/scripts/packets_redis.py
