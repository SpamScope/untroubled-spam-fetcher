#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2018 Fedele Mantuano (https://www.linkedin.com/in/fmantuano/)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import argparse
import runpy
import os


current = os.path.realpath(os.path.dirname(__file__))

__version__ = runpy.run_path(
    os.path.join(current, "version.py"))["__version__"]


def get_args():
    parser = argparse.ArgumentParser(
        description="Untroubled Fetcher",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Commons options
    parser.add_argument(
        "-l",
        "--log",
        choices=[
            "CRITICAL",
            "ERROR",
            "WARNING",
            "INFO",
            "DEBUG",
            "NOTSET"],
        default="INFO",
        help="Log level",
        dest="log")

    parser.add_argument(
        "-c",
        "--cache-path",
        help="Cache path to store downloaded history",
        dest="UNTROUBLED_CACHE_PATH")

    parser.add_argument(
        "-s",
        "--store-path",
        help="Store path to store emails",
        dest="UNTROUBLED_STORE_PATH")

    parser.add_argument(
        "-m",
        "--months",
        help="Months mails archive to get (no more 12)",
        dest="UNTROUBLED_MONTHS")

    parser.add_argument(
        "-d",
        "--daemon",
        dest="daemon",
        action="store_true",
        help="Start in daemon mode")

    parser.add_argument(
        "-w",
        "--wait-time",
        type=int,
        help="Seconds to wait between two fetch",
        dest="UNTROUBLED_WAIT_TIME")

    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        help="HTTP timeout connection in seconds",
        dest="UNTROUBLED_TIMEOUT")

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__))

    return parser.parse_args()
