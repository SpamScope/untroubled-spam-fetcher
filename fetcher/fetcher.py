#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import logging
import sys

import aiohttp
from commons import attachments_urls, fetch_mail_attach, fetch_url
from consts import ATTACH_URL


# Logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)


def main():
    loop = asyncio.get_event_loop()    
    loop.run_until_complete(mails_attach())
    loop.close()


async def mails_attach():
    async with aiohttp.ClientSession() as session:
        html = await fetch_url(session, ATTACH_URL)
        log.debug("Got attachments url {!r}".format(ATTACH_URL))
        urls = attachments_urls(html)
        log.debug("urls in attachments page {}".format(len(urls)))
        tasks = [fetch_mail_attach(session, url) for url in urls[1:]]
        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    main()    