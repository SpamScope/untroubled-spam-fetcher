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


import logging
import os
import json

from bs4 import BeautifulSoup

import async_timeout
from consts import ATTACH_URL

log = logging.getLogger(__name__)


async def fetch_url(session, url, timeout):
    with async_timeout.timeout(timeout):
        async with session.get(url) as response:
            if response.status == 200:
                log.debug("Got url {!r}".format(url))
                return await response.read()
            else:
                log.exception()("Failed getting url {!r}".format(url))
                raise


async def fetch_mail_attach(store_path, session, url, timeout):
    p = os.path.join(store_path, os.path.basename(url))
    response = await fetch_url(session, url, timeout)
    save_mail(response, p)


def save_mail(data, path):
    with open(path, "wb") as f:
        f.write(data)
        log.debug("Saved mail in path {!r}".format(path))


def attachments_urls(html):
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.findAll('tr'):
        if item.a:
            urls.append(ATTACH_URL + item.a.get("href"))
    else:
        return urls[1:]


def get_new_attach_urls(urls, cache_path):
    cache = os.path.join(cache_path, ".untroubled-attach-cache")

    try:
        with open(cache) as f:
            cache_urls = json.loads(f.read())
            log.debug("{} already stored".format(len(cache_urls)))

    except FileNotFoundError:
        save_in_cache(cache, urls)
        return urls

    else:
        get_urls = set(urls) - set(cache_urls)
        log.debug("{} attachments urls to get".format(len(get_urls)))
        save_in_cache(cache, urls)
        return list(get_urls)


def save_in_cache(cache, urls):
    with open(cache, "w") as f:
        f.write(json.dumps(urls, indent=2))
