import requests
import re

from bs4 import BeautifulSoup
from pprint import pprint


class Rental:
    def __init__(self, url, address, cost, bedrooms):
        self.url = url
        self.address = address
        self.cost = cost
        self.bedrooms = bedrooms

    def __str__(self) -> str:
        return f"Location: {self.address} \nCost: {self.cost} \nBedrooms: {self.bedrooms}"


def getRentalsDaft(daftUrl):
    daftWebsite = requests.get(daftUrl)

    soup = BeautifulSoup(daftWebsite.text, "html5lib")

    #print(soup.prettify())

    def findRentalListings(href):
        return href and re.compile("for-rent/").search(href)

    linksInPage = soup.find_all(href=findRentalListings)

    # print(linksInPage)

    for rentalHTML in linksInPage:
        price = getPrice(rentalHTML)
        url = getUrl(rentalHTML)
        bedrooms = getBedrooms(rentalHTML)
        address = getAddress(rentalHTML)
        rental = Rental(
            url,
            address,
            price,
            bedrooms,
        )
        print(rental)

        # print(rentalHTML.prettify())


def getPrice(rentalHTML) -> int:

    infoHTML = rentalHTML.find(
        'span', {"class": "TitleBlock__StyledSpan-sc-1avkvav-5 fKAzIL"})
    costWithComma = re.findall(r'[0-9],[0-9]+', infoHTML.text)
    cost = re.sub(r',', '', costWithComma[0])
    cost = int(cost)
    return cost


def getUrl(rentalHTML) -> str:

    endingURL = rentalHTML.get("href")
    fullURL = "https://www.daft.ie" + endingURL
    return fullURL


def getBedrooms(rentalHTML) -> int:
    infoHTML = rentalHTML.find('p', {"data-testid": "beds"})
    beds = re.findall(r'[0-9]', infoHTML.text)
    beds = int(beds[0])
    return beds


def getAddress(rentalHTML) -> int:
    infoHTML = rentalHTML.find('p', {"data-testid": "address"})
    address = infoHTML.text
    return address


if __name__ == "__main__":
    getRentalsDaft(
        "https://www.daft.ie/property-for-rent/dun-laoghaire-dublin/apartments"
        # "https://www.daft.ie/property-for-rent/dublin-city?from=40&pageSize=20"
    )
