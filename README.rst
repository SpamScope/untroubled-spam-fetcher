untroubled-spam-getter
======================

Overview
--------

This tool gets the `Untroubled <http://untroubled.org/spam/>`__ spam
mails.

Description
-----------

This tool gets the **Untroubled** spam mails and saves them on
filesystem. You can set the followings variables to change the defaults:

::

    "UNTROUBLED_TIMEOUT": 10,
    "UNTROUBLED_CACHE_PATH": "/tmp",
    "UNTROUBLED_STORE_PATH": "/tmp",

You can set environment variables or change them from command line.
Command line has the priority.

::

    usage: fetcher.py [-h] [-l {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}]
                      [-c UNTROUBLED_CACHE_PATH] [-s UNTROUBLED_STORE_PATH] [-v]

    Untroubled Fetcher

    optional arguments:
      -h, --help            show this help message and exit
      -l {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}, --log {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}
                            Log level (default: INFO)
      -c UNTROUBLED_CACHE_PATH, --cache-path UNTROUBLED_CACHE_PATH
                            Cache path to store downloaded history (default: None)
      -s UNTROUBLED_STORE_PATH, --store-path UNTROUBLED_STORE_PATH
                            Store path to store emails (default: None)
      -v, --version         show program's version number and exit

Authors
-------

Main Author
~~~~~~~~~~~

Fedele Mantuano (**Linkedin**: https://www.linkedin.com/in/fmantuano/)

Installation
------------

::

    $ git clone https://github.com/SpamScope/untroubled-spam-fetcher.git

Usage
-----

::

    $ python3 fetcher/fetcher.py
