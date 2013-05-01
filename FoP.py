#!/usr/bin/python
# -*- coding: utf-8  -*-
import catlib
import pagegenerators
import re
import wikipedia

site = wikipedia.getSite("commons", "commons")

source_cat = catlib.Category(site, u"Category:Work by Mattes 2012")

germany_cat = catlib.Category(site, u"Category:User:Mattes/Contributions/Topics/Germany")
germany_cats = [germany_cat]
germany_cats.extend([subcat for subcat in germany_cat.subcategoriesList()])

switzerland_cat = catlib.Category(site, u"Category:User:Mattes/Contributions/Topics/Switzerland")
switzerland_cats = [switzerland_cat]
switzerland_cats.extend([subcat for subcat in switzerland_cat.subcategoriesList()])

oldcat = catlib.Category(site, u"Category:FOP")

def main():
  gen = pagegenerators.ImageGenerator(pagegenerators.NamespaceFilterPageGenerator(pagegenerators.CategorizedPageGenerator(source_cat),[6]))
  for page in gen:
    image = page
    page = wikipedia.Page(site, page.title())
    if not (image.getFileVersionHistory()[0][1] == u"Mattes"):
      continue
    cats = page.categories()
    text = ""
    if not oldcat in cats:
      continue
    g = False
    s = False
    if list(set(cats) & set(germany_cats)):
      g = True
    if list(set(cats) & set(switzerland_cats)):
      s = True
    if g or s:
      text = page.get()
      oldtext = text
      if g:
        if not re.search(ur"\{\{FoP-Germany\}\}", text, re.I):
          text = u"{{FoP-Germany}}\n" + text
          summary = ur"Bot: Added {{[[Template:FoP-Germany|FoP-Germany]]}}"
      if s:
        if not re.search(ur"\{\{FoP-Switzerland\}\}", text, re.I):
          text = u"{{FoP-Switzerland}}\n" + text
          summary = ur"Bot: Added {{[[Template:FoP-Switzerland|FoP-Switzerland]]}}"
      oldtext2 = text
      text = wikipedia.replaceCategoryInPlace(text, oldcat, None)
      if text != oldtext2:
        summary += ur"; removed [[:Category:FOP]]"
    if text != oldtext:
      page.put(text, comment=summary)
  return

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
