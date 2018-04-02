#!/bin/bash

echo ""
date

cd /opt/networkpipeline
source /opt/celery_connectors/venv/bin/activate

if [[ "${UPGRADE_PIPS}" != "" ]]; then
    echo "Updgrading pips: ${UPGRADE_PIPS}"
    pip install --upgrade ${PIP_PROXY_ARGS} ${UPGRADE_PIPS}
fi

echo "Capturing device=${CAP_DEVICE} mode=${CAP_MODE} filter=${NETWORK_FILTER}"

# colorized logging for now
export LOG_CFG=/opt/networkpipeline/network_pipeline/log/colors-logging.json

if [[ "${CAP_COMMAND}" != "" ]]; then
    if [[ -e ${CAP_COMMAND} ]]; then
        chmod 777 ${CAP_COMMAND}
        cap_command=${CAP_COMMAND}
    fi
else
    if [[ "${CAP_MODE}" == "ARP" ]]; then
        echo "loading ARP capture tool"
        cap_command=/opt/networkpipeline/network_pipeline/scripts/capture_arp.py
    elif [[ "${CAP_MODE}" == "ICMP" ]]; then
        echo "loading ICMP capture tool"
        cap_command=/opt/networkpipeline/network_pipeline/scripts/capture_icmp.py
    elif [[ "${CAP_MODE}" == "TCP" ]]; then
        echo "loading TCP capture tool"
        cap_command=/opt/networkpipeline/network_pipeline/scripts/capture_tcp.py
    elif [[ "${CAP_MODE}" == "UDP" ]]; then
        echo "loading UDP capture tool"
        cap_command=/opt/networkpipeline/network_pipeline/scripts/capture_udp.py
    fi
fi

if [[ -e "${cap_command}" ]]; then
    echo "starting command=${cap_command}"
    /opt/celery_connectors/venv/bin/python --version
    /opt/celery_connectors/venv/bin/pip list --format=columns
    /opt/celery_connectors/venv/bin/python $cap_command
    echo "done"
else
    echo "Missing path to cap_command file=${cap_command}"
fi

exit 0
