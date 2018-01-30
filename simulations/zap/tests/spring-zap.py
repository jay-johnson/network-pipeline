#!/usr/bin/env python

import os
import sys
import time
import json
import requests
from zapv2 import ZAPv2

user = os.getenv(
            "ZAP_USER",
            "root")
password = os.getenv(
            "ZAP_PASSWORD",
            "q")
client_id = os.getenv(
            "ZAP_CLIENT_ID",
            "documentation")
secret_key = os.getenv(
            "ZAP_SECRET_KEY",
            "")
endpoint = os.getenv(
            "ZAP_ENDPOINT_URL",
            "http://localhost:8080")
target = "{}/petclinic".format(
            endpoint)

# Change to match the API key set in ZAP, 
# or use None if the API key is disabled
apikey = os.getenv("ZAP_TOKEN",
                   "")

if apikey != "changeme":
    print(("Starting ZAP with target={} apikey={}")
          .format(target,
                  apikey))

# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apikey,
            proxies={"http": "http://localhost:8090",
                     "https": "http://localhost:8090"})

"""
Use the line below if ZAP is not listening on port 8080,
for example, if listening on port 8090
zap = ZAPv2(apikey=apikey, proxies={"http": "http://127.0.0.1:8090",
                                    "https": "http://127.0.0.1:8090"})
"""

# do stuff
print("Accessing target={}".format(target))
# try have a unique enough session...
zap.urlopen(target)
# Give the sites tree a chance to get updated
time.sleep(2)

print("Spidering target={}".format(target))
scanid = zap.spider.scan(target)
# Give the Spider a chance to start
time.sleep(2)
while (int(zap.spider.status(scanid)) < 100):
    print("Spider progress={}".format(zap.spider.status(scanid)))
    time.sleep(2)

print("Spider completed")
# Give the passive scanner a chance to finish
time.sleep(5)

print("Scanning target={}".format(target))
scanid = zap.ascan.scan(target)
while (int(zap.ascan.status(scanid)) < 100):
    print("Scan progress {}: ".format(zap.ascan.status(scanid)))
    time.sleep(5)

print("Scan completed")

# Report the results

print("Hosts: " + ", ".join(zap.core.hosts))
print("Alerts: ")
print(zap.core.alerts())
