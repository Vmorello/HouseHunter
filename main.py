import time

from src.rental import RentalSearch, Rental, findNewestRentals
from src.folder_util import findLastest, loadJsonFile

from datetime import datetime
from pprint import pprint


def scrapeDaft(location="dublin-city"):

    newRentals = RentalSearch()

    #pprint(newRentals.fullList)
    newRentals.getRentalsDaft(
        #"https://www.daft.ie/property-for-rent/dun-laoghaire-dublin?sort=publishDateDesc"
        f"https://www.daft.ie/property-for-rent/{location}?sort=publishDateDesc"
        # "https://www.daft.ie/property-for-rent/dublin-city"
        #"https://www.daft.ie/property-for-rent/south-dublin-city-dublin"
    )
    newRentals.saveJson(location)

    # print(newRentals)
    return newRentals


if __name__ == "__main__":

    while (True):
        print(f"------ starting a run at {datetime.now()}")
        lastestFile = findLastest()
        olderRentals = loadJsonFile("archive/" + lastestFile)

        newRental = scrapeDaft()

        unprocessedRentals = findNewestRentals(olderRentals, newRental)

        # unprocessedRentals = [{
        #     'address':
        #     'Gardiner Place, Dublin 1',
        #     'bedrooms':
        #     '2',
        #     'price':
        #     1950,
        #     'url':
        #     'https://www.daft.ie/for-rent/apartment-gardiner-place-dublin-1/4527116'
        # }]

        # pprint(newRental.fullList)

        for newRental in unprocessedRentals:
            rental = Rental(newRental)
            rental.getDetailedInfo()
            pprint(rental.toDict())
            # rental.sendEmail()

        time.sleep(600)
