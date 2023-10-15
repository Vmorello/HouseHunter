import os
import ast

from datetime import datetime
from pprint import pprint

from .rental import RentalSearch


def findLastest(location, source="archive/" ):

    latestDate = datetime.strptime('2011-01-21 01:01:01', '%Y-%m-%d %H:%M:%S')
    latestFilename = ""

    for file in os.listdir(source):
        try:
            date = extractDateFromFileName(file)
        except TypeError:
            continue

        utcDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        if utcDate > latestDate:
            latestDate = utcDate
            latestFilename = file

    return latestFilename


def extractDateFromFileName(file:str):
    try:
        date = file.split("_")[1]
        date = date.split(".")[0]
    except IndexError:
        #print("non-dated itemed")
        raise TypeError
    return date


def loadJsonFile(jsonFile):
    with open(jsonFile, "r") as f:
        for line in f:
            rentalList = ast.literal_eval(line)
    rentals = RentalSearch(rentalList)
    #pprint(rentalList)
    return rentals
