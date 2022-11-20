import requests
import re
import json

from pprint import pprint
from datetime import datetime
from bs4 import BeautifulSoup


class Rentals:
    def __init__(self, values=[]):
        self.allRentals = values

    def __str__(self) -> str:
        full_str = ''
        for rental in self.allRentals:
            full_str = full_str + str(rental)
        return full_str

    def saveJson(self, location):
        rentalCollection = []
        for rental in self.allRentals:
            rentalCollection.append(rental)
        with open(f'archive/{location}|{datetime.utcnow()}.json',
                  'w') as json_file:
            json.dump(rentalCollection, json_file)

    def getRentalsDaft(self, daftUrl):
        daftWebsite = requests.get(daftUrl)

        soup = BeautifulSoup(daftWebsite.text, "html5lib")

        # linksInPage = soup.find_all("a")
        # for rentalHTML in linksInPage:
        #     print(rentalHTML.prettify())

        def findRentalListings(href):
            return href and re.compile("/for-rent/").search(href)

        linksInPage = soup.find_all(href=findRentalListings)

        for rentalHTML in linksInPage:

            # print(rentalHTML.prettify())

            price = self.getPrice(rentalHTML)
            url = self.getUrl(rentalHTML)
            bedrooms = self.getBedrooms(rentalHTML)
            address = self.getAddress(rentalHTML)

            rental = {
                "url": url,
                "address": address,
                "price": price,
                "bedrooms": bedrooms,
            }
            self.allRentals.append(rental)

    def getPrice(self, rentalHTML) -> int:

        infoHTML = rentalHTML.find(
            'span', {"class": "TitleBlock__StyledSpan-sc-1avkvav-5 fKAzIL"})
        costWithComma = re.findall(r'[0-9],[0-9]+|[0-9]+', infoHTML.text)
        cost = re.sub(r',', '', costWithComma[0])
        cost = int(cost)
        return cost

    def getUrl(self, rentalHTML) -> str:

        endingURL = rentalHTML.get("href")
        fullURL = "https://www.daft.ie" + endingURL
        return fullURL

    def getBedrooms(self, rentalHTML) -> int:
        try:
            infoHTML = rentalHTML.find('p', {"data-testid": "beds"})
            beds = re.findall(r'[0-9]', infoHTML.text)
            beds = beds[0]
        except AttributeError:
            beds = "Probably studio"
        return beds

    def getAddress(self, rentalHTML) -> int:
        infoHTML = rentalHTML.find('p', {"data-testid": "address"})
        address = infoHTML.text
        return address


# class Rental:
#     def __init__(self, url, address, cost, bedrooms):
#         self.url = url
#         self.address = address
#         self.cost = cost
#         self.bedrooms = bedrooms

#     def loadJson(self, jsonInput):
#         print(jsonInput)

#     def toDict(self):
#         return {
#             "url": self.url,
#             "address": self.address,
#             "cost": self.cost,
#             "bedrooms": self.bedrooms
#         }

#     def toJson(self):
#         return json.dump(self.toDict())

#     def __str__(self) -> str:
#         return f"---------\nLocation: {self.address} \nCost: {self.cost} \nBedrooms: {self.bedrooms} \nLink: {self.url}\n"
