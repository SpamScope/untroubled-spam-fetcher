#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import logging
import os

from bs4 import BeautifulSoup

import aiohttp
import async_timeout
from consts import ATTACH_URL, STORE_PATH, TIMEOUT

log = logging.getLogger(__name__)


async def fetch_url(session, url):
    with async_timeout.timeout(TIMEOUT):
        async with session.get(url) as response:
            if response.status == 200:
                log.debug("Got url {!r}".format(url))
                return await response.read()
            else:
                log.exception()("Failed getting url {!r}".format(url))
                raise


async def fetch_mail_attach(session, url):
    p = os.path.join(STORE_PATH, os.path.basename(url))
    response = await fetch_url(session, url)
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
        return urls
