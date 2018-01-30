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
    "ansible>=1.9",
    "celery-connectors",
    "coverage",
    "colorlog",
    "docker-compose",
    "flake8>=3.4.1",
    "future",
    "netifaces",
    "pandas",
    "pep8>=1.7.1",
    "pipenv",
    "pydocstyle",
    "pylint",
    "python-logstash",
    "python-owasp-zap-v2.4",
    "scapy-python3",
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
    version="1.0.4",
    description="Distributed Network Packet Analysis Pipeline " +
    "for Layer 2, 3 and 4 Frames",
    long_description="" +
    "Python 3 framework for building a distributed network analysis "
    "pipeline. Currently supports recording ethernet and arp (layer 2), " +
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
        "network_pipeline.log"
    ],
    package_data={},
    install_requires=install_requires,
    test_suite="setup.networkpipeline_test_suite",
    tests_require=[
    ],
    scripts=[
        "network_pipeline/scripts/arp-send-msg.py",
        "network_pipeline/scripts/capture-arp.py",
        "network_pipeline/scripts/capture-icmp.py",
        "network_pipeline/scripts/capture-tcp.py",
        "network_pipeline/scripts/capture-udp.py",
        "network_pipeline/scripts/icmp-send-msg.py",
        "network_pipeline/scripts/listen-udp-port.py",
        "network_pipeline/scripts/listen-tcp-port.py",
        "network_pipeline/scripts/network-agent.py",
        "network_pipeline/scripts/tcp-send-msg.py",
        "network_pipeline/scripts/udp-send-msg.py",
        "network_pipeline/scripts/packets-redis.py",
        "network_pipeline/scripts/packets-rabbitmq.py",
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
