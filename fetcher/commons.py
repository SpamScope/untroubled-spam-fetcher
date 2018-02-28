#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio
import async_timeout

import aiohttp
from aiohttp.web import HTTPNotFound
from bs4 import BeautifulSoup

from consts import ATTACH_URL


async def fetch_page(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            if response.status == 200:
                response = await response.read()
                return attachments_urls(response)
            elif response.status == 404:
                raise HTTPNotFound()
            else:
                raise


def attachments_urls(html):
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.findAll('tr'):
        if item.a:
            urls.append(ATTACH_URL + item.a.get("href"))
    else:
        return urls
