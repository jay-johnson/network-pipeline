#!/usr/bin/env python

import time
from zapv2 import ZAPv2

target = "http://localhost:8090"
# Change to match the API key set in ZAP, 
# or use None if the API key is disabled
apikey = "changeme"

# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apikey,
            proxies={"http": target,
                     "https": target})

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
