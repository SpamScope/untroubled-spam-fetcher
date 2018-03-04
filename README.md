[![PyPI version](https://badge.fury.io/py/untroubled-spam-fetcher.svg)](https://badge.fury.io/py/untroubled-spam-fetcher)

# untroubled-spam-getter


## Overview
This tool gets the [Untroubled](http://untroubled.org/spam/) spam mails.
You can use this tool as daemon or not.


## Description
This tool gets the **Untroubled** spam mails and saves them on filesystem.
You can set the followings variables to change the defaults:

```
"UNTROUBLED_TIMEOUT": 20,
"UNTROUBLED_CACHE_PATH": "/var/tmp",
"UNTROUBLED_STORE_PATH": "/tmp/untroubled_mails",
"UNTROUBLED_WAIT_TIME": 3600,
"UNTROUBLED_MONTHS": 0,
```

`UNTROUBLED_TIMEOUT`: timeout HTTP connections.
`UNTROUBLED_CACHE_PATH`: path where store the cache files useful to get only mails delta.
`UNTROUBLED_STORE_PATH`: path where store the mails.
`UNTROUBLED_WAIT_TIME`: if daemon is enabled wait time seconds before gets new mails.
`UNTROUBLED_MONTHS`: how many months archive you want get. 0 means only last month.


You can set environment variables or change them from command line. Command line
has the priority.

```
 $ untroubled-spam-fetcher -h
usage: fetcher.py [-h] [-l {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}]
                  [-c UNTROUBLED_CACHE_PATH] [-s UNTROUBLED_STORE_PATH]
                  [-m UNTROUBLED_MONTHS] [-d] [-w UNTROUBLED_WAIT_TIME]
                  [-t UNTROUBLED_TIMEOUT] [-v]

Untroubled Fetcher

optional arguments:
  -h, --help            show this help message and exit
  -l {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}, --log {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}
                        Log level (default: INFO)
  -c UNTROUBLED_CACHE_PATH, --cache-path UNTROUBLED_CACHE_PATH
                        Cache path to store downloaded history (default: None)
  -s UNTROUBLED_STORE_PATH, --store-path UNTROUBLED_STORE_PATH
                        Store path to store emails (default: None)
  -m UNTROUBLED_MONTHS, --months UNTROUBLED_MONTHS
                        Months mails archive to get (no more 12) (default:
                        None)
  -d, --daemon          Start in daemon mode (default: False)
  -w UNTROUBLED_WAIT_TIME, --wait-time UNTROUBLED_WAIT_TIME
                        Seconds to wait between two fetch (default: None)
  -t UNTROUBLED_TIMEOUT, --timeout UNTROUBLED_TIMEOUT
                        HTTP timeout connection in seconds (default: None)
  -v, --version         show program's version number and exit
```


## Authors

### Main Author
Fedele Mantuano (**Linkedin**: https://www.linkedin.com/in/fmantuano/)


## Installation

```
$ git clone https://github.com/SpamScope/untroubled-spam-fetcher.git
$ cd virtualenv -p python3 venv
$ source venv/bin/activate
$ python setup.py install
```

or

```
$ cd virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install untroubled-spam-fetcher
```


## Usage
`untroubled-spam-fetcher` only works with Python 3.

```
$ untroubled-spam-fetcher -l DEBUG -c /tmp/cache -s /tmp/mails -d
```

In this case runs as daemon, with logging in debug mode, uses `/tmp/cache` as cache folder and `/tmp/mails` as folder where stores the mails.