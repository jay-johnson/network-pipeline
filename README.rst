Network Data Analysis Pipeline
==============================

This is a distributed python 3 framework for automating network traffic capture and converting it into a csv file. Once you have a csv file you can build, train and tune machine learning models to defend your own infrastructure by actively monitoring the network layer.

There are many choices to build a machine learning or AI model but for now I am using `Jupyter Hub`_ to build a pre-trained model for defending against `OWASP Dynamic Analysis tools for finding vulnerabilities`_ running in my `owasp-jenkins`_ repository.

.. image:: https://github.com/jay-johnson/network-pipeline/blob/master/docker/images/network-pipeline-workflow.png
    :align: center

.. _Jupyter Hub: https://github.com/jay-johnson/celery-connectors#running-jupyterhub-with-postgres-and-ssl
.. _OWASP Dynamic Analysis tools for finding vulnerabilities: https://www.owasp.org/index.php/Category:Vulnerability_Scanning_Tools
.. _owasp-jenkins: https://github.com/jay-johnson/owasp-jenkins

Why?
====

After digging into how `Internet Chemotherapy`_ worked with a simple `Nerfball approach`_, I wanted to see if I could train machine learning and AI models to defend this type of attack. Since the network is the first line to defend on the edge, on-premise or in the cloud, I wanted to start building the first line of defense and open source it. Also I do not know of any other toolchains to build defensive models using the network layer for free.

This repository automates dataset creation for training models by capturing network traffic on layers 2, 3 and 4 of the `OSI model`_. I hope to have functional, deployable, pre-trained models for django and flask soon... 

Stay tuned and **please reach out if you are interested in helping everyone protect our mission-critical and personal infrastructure**.

.. _Internet Chemotherapy: https://0x00sec.org/t/internet-chemotherapy/4664
.. _Nerfball approach: https://github.com/jay-johnson/nerfball
.. _OSI model: https://en.wikipedia.org/wiki/OSI_model

How does it work?
=================

This framework uses free open source tools to create the following publish-subscriber workflow:

#.  Network traffic matches a capture tool filter
#.  Capture tool converts packet layers into JSON
#.  Capture tool publishes converted JSON dictionary to a message broker (Redis or RabbitMQ)
#.  Packet processor consumes dictionary from message broker
#.  Packet processor flattens dictionary
#.  Packet processor periodically writes csv dataset from collected, flattened dictionaries (configurable for snapshotting csv on n-th number of packets consumed)
#.  (Coming soon) Flatten packets are forwarded to a model prediction key for models to predict if the network traffic is good or bad

Envisioned Deployment
---------------------

- For on-premise and cloud environments, this framework would deploy capture tools to load balancers and application servers. These capture tool agents would publish to a redis cluster outside of the load balancers and application servers for analysis. By doing this, models could also be tuned to defend on the load balancer tier or application server tier independently.

- Remote edge machines would be running deployed, pre-trained, package-maintained models that are integrated with a prediction API. Periodic uploads of new, unexpected records would be sent encrypted back to the cloud for retraining models for helping defend an IoT fleet.

Detailed Version
----------------

The pipeline is a capture forwarding system focused on redundancy and scalability. Components-wise there are pre-configured capture tools that hook into the network devices on the operating system. If the capture tools find any traffic that matches their respective filter, then they json-ify the captured packet and forward it as a nested dictionary to a redis server (rabbitmq works as well, but requires setting the environment variables for authentication). Once the traffic packet dictionaries are in redis/rabbitmq, the packet processor consumes the nested dictionary and flattens them using pandas. The packet processors are set up to write csv datasets from the consumed, flattened dictionaries every 100 packets (you can configure the ``SAVE_AFTER_NUM`` environment variable to a larger number too).

Here are the included, standalone capture tools (all of which require root privileges to work):

#.  `capture-arp.py`_
#.  `capture-icmp.py`_
#.  `capture-tcp.py`_
#.  `capture-udp.py`_

.. _capture-arp.py: https://github.com/jay-johnson/network-pipeline/blob/master/network_pipeline/scripts/capture-arp.py
.. _capture-icmp.py: https://github.com/jay-johnson/network-pipeline/blob/master/network_pipeline/scripts/capture-icmp.py
.. _capture-tcp.py: https://github.com/jay-johnson/network-pipeline/blob/master/network_pipeline/scripts/capture-tcp.py
.. _capture-udp.py: https://github.com/jay-johnson/network-pipeline/blob/master/network_pipeline/scripts/capture-udp.py

What packets and layers are supported?
======================================

Layer 2 
-------
    
- Ethernet_
- ARP_

Layer 3
-------

- IPv4_
- IPv6_
- ICMP_

Layer 4
-------

- TCP_
- UDP_
- Raw - hex data from TCP or UDP packet body
    
Layer 5 
-------

- DNS_

.. _Ethernet: https://en.wikipedia.org/wiki/Ethernet
.. _ARP: https://en.wikipedia.org/wiki/Address_Resolution_Protocol
.. _IPv4: https://en.wikipedia.org/wiki/IPv4
.. _IPv6: https://en.wikipedia.org/wiki/IPv6
.. _ICMP: https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol
.. _TCP: https://en.wikipedia.org/wiki/Transmission_Control_Protocol
.. _UDP: https://en.wikipedia.org/wiki/User_Datagram_Protocol
.. _DNS: https://en.wikipedia.org/wiki/Domain_Name_System

How do I get started?
---------------------

#.  Install from pypi or build the development environment

    ::

        pip install network-pipeline

    **Or you can set up the repository locally**

    ::

        git clone https://github.com/jay-johnson/network-pipeline.git
        cd network-pipeline
        virtualenv -m python3 /tmp/netpipevenv && source /tmp/netpipevenv/bin/activate && pip install -e .

#.  Start Redis

    This guide assumes redis is running in docker, but as long as there's an accessible redis server on port 6379 you can use that too. RabbitMQ works as well, but requires setting the environment variables for connectivity.

    ::

        ./start.sh

#.  Verify Redis is Working

    ::

        redis-cli

    or

    ::

        telnet localhost 6379

#.  Start `Packet Processor for Consuming Messages`_

    Activate the virtual environment

    ::

        source /tmp/netpipevenv/bin/activate
        
    Start it up

    ::
    
        ./network_pipeline/scripts/packets-redis.py

    .. _Packet Processor for Consuming Messages: https://github.com/jay-johnson/network-pipeline/blob/master/network_pipeline/scripts/packets-redis.py

Capture Network Traffic
=======================

These tools are installed with the pip and require running with root to be able to hook into the local network devices for capturing traffic correctly.

Scapy_ currently provides the traffic capture tooling, but the code already has a semi-functional scalable, multi-processing engine to replace it. This will be ideal for dropping on a heavily utilized load balancer tier and run as an agent managed as a systemd service.

.. _Scapy: https://github.com/phaethon/scapy

#.  Login as root

    ::

        sudo su

#.  Activate the Virtual Environment

    ::

        source /tmp/netpipevenv/bin/activate

#.  Capture TCP Data

    By default TCP capture is only capturing traffic on ports: 80, 443, 8080, and 8443. This can be modified with the ``NETWORK_FILTER`` environment variable. Please avoid capturing on the redis port (default 6379) and rabbitmq port (default 5672) to prevent duplicate sniffing on the already-captured data that is being forwarded to the message queues which are ideally running in another virtual machine.
    
    This guide assumes you are running all these tools from the base directory of the repository.

    ::
    
        ./network_pipeline/scripts/capture-tcp.py

#.  Capture UDP Data

    With another terminal, you can capture UDP traffic at the same time

    ::

        sudo su
    
    Start UDP capture tool

    ::
    
        source /tmp/netpipevenv/bin/activate && ./network_pipeline/scripts/capture-udp.py

#.  Capture ARP Data

    With another terminal, you can capture ARP traffic at the same time

    ::

        sudo su
    
    Start ARP capture tool

    ::
        
        source /tmp/netpipevenv/bin/activate && ./network_pipeline/scripts/capture-arp.py
        
#.  Capture ICMP Data

    With another terminal, you can capture ICMP traffic at the same time

    ::

        sudo su
    
    Start ICMP capture tool
    
    ::
        
        source /tmp/netpipevenv/bin/activate && ./network_pipeline/scripts/capture-icmp.py

Simulating Network Traffic
--------------------------

I will be updating this guide with ZAP tests in the future but for now here's tools to start simulating network traffic for seeding your csv datasets.

#.  Send a TCP message

    ::

        ./network_pipeline/scripts/tcp-send-msg.py

#.  Send a UDP message

    (Optional) Start a UDP server for echo-ing a response on port 17000
    
    ::

        sudo ./network_pipeline/scripts/listen-udp-port.py
        2018-01-27T17:39:47.725377 - Starting UDP Server address=127.0.0.1:17000 backlog=5 size=1024 sleep=0.5 shutdown=/tmp/udp-shutdown-listen-server-127.0.0.1-17000

    Send the UDP message

    ::

        ./network_pipeline/scripts/udp-send-msg.py
        sending UDP: address=('0.0.0.0', 17000) msg=testing UDP msg time=2018-01-27 17:40:04 - cc9cdc1a-a900-48c5-acc9-b8ff5919087b

    (Optional) Verify the UDP server received the message

    ::

        2018-01-27T17:40:04.915469 received UDP data=testing UDP msg time=2018-01-27 17:40:04 - cc9cdc1a-a900-48c5-acc9-b8ff5919087b 

#.  Simulate traffic with comon shell tools

    ::

        nslookup 127.0.0.1; nslookup 0.0.0.0; nslookup localhost

    ::

        dig www.google.com; dig www.cnn.com; dig amazon.com

    ::

        wget https://www.google.com; wget http://www.cnn.com; wget https://amazon.com

    ::

        ping google.com; ping amazon.com


#.  Run all of them at once

    ::

        nslookup 127.0.0.1; nslookup 0.0.0.0; nslookup localhost; dig www.google.com; dig www.cnn.com; dig amazon.com; wget https://www.google.com; wget http://www.cnn.com; wget https://amazon.com; ping google.com; ping amazon.com
    
Capturing an API Simulation
---------------------------

API analysis using `ZAP`_ is coming soon, but for now a simple POST works too.

.. _ZAP: https://github.com/zaproxy/zaproxy

#.  Start a local server listening on TCP port 80

    ::

        sudo ./network_pipeline/scripts/listen-tcp-port.py 
        2018-01-27T23:59:22.344687 - Starting Server address=127.0.0.1:80 backlog=5 size=1024 sleep=0.5 shutdown=/tmp/shutdown-listen-server-127.0.0.1-80

#.  Run a POST curl

    ::

        curl -i -vvvv -POST http://localhost:80/TESTURLENDPOINT -d '{"user_id", "1234", "api_key": "abcd", "api_secret": "xyz"}'
        *   Trying 127.0.0.1...
        * TCP_NODELAY set
        * Connected to localhost (127.0.0.1) port 80 (#0)
        > POST /TESTURLENDPOINT HTTP/1.1
        > Host: localhost
        > User-Agent: curl/7.55.1
        > Accept: */*
        > Content-Length: 59
        > Content-Type: application/x-www-form-urlencoded
        > 
        * upload completely sent off: 59 out of 59 bytes
        POST /TESTURLENDPOINT HTTP/1.1
        Host: localhost
        User-Agent: curl/7.55.1
        Accept: */*
        Content-Length: 59
        Content-Type: application/x-www-form-urlencoded
        
        * Connection #0 to host localhost left intact
        {"user_id", "1234", "api_key": "abcd", "api_secret": "xyz"}    

#.  Verify local TCP server received the POST

    ::

        2018-01-28T00:00:54.445294 received msg=7 data=POST /TESTURLENDPOINT HTTP/1.1
        Host: localhost
        User-Agent: curl/7.55.1
        Accept: */*
        Content-Length: 59
        Content-Type: application/x-www-form-urlencoded

        {"user_id", "1234", "api_key": "abcd", "api_secret": "xyz"} replying

Larger Traffic Testing
----------------------

#.  Host a local server listening on TCP port 80 using ``nc``

    ::

        sudo nc -l 80

#.  Send a large TCP msg to the ``nc`` server

    ::

        ./network_pipeline/scripts/tcp-send-large-msg.py

Inspecting the CSV Datasets
===========================

By default, the dataset csv files are saved to: ``/tmp/netdata-*.csv`` and you can set a custom path by exporting the environment variables ``DS_NAME``, ``DS_DIR`` or ``OUTPUT_CSV`` as needed.

::

    ls /tmp/netdata-*.csv 
    /tmp/netdata-2018-01-27-13-13-58.csv  /tmp/netdata-2018-01-27-13-18-25.csv  /tmp/netdata-2018-01-27-16-44-08.csv
    /tmp/netdata-2018-01-27-13-16-38.csv  /tmp/netdata-2018-01-27-13-19-46.csv
    /tmp/netdata-2018-01-27-13-18-03.csv  /tmp/netdata-2018-01-27-13-26-34.csv

Optional Tweaks
---------------

#.  Colorized Logging for Debugging

    Export the path to the colorized logger config. This examples assumes you are in the base directory of the repository.

    ::

        export LOG_CFG=$(pwd)/network_pipeline/log/colors-logging.json

Linting
-------

flake8 .

pycodestyle

License
-------

Apache 2.0 - Please refer to the LICENSE_ for more details

.. _License: https://github.com/jay-johnson/network-pipeline/blob/master/LICENSE

