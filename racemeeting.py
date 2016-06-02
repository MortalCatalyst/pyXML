from pyquery import PyQuery as pq
import pandas as pd
# import psycopg2
import argparse
import os
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, nargs="+")
parser.add_argument('-e',
                    '--extension',
                    default='',
                    help='File extension to filter by.')

args = parser.parse_args()
name_pattern = "*" + args.extension
my_dir = args.path[0]

for dir_path, subdir_list, file_list in os.walk(my_dir):
    for name_pattern in file_list:
        full_path = os.path.join(dir_path, name_pattern)

meetattrs = ('id', 'venue', 'date', 'rail', 'weather', 'trackcondition',
             'barriertrial')
raceattrs = ('id', 'meeting_id', 'number', 'shortname', 'stage', 'distance',
             'grade', 'age', 'weightcondition', 'fastesttime', 'sectionaltime',
             'stage', 'name', 'time')
horseattrs = ('id', 'race_id', 'horse', 'number', 'finished', 'blinkers',
              'trainernumber', 'jockeynumber', 'career', 'thistrack',
              'thisdistance', 'firstup', 'secondup', 'goodtrack', 'heavytrack',
              'fasttrack', 'variedweight', 'weight', 'rating', 'pricestarting',
              'decimalmargin', 'barrier')
horsedetails = ('id', 'horse', 'sex', 'dob', 'description', 'age')
trainerdetails = ('trainernumber', 'trainersurname', 'trainertrack',
                  'rsbtrainername')
jockeydetails = ('jockeynumber', 'jockeysurname', 'jockeyfirstname')

# attrList = [meetattrs, raceattrs, horseattrs, horsedetails, trainerdetails,
# jockeydetails]

# pathItems = ['race','id','nomination']

m_frames = pd.DataFrame()
r_frames = pd.DataFrame()
h_frames = pd.DataFrame()
hd_frames = pd.DataFrame()
td_frames = pd.DataFrame()
jd_frames = pd.DataFrame()
# x_frames = pd.DataFrame()

# def RaceCSV(xmlList=attrList, filetoParse=file_list):
#     """module to reduce the for loops"""
#     for filename in sorted(filetoParse):
#         for item in pq(filename=my_dir + filename):
#             itemData = [item.get(attr) for attr in item]
#             itemFrame = pd.DataFrame(itemData)
#             itemFrame = itemFrame.transpose()
#             x_frames = x_frames.append(itemFrame)
#             pathCount = 0
#             for detail in item.findall(pathItems[pathCount]):
#

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
meet = 'meeting' + '_' + stamp + '.csv'
raceName = 'race' + '_' + stamp + '.csv'
horseName = 'horse' + '_' + stamp + '.csv'
hdetail = 'hdetail' + '_' + stamp + '.csv'
trainer = 'trainer' + '_' + stamp + '.csv'
jockey = 'jockey' + '_' + stamp + '.csv'


def writeFile(file, frame):
    """Take a frame and write it to csv.

    making this D400 compliant
    """
    print('Processed...' + str(file))
    directory = '/home/sayth/Output'
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
    file = os.path.join(directory, file)
    frame.to_csv(str(file), sep=',', encoding='utf-8')

# filenamesToWrite = [meet, race, horse, hdetail, trainer, jockey]
# frames = [m_frames, r_frames, h_frames, hd_frames, td_frames, jd_frames]

screenOutput = 0

for filename in sorted(file_list):
    for meeting in pq(filename=my_dir + filename):
        meetdata = [meeting.get(attr) for attr in meetattrs]
        meetFrame = pd.DataFrame(meetdata)
        meetFrame = meetFrame.transpose()
        print(meetFrame)
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
                for hdetails in race.findall("nomination"):
                    hdetailsdata = [hdetails.get(attr)
                                    for attr in horsedetails]
                    hdetailsFrame = pd.DataFrame(hdetailsdata)
                    hdetailsFrame = hdetailsFrame.transpose()
                    hd_frames = hd_frames.append(hdetailsFrame)

for filename in sorted(file_list):
    for meeting in pq(filename=my_dir + filename):
        for tdetails in race.findall("nomination"):
            trainerdata = [tdetails.get(attr) for attr in trainerdetails]
            tdetailsFrame = pd.DataFrame(trainerdata)
            tdetailsFrame = tdetailsFrame.transpose()
            td_frames = td_frames.append(tdetailsFrame)
            for jdetails in race.findall("nomination"):
                jockeydata = [jdetails.get(attr) for attr in jockeydetails]
                jdetailsFrame = pd.DataFrame(jockeydata)
                jdetailsFrame = jdetailsFrame.transpose()
                jd_frames = jd_frames.append(jdetailsFrame)

m_frames.columns = meetattrs
writeFile(meet, m_frames)
r_frames.columns = raceattrs
writeFile(raceName, r_frames)
h_frames.columns = horseattrs
writeFile(horseName, h_frames)
hd_frames.columns = horsedetails
writeFile(hdetail, hd_frames)
td_frames.columns = trainerdetails
writeFile(trainer, td_frames)
jd_frames.columns = jockeydetails
writeFile(jockey, jd_frames)
# for fname in filenamesToWrite:
#     print('Processed...' + filenamesToWrite.index(file))
#     for frame in frames:
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#     fname = os.path.join(directory, fname)
#     frame.to_csv(fname, sep=',', encoding='utf-8')

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
#                             ",".join(["%s"] * len(raceattrs)) + ")",racedata)
#                 for horse in race.findall("nomination"):
#                     horse.set("race_id", race.get("id"))
#                     horsedata = [horse.get(attr) for attr in horseattrs]
#                     cur.execute("insert into horses values (" +
#                                 ",".join(["%s"] * len(horseattrs)) + ")",
#                                 horsedata)
