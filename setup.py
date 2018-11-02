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

"""
https://packaging.python.org/guides/making-a-pypi-friendly-readme/
check the README.rst works on pypi as the
long_description with:
twine check dist/*
"""
long_description = open('README.rst').read()
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
    version="1.2.10",
    description=(
        "Distributed Network Packet Analysis Pipeline " +
        "for Layer 2, 3 and 4 Frames"),
    long_description=long_description,
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
