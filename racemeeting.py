from pyquery import PyQuery as pq
#import pandas as pd
import psycopg2
import argparse
import glob


def GetArgs(parser):
    '''parse XML from command line'''
    parser.add_argument("path", nargs="+")
    parser.add_argument('-e', '--extension', default='',
                        help='File extension to filter by.')
    args = parser.parse_args()

    files = set()
    name_pattern = "*" + args.extension
    for path in args.path:
        files.update(glob.glob(os.path.join(path, name_pattern)))
  return files


meetattrs = ('id', 'venue', 'date', 'rail', 'weather', 'trackcondition')
raceattrs = ('id', 'meeting_id', 'number', 'shortname', 'stage', 'distance',
             'grade', 'age', 'weightcondition', 'fastesttime', 'sectionaltime')
horseattrs = ('id', 'race_id', 'horse', 'number', 'finished', 'age', 'sex',
              'blinkers', 'trainernumber', 'career', 'thistrack', 'firstup',
              'secondup', 'variedweight', 'weight', 'pricestarting')

conn = psycopg2.connect("")
with conn, conn.cursor() as cur:
        # First, create tables.
    cur.execute("drop table if exists meetings, races, horses")
    cur.execute("create table meetings (" +
                ", ".join("%s varchar" % fld for fld in meetattrs)
                + ")")
    cur.execute("create table races (" +
                ", ".join("%s varchar" % fld for fld in raceattrs)
                + ")")
    cur.execute("create table horses (" +
                ", ".join("%s varchar" % fld for fld in horseattrs)
                + ")")

    # Now walk the tree and insert data.
    for meeting in pq(filename="20160416RAND0.xml"):
        meetdata = [meeting.get(attr) for attr in meetattrs]
        cur.execute("insert into meetings values (" +
                    ",".join(["%s"]*len(meetattrs)) + ")", meetdata)
        for race in meeting.findall("race"):
            race.set("meeting_id", meeting.get("id"))
            racedata = [race.get(attr) for attr in raceattrs]
            cur.execute("insert into races values (" +
                        ",".join(["%s"]*len(raceattrs)) + ")", racedata)
            for horse in race.findall("nomination"):
                horse.set("race_id", race.get("id"))
                horsedata = [horse.get(attr) for attr in horseattrs]
                cur.execute("insert into horses values (" +
                            ",".join(["%s"]*len(horseattrs)) + ")", horsedata)
