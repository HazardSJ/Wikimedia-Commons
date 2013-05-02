#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Published by Hazard-SJ (https://www.wikidata.org/wiki/User:Hazard-SJ)
# under the terms of Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
# https://creativecommons.org/licenses/by-sa/3.0/

import os
import oursql

class PopulateTables(object):
    def __init__(self, dbname):
        if dbname.endswith("p"):
            self.dbname = dbname[:-2]
        else:
            self.dbname = dbname
        self.sourceDB = oursql.connect(
            db = self.dbname + "_p",
            host = self.dbname + "-p.rrdb.toolserver.org",
            read_default_file = os.path.expanduser("~/.my.cnf"),
            charset = None,
            use_unicode = False
            )
        self.targetDB = oursql.connect(
            db = "u_hazard_files_p",
            host = "sql-s1-user.toolserver.org",
            read_default_file = os.path.expanduser("~/.my.cnf"),
            charset = None,
            use_unicode = False
            )

    def getStartPoint(self):
        """This always returns None for some reason"""
        cursor = self.targetDB.cursor()
        query = """
            SELECT max(timestamp)
            FROM %s;
            """ % self.dbname
        result = cursor.execute(query)
        #return int(result)

    def getData(self):
        cursor = self.sourceDB.cursor()
        query = """
            SELECT img_sha1, img_name, img_timestamp
            FROM image
            WHERE img_timestamp > ?
            ORDER BY img_timestamp
            LIMIT 100;
            """
        newLast = 0  # until self.getStartPoint is fixed...
        fetch = True
        while fetch:
            oldLast = newLast
            cursor.execute(query, (newLast,))
            for result in cursor:
                newLast = result[2]
                print result
                yield result
            if oldLast == newLast:
                fetch = False

    def putData(self):
        cursor = self.targetDB.cursor()
        query = """
            INSERT INTO `u_hazard_files_p`.`%s` SET
            `sha1` = ?,
            `name` = ?,
            `timestamp` = ?,
            `checked` = CURRENT_TIMESTAMP;
            """ % self.dbname
        data = self.getData()
        for datum in data:
            try:
                cursor.execute(query, (datum[0], datum[1], datum[2]))
            except oursql.IntegrityError:
                pass  # possible duplicate; don't wont those in the tables


def main():
    bot = PopulateTables(raw_input(u"Please enter the database name: "))
    bot.putData()

if __name__ == '__main__':
    main()
