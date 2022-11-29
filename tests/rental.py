import pytest

from ..src.rental import findNewestRentals
from ..src.folder_util import loadJsonFile


def test_app_health():

    olderRentals = loadJsonFile(
        "archive/dublin-city|2022-11-21 15:08:56.557176.json")

    newRental = loadJsonFile(
        "archive/dublin-city|2022-11-21 15:41:36.565252.json")

    findNewestRentals(olderRentals, newRental)