#!/usr/bin/env python
# -*- coding: utf-8 -*-


import async_timeout
import asyncio
import os

import aiohttp
from bs4 import BeautifulSoup

from consts import ATTACH_URL, BASE_PATH, TIMEOUT


async def fetch_url(session, url):
    with async_timeout.timeout(TIMEOUT):
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise


async def fetch_mail_attach(session, url):
    p = os.path.join(BASE_PATH, os.path.basename(url))
    response = await fetch_url(session, url)
    save_mail(response, p)


def save_mail(data, path):
    with open(path, "wb") as f:
        f.write(data)


def attachments_urls(html):
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.findAll('tr'):
        if item.a:
            urls.append(ATTACH_URL + item.a.get("href"))
    else:
        return urls