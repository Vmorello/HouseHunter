import pytest

from pprint import pprint

from src.rental import findNewestRentals
from src.folder_util import loadJsonFile


def test_find_rental_search_comparision():

    olderRentals = loadJsonFile(
        "archive/dublin-city|2022-11-21 15:08:56.557176.json")

    newRental = loadJsonFile(
        "archive/dublin-city|2022-11-21 15:41:36.565252.json")

    differances = findNewestRentals(olderRentals, newRental)

    pprint(differances)

    assert len(differances) > 0


def test_last_url_expired():
    olderRentals = loadJsonFile(
        "archive/dublin-city|2022-11-29 15:55:09.599652.json")

    newRental = loadJsonFile(
        "archive/dublin-city|2022-11-29 16:05:10.564924.json")

    differances = findNewestRentals(olderRentals, newRental)

    pprint(differances)

    assert len(differances) < 20
