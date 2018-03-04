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


import asyncio
import logging
import os
import sys
from collections import ChainMap

import aiohttp

from .commons import (
    fetch_mail_archive,
    fetch_mail_attach,
    fetch_url,
    get_new_attach_urls,
    make_worker_folders,
    urls_to_fetch,
)
from .consts import ATTACH_URL, MAILS_URL, __defaults__
from .args import get_args
from .exceptions import UntroubledMonthsError


log = logging.getLogger()


def main():
    # all options
    args = {k: v for k, v in vars(get_args()).items() if v}
    options = ChainMap(args, os.environ, __defaults__)
    daemon = bool(options.get("daemon", False))
    months = int(options["UNTROUBLED_MONTHS"])

    if daemon and months != 0:
        raise UntroubledMonthsError(
            "In daemon mode you can fetch only last month [-m 0]")

    if months > 12:
        raise UntroubledMonthsError("Number of months upper that 12")

    # make Untroubled worker folder
    make_worker_folders(options)

    # Logging
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        ("%(asctime)s | %(process)d | %(thread)d | "
         "%(name)s | %(levelname)s | %(message)s"))

    # stdout log
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(formatter)
    stdout.setLevel(options["log"])
    log.addHandler(stdout)

    # asyncio loop
    loop = asyncio.get_event_loop()

    if daemon:
        try:
            loop.create_task(mails_attach(options))
            loop.create_task(mails(options))
            loop.run_forever()
        except KeyboardInterrupt:
            log.info("Exit from asyncio loop")
        finally:
            log.info("Asyncio loop closed")
            loop.close()
    else:
        future = asyncio.ensure_future(run(options))
        loop.run_until_complete(future)
        if loop.is_running():
            loop.close()


async def run(options):
    tasks = []
    for i in (mails_attach(options), mails(options)):
        tasks.append(asyncio.ensure_future(i))
    return await asyncio.gather(*tasks)


async def mails_attach(options):
    store_path = options["UNTROUBLED_STORE_PATH"]
    cache_path = options["UNTROUBLED_CACHE_PATH"]
    timeout = int(options["UNTROUBLED_TIMEOUT"])
    wait_sec = int(options["UNTROUBLED_WAIT_TIME"])
    daemon = bool(options.get("daemon", False))

    async with aiohttp.ClientSession() as session:
        while True:
            html = await fetch_url(session, ATTACH_URL, timeout)
            urls = urls_to_fetch(html, ATTACH_URL)
            log.debug("urls in attachments page {}".format(len(urls)))
            urls = get_new_attach_urls(urls, cache_path)
            tasks = [fetch_mail_attach(
                store_path,
                session,
                url,
                timeout) for url in urls]

            res = await asyncio.gather(*tasks)

            if daemon:
                log.debug("Waiting for {} seconds in mail_attach".format(
                    wait_sec))
                await asyncio.sleep(wait_sec)
            else:
                return res


async def mails(options):
    store_path = options["UNTROUBLED_STORE_PATH"]
    cache_path = options["UNTROUBLED_CACHE_PATH"]
    timeout = int(options["UNTROUBLED_TIMEOUT"])
    wait_sec = int(options["UNTROUBLED_WAIT_TIME"])
    months = int(options["UNTROUBLED_MONTHS"])
    daemon = bool(options.get("daemon", False))

    async with aiohttp.ClientSession() as session:
        while True:
            html = await fetch_url(session, MAILS_URL, timeout)
            log.debug("Got main page {!r}".format(MAILS_URL))
            urls = urls_to_fetch(html, MAILS_URL)[-(2 + months):-1]
            log.debug("Getting {} archive from Untroubled".format(len(urls)))
            tasks = [fetch_mail_archive(
                cache_path,
                store_path,
                session,
                url,
                timeout) for url in urls]

            res = await asyncio.gather(*tasks)

            if daemon:
                log.debug("Waiting for {} seconds in mails".format(wait_sec))
                await asyncio.sleep(wait_sec)
            else:
                return res


if __name__ == '__main__':
    main()
