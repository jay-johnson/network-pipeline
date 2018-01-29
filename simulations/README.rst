Network Traffic Simulations
===========================

This directory holds examples for generating ZAP tests for recording the network traffic. The included web applications are targeted by **ZAP** attacks and `dynamic analysis testing`_ and recorded using the capture tools. Once a server is running you can use the `ZAPv2 script`_ to generate network traffic, and auto-capture it as a dataset for modeling and predicting an incoming attack on your network layer.

This guide assumes the `Network Pipeline - Capture tools`_ are already running and capturing traffic on the server port (TCP 8080 by default).

.. _dynamic analysis testing: https://www.owasp.org/index.php/Category:Vulnerability_Scanning_Tools
.. _ZAPv2 script: https://github.com/zaproxy/zaproxy/wiki/ApiPython
.. _Network Pipeline - Capture tools: https://github.com/jay-johnson/network-pipeline#detailed-version

Django 2.0
----------

#.  Install

    Install a sample `Django 2.0`_ web application

    ::

        cd simulations/django

    ::

        ./install.sh

    .. _Django 2.0: https://docs.djangoproject.com/en/2.0/intro/tutorial01/

#.  Start the Application

    ::

        ./start.sh


Setting up ZAP
--------------

.. image:: https://www.owasp.org/images/1/11/Zap128x128.png
    :align: center

#.  Run ZAPv2 Test Script
        
    Activate the virtual environment

    ::
    
        source /tmp/netpipevenv/bin/activate

    Start the tests

    ::

        cd zap/tests
        ./django-zap.py 

#.  Verify ZAP output

    ::

        Accessing target=http://localhost:8090
        Spidering target=http://localhost:8090
        Spider progress=33
        Spider progress=59
        Spider completed
        Scanning target=http://localhost:8090
        Scan progress 0: 

#.  (Optional) Start the ZAP UI in Docker

    This will install the `owasp/zap2docker-live`_ docker image that is ``~1.5 GB``
    
    ::

        cd zap

    ::

        ./start.sh

    If you want to use the ZAP UI in a browser:

    http://127.0.0.1:8090
    
    .. _owasp/zap2docker-live: https://hub.docker.com/r/owasp/zap2docker-live/

Customizing ZAP Tests
=====================

If you want to build your own ZAP tests, here is a `sample ZAPv2 script`_ showing how to build a scanning tool for automating attacks for capturing the network traffic.

    .. _sample ZAPv2 script: https://github.com/zaproxy/zaproxy/wiki/ApiPython#an-example-python-script
