#!/usr/bin/python
# -*- coding: utf-8  -*-

import pagegenerators
import re
import wikipedia

site = wikipedia.getSite("commons", "commons")
source = wikipedia.Page(site, "Template:Must be substituted")

def gen():
    templates1 = pagegenerators.NamespaceFilterPageGenerator(pagegenerators.ReferringPageGenerator(source, onlyTemplateInclusion=True), [10])
    templates2 = list()
    for pg in templates1:
        page = pg
        if page.title().endswith(ur"/doc") and wikipedia.Page(site, re.sub('/doc', '', page.title())).exists():
            page = wikipedia.Page(site, re.sub('/doc', '', page.title()))
        if not ur"/" in page.title():
            templates2.append(page)
            redirects = page.getReferences(redirectsOnly=True)
            for redirect in redirects:
                templates2.append(redirect)
    return sorted(set(templates2))

def main():
    templates = gen()
    for template in templates:
        match = template.title(withNamespace=False)
        tosubst = pagegenerators.ReferringPageGenerator(template, onlyTemplateInclusion=True)
        for page in tosubst:
            text = page.get()
            oldtext = text
            text = re.sub(ur"\{\{(Template:|)%s" % match,u"{{subst:%s" % template.title(withNamespace=False), text,re.I)
            if not oldtext == text:
                try:
                    page.put(text, comment="Bot: Substituting {{[[Template:%s|%s]]}}" % (match, match))
                except:
                    print "Could not edit"
            else:
                print "No changes made"
    return


if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
