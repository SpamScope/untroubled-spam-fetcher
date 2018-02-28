#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio

import aiohttp

from consts import ATTACH_URL
from commons import fetch_page


# for i in mail_urls[1:]:
    # path = join("/mnt/spamscope/mailboxes/untroubled.org", basename(i))
    # r = requests.get(i, stream=True)
    # if r.status_code == 200:
        # print("Downloaded {!r}".format(i))
        # with open(path, 'wb') as f:
            # r.raw.decode_content = True
            # shutil.copyfileobj(r.raw, f)

async def main():
    async with aiohttp.ClientSession() as session:
        urls = await fetch_page(session, ATTACH_URL)
        print(urls)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
