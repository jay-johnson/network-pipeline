Network Traffic Simulations
===========================

This directory holds examples for generating ZAP tests for recording network traffic. The included web applications are targeted by **ZAP** attacks and `dynamic analysis testing`_ and recorded using the capture tools. Once a server is running you can use the `ZAPv2 script`_ to generate network traffic, and auto-capture it as a dataset for modeling and predicting an incoming attack on your network layer.

This guide assumes the `Network Pipeline - Capture tools`_ are already running and capturing traffic on the server port (TCP 8080 by default).

.. _dynamic analysis testing: https://www.owasp.org/index.php/Category:Vulnerability_Scanning_Tools
.. _ZAPv2 script: https://github.com/zaproxy/zaproxy/wiki/ApiPython
.. _Network Pipeline - Capture tools: https://github.com/jay-johnson/network-pipeline#detailed-version

Starting ZAP
============

.. image:: https://www.owasp.org/images/1/11/Zap128x128.png
    :align: center

#.  Start the ZAP Docker Proxy

    This will start the `owasp/zap2docker-live`_ docker image that is ``~1.5 GB``. This will run on TCP port 8090 on the local host and then scans a web application listening on TCP port 8080.
    
    ::

        cd zap

    ::

        ./start.sh

    If you want to use the ZAP UI in a browser:

    http://127.0.0.1:8090
    
    .. _owasp/zap2docker-live: https://hub.docker.com/r/owasp/zap2docker-live/

Django REST Framework with JWT and Swagger
==========================================

This also includes some advanced user registration handling with:

https://github.com/alej0varas/django-registration-rest-framework

#.  Install

    ::

        cd simulations/jwt-swagger-django-rest

    ::

        ./install.sh
    
#.  Start

    ::

        ./start.sh 
        Starting Django listening on TCP port 8080
        http://localhost:8080/admin

        django-configurations version 2.0, using configuration 'Development'
        Performing system checks...

        System check identified no issues (0 silenced).
        February 02, 2018 - 09:44:43
        Django version 2.0, using settings 'project_name.settings'
        Starting development server at http://0.0.0.0:8080/
        Quit the server with CONTROL-C.

#.  Browse the Django REST Framework API
    
    http://0.0.0.0:8080/

#.  Browse to Swagger

    http://0.0.0.0:8080/swagger/

#.  Login

    By default the super user is: ``root`` with password ``123321``

    http://0.0.0.0:8080/api-auth/login/

#.  Create a new user

    http://localhost:8080/swagger/#!/users/users_create

#.  Get a JWT Token

    http://localhost:8080/swagger/#!/api-token-auth/api_token_auth_create

Flask RESTplus with Swagger
===========================

#.  Install

    Install an example `Flask RESTplus with Swagger`_ web application

    ::

        cd simulations/flask

    ::

        ./install.sh

    .. _Flask RESTplus with Swagger: https://github.com/frol/flask-restplus-server-example.git

#.  Start the Application

    ::

        ./start.sh

Login using a browser
---------------------

http://localhost:8080/api/v1/

To authenticate, click the ``Authorize`` button on the top right.

#.  User credentials

    ::

        Username: root
        Password: q

#.  Select Basic Auth

    ::

        Basic auth

#.  Set Client ID

    ::

        documentation

#.  Scope this access by selecting checkboxes

    ::

        auth:read
        auth:write
        users:read
        users:write
        teams:read
        teams:write

#.  Click the ``Authorize`` button below the scope section

#.  Get User Details

    http://localhost:8080/api/v1/#!/users/get_user_me

    Click the ``Try it out!`` button

#.  Run ZAPv2 test
        
    Activate the virtual environment

    ::
    
        source /tmp/netpipevenv/bin/activate

#.  Start the tests

    The tests will authenticate using OAuth 2.0 to get a valid token for the default ``root`` user. ZAP will use this token to run scans as the user.

    ::

        cd zap/tests
        ./flask-zap.py 

#.  Verify ZAP output

    ::

        ./flask-zap.py 
        Starting zap with auth_url=http://localhost:8080/auth/oauth2/token?grant_type=password&client_id=documentation&username=root&password=q
        Starting ZAP with target=http://127.0.0.1:8080 apikey=ADwUFlRehVS1vbhMkiNayoGjf3O8Xw
        Accessing target=http://127.0.0.1:8080
        Spidering target=http://127.0.0.1:8080
        Spider completed
        Scanning target=http://127.0.0.1:8080
        Scan progress 1: 

#.  Verify Flask is processing the ZAP scan

    ::

        2018-01-29 11:15:49,232 [DEBUG] [flask_oauthlib] Fetched extra credentials, {}.
        2018-01-29 11:15:49,233 [DEBUG] [flask_oauthlib] Authenticate client 'documentation'.
        2018-01-29 11:15:49,235 [DEBUG] [flask_oauthlib] Validating username 'root' and its password
        2018-01-29 11:15:49,514 [DEBUG] [flask_oauthlib] Found default scopes ['auth:read', 'auth:write', 'users:read', 'users:write', 'teams:read', 'teams:write']
        2018-01-29 11:15:49,515 [DEBUG] [flask_oauthlib] Save bearer token {'access_token': 'ADwUFlRehVS1vbhMkiNayoGjf3O8Xw', 'expires_in': 3600, 'token_type': 'Bearer', 'scope': 'auth:read auth:write users:read users:write teams:read teams:write', 'refresh_token': '1Dp2RXfBqslR8nJ6HvUHAXj1mqBvbd'}
        2018-01-29 11:15:49,521 [INFO] [werkzeug] 127.0.0.1 - - [29/Jan/2018 11:15:49] "GET /auth/oauth2/token?grant_type=password&client_id=documentation&username=root&password=q HTTP/1.1" 200 -
        2018-01-29 11:15:49,527 [INFO] [werkzeug] 127.0.0.1 - - [29/Jan/2018 11:15:49] "GET / HTTP/1.1" 404 -
        2018-01-29 11:15:51,542 [INFO] [werkzeug] 127.0.0.1 - - [29/Jan/2018 11:15:51] "GET / HTTP/1.1" 404 -
        2018-01-29 11:15:51,550 [INFO] [werkzeug] 127.0.0.1 - - [29/Jan/2018 11:15:51] "GET /robots.txt HTTP/1.1" 404 -
        2018-01-29 11:15:51,552 [INFO] [werkzeug] 127.0.0.1 - - [29/Jan/2018 11:15:51] "GET /sitemap.xml HTTP/1.1" 404 -
        2018-01-29 11:15:51,553 [INFO] [werkzeug] 127.0.0.1 - - [29/Jan/2018 11:15:51] "GET / HTTP/1.1" 404 -
        2018-01-29 11:15:53,611 [INFO] [werkzeug] 127.0.0.1 - - [29/Jan/2018 11:15:53] "GET / HTTP/1.1" 404 -
        2018-01-29 11:15:58,587 [INFO] [werkzeug] 127.0.0.1 - - [29/Jan/2018 11:15:58] "GET /8927056341039516893 HTTP/1.1" 404 -
        2018-01-29 11:15:58,602 [INFO] [werkzeug] 127.0.0.1 - - [29/Jan/2018 11:15:58] "GET /?query=c%3A%2FWindows%2Fsystem.ini HTTP/1.1" 404 -

Django 2.0
==========

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

#.  Confirm Django is running in a browser

    Register a user:
    
    http://0.0.0.0:8080/accounts/register/
    
    Login as that user:

    http://0.0.0.0:8080/accounts/login/
    
    View user profile:

    http://0.0.0.0:8080/accounts/profile/

#.  Run ZAPv2 test
        
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

React and Redux User Registration
=================================

#.  Install

    Install the `React and Redux Registration example`_ web application

    ::

        cd simulations/react-redux

    (Optional) install ``npm`` on the host (``sudo apt-get install npm``).

    ::

        ./install.sh

    .. _React and Redux Registration example: https://github.com/cornflourblue/react-redux-registration-login-example

#.  Start the Application

    ::

        ./start.sh

#.  Confirm React and Redux is running from a browser

    http://localhost:8080/

#.  Run ZAPv2 test
        
    Activate the virtual environment

    ::
    
        source /tmp/netpipevenv/bin/activate

    Start the tests

    ::

        cd zap/tests
        ./react-redux-zap.py

#.  Verify ZAP output

    ::

        Starting ZAP with target=http://localhost:8080/ apikey=
        Accessing target=http://localhost:8080/
        Spidering target=http://localhost:8080/
        Spider completed
        Scanning target=http://localhost:8080/
        Scan progress 0: 
        Scan progress 18: 
        Scan progress 18: 
        Scan progress 18: 
        Scan progress 30: 
        Scan progress 71: 
        Scan completed

Vue User Registration
=====================

#.  Install

    Install the `Vue boilerplate`_ web application

    ::

        cd simulations/vue

    (Optional) install ``npm`` on the host (``sudo apt-get install npm``).

    ::

        ./install.sh

    .. _Vue boilerplate: https://github.com/petervmeijgaard/vue-2-boilerplate.git

#.  Start the Application

    ::

        ./start.sh

#.  Confirm Vue is running from a browser

    http://localhost:8080/#/login

#.  Run ZAPv2 test
        
    Activate the virtual environment

    ::
    
        source /tmp/netpipevenv/bin/activate

    Start the tests

    ::

        cd zap/tests
        ./vue-zap.py

#.  Verify ZAP output

    ::

        Starting ZAP with target=http://localhost:8080/ apikey=
        Accessing target=http://localhost:8080/
        Spidering target=http://localhost:8080/
        Spider completed
        Scanning target=http://localhost:8080/
        Scan progress 0: 
        Scan progress 18: 
        Scan progress 18: 
        Scan progress 18: 
        Scan progress 30: 
        Scan progress 71: 
        Scan completed

Spring Pet Clinic
=================

#.  Start the Containers

    ::

        cd simulations/spring 

    ::

        ./install.sh

    The docker containers can take a few minutes to download, and then they download the jars before starting up. Just a note, these containers are ``~1.5 GB`` combined.
    
    ::

        ./start.sh

#.  Verify Pet Clinic works in a browser

    http://localhost:8080/petclinic

#.  Run ZAPv2 test
        
    Activate the virtual environment

    ::
    
        source /tmp/netpipevenv/bin/activate

    Start the tests

    ::

        cd zap/tests
        ./spring-zap.py

#.  Verify ZAP output

    ::

        Starting ZAP with target=http://localhost:8080/ apikey=
        Accessing target=http://localhost:8080/
        Spidering target=http://localhost:8080/
        Spider completed
        Scanning target=http://localhost:8080/
        Scan progress 0: 
        Scan progress 18: 
        Scan progress 18: 
        Scan progress 18: 
        Scan progress 30: 
        Scan progress 71: 
        Scan completed

#.  Stop the Containers

    ::

        ./stop.sh

Customizing ZAP Tests
=====================

If you want to build your own ZAP tests, here is a `sample ZAPv2 script`_ showing how to build a scanning tool for automating attacks for capturing the network traffic.

    .. _sample ZAPv2 script: https://github.com/zaproxy/zaproxy/wiki/ApiPython#an-example-python-script
