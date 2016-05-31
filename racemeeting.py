from pyquery import PyQuery as pq
import pandas as pd
# import psycopg2
import argparse
import os
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, nargs="+")
parser.add_argument('-e', '--extension', default='',
                    help='File extension to filter by.')

args = parser.parse_args()
name_pattern = "*" + args.extension
my_dir = args.path[0]

for dir_path, subdir_list, file_list in os.walk(my_dir):
    for name_pattern in file_list:
        full_path = os.path.join(dir_path, name_pattern)
        print(full_path)
        print(file_list)

meetattrs = ('id', 'venue', 'date', 'rail', 'weather', 'trackcondition')
raceattrs = ('id', 'meeting_id', 'number', 'shortname', 'stage', 'distance',
             'grade', 'age', 'weightcondition', 'fastesttime', 'sectionaltime')
horseattrs = ('id', 'race_id', 'horse', 'number', 'finished', 'age', 'sex',
              'blinkers', 'trainernumber', 'career', 'thistrack', 'firstup',
              'secondup', 'variedweight', 'weight', 'pricestarting')

m_frames = pd.DataFrame()
r_frames = pd.DataFrame()
h_frames = pd.DataFrame()

for filename in sorted(file_list):
    for meeting in pq(filename=my_dir + filename):
        meetdata = [meeting.get(attr) for attr in meetattrs]
        meetFrame = pd.DataFrame(meetdata)
        meetFrame = meetFrame.transpose()
        m_frames = m_frames.append(meetFrame)
        for race in meeting.findall("race"):
            race.set("meeting_id", meeting.get("id"))
            racedata = [race.get(attr) for attr in raceattrs]
            raceFrame = pd.DataFrame(racedata)
            raceFrame = raceFrame.transpose()
            r_frames = r_frames.append(raceFrame)
            for horse in race.findall("nomination"):
                horse.set("race_id", race.get("id"))
                horsedata = [horse.get(attr) for attr in horseattrs]
                horseFrame = pd.DataFrame(horsedata)
                horseFrame = horseFrame.transpose()
                h_frames = h_frames.append(horseFrame)


m_frames.columns = meetattrs
r_frames.columns = raceattrs
h_frames.columns = horseattrs

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
meet = '/home/sayth/' + 'meeting' + '_' + stamp + '.csv'
race = '/home/sayth/' + 'race' + '_' + stamp + '.csv'
horse = '/home/sayth/' + 'horse' + '_' + stamp + '.csv'
m_frames.to_csv( str(meet), sep=',', encoding='utf-8')
r_frames.to_csv( str(race), sep=',', encoding='utf-8')
h_frames.to_csv( str(horse), sep=',', encoding='utf-8')
# print(meetFrame)
# print(raceFrame)
# print(horseFrame)
# conn = psycopg2.connect("")
# with conn, conn.cursor() as cur:
#         # First, create tables.
#     cur.execute("drop table if exists meetings, races, horses")
#     cur.execute("create table meetings ( " +
#                 ", ".join("%s varchar" % fld for fld in meetattrs)
#                 + ")")
#     cur.execute("create table races (" +
#                 ", ".join("%s varchar" % fld for fld in raceattrs)
#                 + ")")
#     cur.execute("create table horses (" +
#                 ", ".join("%s varchar" % fld for fld in horseattrs)
#                 + ")")
#
#     # Now walk the tree and insert data.
#     for filename in sorted(file_list):
#         for meeting in pq(filename=my_dir + filename):
#             meetdata = [meeting.get(attr) for attr in meetattrs]
#             cur.execute("insert into meetings values (" +
#                         ",".join(["%s"] * len(meetattrs)) + ")", meetdata)
#             for race in meeting.findall("race"):
#                 race.set("meeting_id", meeting.get("id"))
#                 racedata = [race.get(attr) for attr in raceattrs]
#                 cur.execute("insert into races values (" +
#                             ",".join(["%s"] * len(raceattrs)) + ")", racedata)
#                 for horse in race.findall("nomination"):
#                     horse.set("race_id", race.get("id"))
#                     horsedata = [horse.get(attr) for attr in horseattrs]
#                     cur.execute("insert into horses values (" +
#                                 ",".join(["%s"] * len(horseattrs)) + ")",
#                                 horsedata)
