#!/usr/bin/python
# -*- coding: utf-8  -*-

import wikipedia as pywikibot
from query import GetData
from time import gmtime, strftime

site = pywikibot.getSite('commons', 'commons')

params = {
    'action': 'edit',
    'title': 'Commons:Village pump',
    'appendtext': u'\n\n= %s =' % strftime('%B %d', gmtime()),
    'token': site.getToken(),
    'summary': '[[Commons:Bots|Robot]]: Adding today\'s section header',
    'bot': 1,
    'minor': 1
    }

if __name__ == "__main__":
    try:
        GetData(params, site)
    finally:
        pywikibot.stopme()
