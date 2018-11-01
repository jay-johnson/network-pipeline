import os
import sys
import warnings
import unittest

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py


cur_path, cur_script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(cur_path))

install_requires = [
    "antinex-client",
    "ansible>=1.9",
    "celery-connectors",
    "coverage",
    "colorlog",
    "flake8<=3.4.1",
    "future",
    "kamene",
    "netifaces",
    "pandas",
    "pep8>=1.7.1",
    "pipenv",
    "pydocstyle",
    "pycodestyle<=2.3.1",
    "pylint",
    "python-logstash",
    "python-owasp-zap-v2.4",
    "python-dateutil<2.7.0",
    "spylunking",
    "tox",
    "unittest2",
    "mock"
]


if sys.version_info < (3, 5):
    warnings.warn(
        "Less than Python 3.5 is not supported.",
        DeprecationWarning)


def networkpipeline_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    return test_suite


# Do not import networkpipeline module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "network_pipeline"))

setup(
    name="network-pipeline",
    cmdclass={"build_py": build_py},
    version="1.2.6",
    description=(
        "Distributed Network Packet Analysis Pipeline " +
        "for Layer 2, 3 and 4 Frames"),
    long_description="" +
    "Python 3 AI-ready framework for recording network traffic in "
    "a data pipeline. Once recorded, you can train a " +
    "deep neural network (DNN) " +
    "to identify attack and non-attack traffic on your network. " +
    "Included demo DNN has over 83% accuracy predicting " +
    "attack vs non-attack records. " +
    "" +
    "Currently supports recording ethernet and arp (layer 2), " +
    "ipv4, ipv6 and icmp (layer 3) and also " +
    "tcp, udp frames (layer 4) frames and datagrams. " +
    "Messages are auto-forwarded over to redis or rabbitmq " +
    "for distributed processing in realtime. " +
    "\n" +
    "Why should I use this? " +
    "This framework can help " +
    "build, train and tune your own " +
    "defensive machine learning models to help defend your " +
    "own infrastructure at the network layer. Once the data " +
    "is auto-saved as a csv file, then you can build models " +
    "within Jupyter notebooks: " +
    "https://github.com/jay-johnson/celery-connectors" +
    "#running-jupyterhub-with-postgres-and-ssl " +
    "or your ML/AI framework of choice. " +
    "\n" +
    "This pip also has an example for training a Keras Deep "
    "Neural Network model to predict attack and non-attack records " +
    "using a captured and prepared dataset. " +
    "\n" +
    "There are test tools installed with this pip to quickly " +
    "send mock: TCP, UDP, ARP and ICMP packets. " +
    "\n" +
    "This build currently utilizes scapy-python3 " +
    "for packet recording: " +
    "https://github.com/phaethon/scapy " +
    "\n" +
    "Future builds will utilize the multiprocessing engine " +
    "included but does not filter src/dst ports correctly yet." +
    "The license will be full Apache 2 once that migration " +
    "is done." +
    "",
    author="Jay Johnson",
    author_email="jay.p.h.johnson@gmail.com",
    url="https://github.com/jay-johnson/network-pipeline",
    packages=[
        "network_pipeline",
        "network_pipeline.scripts",
        "network_pipeline.scripts.builders",
        "network_pipeline.scripts.modelers",
        "network_pipeline.scripts.tools",
        "network_pipeline.log"
    ],
    package_data={},
    install_requires=install_requires,
    test_suite="setup.networkpipeline_test_suite",
    tests_require=[
    ],
    scripts=[
        "network_pipeline/scripts/arp_send_msg.py",
        "network_pipeline/scripts/capture_arp.py",
        "network_pipeline/scripts/capture_icmp.py",
        "network_pipeline/scripts/capture_ssh.py",
        "network_pipeline/scripts/capture_tcp.py",
        "network_pipeline/scripts/capture_telnet.py",
        "network_pipeline/scripts/capture_udp.py",
        "network_pipeline/scripts/icmp_send_msg.py",
        "network_pipeline/scripts/listen_udp_port.py",
        "network_pipeline/scripts/listen_tcp_port.py",
        "network_pipeline/scripts/network_agent.py",
        "network_pipeline/scripts/tcp_send_msg.py",
        "network_pipeline/scripts/udp_send_msg.py",
        "network_pipeline/scripts/packets_redis.py",
        "network_pipeline/scripts/packets_rabbitmq.py",
        "network_pipeline/scripts/builders/prepare_dataset.py",
        "network_pipeline/scripts/modelers/keras_dnn.py",
        "network_pipeline/scripts/start-container.sh"
    ],
    use_2to3=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
