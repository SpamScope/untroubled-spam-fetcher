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


import async_timeout
import hashlib
import json
import logging
import os
import shutil
import tempfile

from aiohttp.client_exceptions import ClientError
from bs4 import BeautifulSoup
import patoolib


log = logging.getLogger(__name__)


def md5sum(data):
    md5 = hashlib.md5()
    md5.update(data)
    md5 = md5.hexdigest()
    return md5


async def fetch_url(session, url, timeout):
    with async_timeout.timeout(timeout):
        async with session.get(url) as response:
            if response.status == 200:
                log.debug("Got url {!r}".format(url))
                return await response.read()
            else:
                log.exception("Failed getting url {!r}".format(url))
                raise ClientError("Failed getting url {!r}".format(url))


async def fetch_mail_attach(store_path, session, url, timeout):
    p = os.path.join(store_path, os.path.basename(url))
    response = await fetch_url(session, url, timeout)
    save_mail(response, p)


async def fetch_mail_archive(cache_path, store_path, session, url, timeout):
    response = await fetch_url(session, url, timeout)
    md5 = md5sum(response)
    filename = os.path.basename(url)
    cache_md5 = os.path.join(
        cache_path, ".{}_{}".format(filename, md5))
    cache = os.path.join(
        cache_path, ".{}".format(filename))

    if not os.path.exists(cache_md5):
        log.info("New archive mails. Name: {}, md5: {}".format(filename, md5))
        temp = tempfile.mkdtemp(prefix="untroubled_")
        log.debug("Temporary folder for mail archive: {}".format(temp))
        file_7z = os.path.join(temp, filename)
        save_mail(response, file_7z)
        log.debug("7z file in {!r}".format(file_7z))
        unzip(file_7z, temp)
        move_mails(temp, store_path, cache)
        shutil.rmtree(temp)
        open(cache_md5, "w").close()
        log.debug("New cache file: {}".format(cache_md5))


def save_mail(data, path):
    with open(path, "wb") as f:
        f.write(data)
        log.debug("Saved mail in path {!r}".format(path))


def urls_to_fetch(html, base_url):
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.findAll('tr'):
        if item.a:
            urls.append(base_url + item.a.get("href"))
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


def save_in_cache(cache, items):
    with open(cache, "w") as f:
        f.write(json.dumps(items, indent=2))


def unzip(file, path):
    patoolib.extract_archive(
        file,
        outdir=path,
        verbosity=-1)
    os.remove(file)


def move_mails(mails_path, store_path, cache_file):
    mails = []
    cache = load_mails_cache(cache_file)

    for path, subdirs, files in os.walk(mails_path):
        for name in files:
            mails.append(name)

            if name not in cache:
                log.info("New name found: {!r}".format(name))
                try:
                    shutil.move(os.path.join(path, name), store_path)
                except shutil.Error:
                    pass

    save_in_cache(cache_file, mails)


def load_mails_cache(cache_file):
    try:
        with open(cache_file) as f:
            cache = json.loads(f.read())
            return cache

    except FileNotFoundError:
        return []
