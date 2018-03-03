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

import aiohttp
from commons import (
    attachments_urls,
    fetch_mail_attach,
    fetch_url,
    get_new_attach_urls
)
from consts import ATTACH_URL, __defaults__
from collections import ChainMap
from args import get_args


log = logging.getLogger()


def main():
    # all options
    args = {k: v for k, v in vars(get_args()).items() if v}
    options = ChainMap(args, os.environ, __defaults__)

    # Logging
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    # stdout log
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(formatter)
    stdout.setLevel(options["log"])
    log.addHandler(stdout)

    # asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mails_attach(options))
    loop.close()


async def mails_attach(options):
    store_path = options["UNTROUBLED_STORE_PATH"]
    cache_path = options["UNTROUBLED_CACHE_PATH"]
    timeout = options["UNTROUBLED_TIMEOUT"]

    async with aiohttp.ClientSession() as session:
        html = await fetch_url(session, ATTACH_URL, timeout)
        log.debug("Got attachments url {!r}".format(ATTACH_URL))
        urls = attachments_urls(html)
        log.debug("urls in attachments page {}".format(len(urls)))
        urls = get_new_attach_urls(urls, cache_path)
        tasks = [fetch_mail_attach(
            store_path,
            session,
            url,
            timeout) for url in urls]
        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    main()
