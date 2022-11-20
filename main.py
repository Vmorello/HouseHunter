from src.rental import Rentals
from src.folder_util import findLastest, loadJsonFile


def scrapeDaft(location="dublin-city"):
    newRentals = Rentals()
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

    lastestFile = findLastest()
    olderRentals = loadJsonFile("archive/" + lastestFile)

    newRental = scrapeDaft()
