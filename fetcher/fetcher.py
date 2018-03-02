#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio

import aiohttp
from commons import attachments_urls, fetch_mail_attach, fetch_url
from consts import ATTACH_URL


async def mails_attach():
    async with aiohttp.ClientSession() as session:
        html = await fetch_url(session, ATTACH_URL)
        urls = attachments_urls(html)
        tasks = [fetch_mail_attach(session, url) for url in urls[1:]]
        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(mails_attach())
    loop.run_until_complete(future)
