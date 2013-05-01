#!/usr/bin/python
# -*- coding: utf-8 -*-


import wikipedia as pywikibot
import time


class Sandbot(object):
    def __init__(self):
        self.sandbots = [u'Hazard-Bot', u'O (bot)']
        self.config = {u'Commons:Sandbox': 'general'}
        self.sandboxes = self.config.keys()
        self.sandboxes.sort()
        self.recheck = list() # Just in case we need to recheck one or more sandboxes
        self.content = {'general': u'{{Sandbox}}\n<!-- Please edit only below this line. -->'}
        self.editsummary = u'[[Commons:Bots|Robot]]: Cleaning the sandbox'
        self.site = pywikibot.getSite()
        #self.shutoffpage = pywikibot.Page(self.site, u'User:Hazard-Bot/Check/Sandbot')
        self.delay = 5

    def shutoffcheck(self):
        return # Not implemented
        print u'Checking emergency shutoff page %s.' % self.shutoffpage.title(asLink=True)
        self.shutoffpagetext = self.shutoffpage.get()
        if unicode(self.shutoffpagetext.strip()) != u'enable':
            print u'Emergency shutoff enabled; stopping.'
            pywikibot.stopme()
            exit()
        else:
            print u'Emergency shutoff disabled; continuing.'

    def run(self):
        self.shutoffcheck()

        # From clean_user_sandbox.py in the Python Wikipedia Robot Framework
        def minutesDiff(time1, time2):
            if type(time1) in [long, int]:
                time1 = str(time1)
            if type(time2) in [long, int]:
                time2 = str(time2)
            t1 = (((int(time1[0:4]) * 12 + int(time1[4:6])) * 30 +
                   int(time1[6:8])) * 24 + int(time1[8:10])) * 60 + \
                   int(time1[10:12])
            t2 = (((int(time2[0:4]) * 12 + int(time2[4:6])) * 30 +
                   int(time2[6:8])) * 24 + int(time2[8:10])) * 60 + \
                   int(time2[10:12])
            return abs(t2-t1)

        def cleanSandbox(titles):
            self.recheck = list()
            for title in titles:
                sandbox = pywikibot.Page(self.site, title)
                try:
                    text = sandbox.get()
                    if text.strip() == self.content[self.config[title]].strip():
                        print u'Skipping [[%s]]: Sandbox is clean' % title
                        continue
                    elif sandbox.userName() in self.sandbots:
                        print u'Skipping [[%s]]: Sandbot version' % title
                        continue
                    else:
                        diff = minutesDiff(sandbox.editTime(), time.strftime("%Y%m%d%H%M%S", time.gmtime()))
                        if diff >= self.delay:
                            try:
                                sandbox.put(self.content[self.config[title]], comment=self.editsummary)
                            except pywikibot.EditConflict:
                                self.recheck.append(title)
                                print u'Delaying [[%s]]: Edit conflict encountered' % title
                        else:
                            self.recheck.append(title)
                            print u'Delaying [[%s]]: Sandbox may still be in use' % title
                except pywikibot.NoPage:
                    print u'Skipping [[%s]]: Nonexistent sandbox' % title

        cleanSandbox(self.sandboxes)
        while len(self.recheck) > 0:
            print u'Pausing to recheck %i sandboxes %s' % (len(self.recheck), tuple(self.recheck))
            time.sleep(self.delay * 60)
            cleanSandbox(self.recheck)


def main():
    bot = Sandbot()
    bot.run()


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
