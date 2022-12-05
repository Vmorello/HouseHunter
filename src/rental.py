import requests
import re
import json

from pprint import pprint
from datetime import datetime
from bs4 import BeautifulSoup
from splinter import Browser


class RentalSearch:
    def __init__(self, entries=None):
        if entries == None:
            self.allRentals = []
            return
        self.allRentals = entries.copy()
        #print(self.allRentals)

    @property
    def fullList(self):
        return self.allRentals

    @property
    def URLs(self):
        return [rental["url"] for rental in self.allRentals]

    # def __str__(self) -> str:
    #     full_str = ''
    #     for rental in self.allRentals:
    #         full_str = full_str + str(rental)
    #     return full_str

    def saveJson(self, location):
        # rentalCollection = []
        # for rental in self.allRentals:
        #     rentalCollection.append(rental.toJson())
        with open(f'archive/{location}|{datetime.utcnow()}.json',
                  'w') as json_file:
            json.dump(self.allRentals, json_file)

    def getRentalsDaft(self, daftUrl):
        daftWebsite = requests.get(daftUrl, timeout=10)

        rentalSearchPage = BeautifulSoup(daftWebsite.text, "html5lib")

        def findRentalListings(href):
            return href and re.compile("/for-rent/").search(href)

        linksInPage = rentalSearchPage.find_all(href=findRentalListings)

        for rentalHTML in linksInPage:

            # print(rentalHTML.prettify())
            try:
                price = self.getPrice(rentalHTML)
                url = self.getUrl(rentalHTML)
                bedrooms = self.getBedrooms(rentalHTML)
                address = self.getAddress(url)

                rental = {
                    "url": url,
                    "address": address,
                    "price": price,
                    "bedrooms": bedrooms,
                }
                self.allRentals.append(rental)
            except IndexError as e:
                pass

    def getPrice(self, rentalHTML) -> int:
        try:
            priceHTML = rentalHTML.find(
                'span',
                {"class": "TitleBlock__StyledSpan-sc-1avkvav-5 fKAzIL"})
            # pprint(priceHTML)
            price = priceHTML.text
        except AttributeError:
            priceHTML = rentalHTML.find(
                'p', {"class": "SubUnit__Title-sc-10x486s-5 feGTKf"})
            # pprint(priceHTML)
            price = priceHTML.text

        costWithComma = re.findall(r'[0-9],[0-9]+|[0-9]+', price)
        cost = re.sub(r',', '', costWithComma[0])
        cost = int(cost)

        return cost

    def getUrl(self, rentalHTML) -> str:

        endingURL = rentalHTML.get("href")
        fullURL = "https://www.daft.ie" + endingURL
        return fullURL

    def getBedrooms(self, rentalHTML) -> int:
        try:
            bedHTML = rentalHTML.find('p', {"data-testid": "beds"})
            beds = re.findall(r'[0-9]', bedHTML.text)
            beds = beds[0]
        except AttributeError:
            try:
                bedHTML = rentalHTML.find(
                    'div',
                    {"class": "SubUnit__CardInfoItem-sc-10x486s-7 YYbRy"})
                beds = re.findall(r'[0-9]', bedHTML.text)
                beds = beds[0]
            except AttributeError:
                beds = "Probably studio"
        return beds

    def getAddress(self, url) -> int:
        address = url.split("/")[4]
        address = re.sub(r'apartment|house|studio', '', address)
        address = re.sub(r'-', ' ', address)

        return address


class Rental:
    def __init__(self, input: dict):

        self.url = input["url"]
        self.address = input["address"]
        self.price = input["price"]
        self.bedrooms = input["bedrooms"]

    def getDetailedInfo(self):
        daftWebsite = requests.get(self.url)

        singlePageHtml = BeautifulSoup(daftWebsite.text, "html5lib")

        self.scrapingFacilities(singlePageHtml)
        self.scrapingOverview(singlePageHtml)
        self.getPostalNumber()
        self.makeDecision()

        # print(singlePageHtml.prettify())

    def scrapingFacilities(self, singlePageHtml):
        self.facility = []
        rentalFacilities = singlePageHtml.find_all(
            'li', {
                "class":
                "PropertyDetailsList__PropertyDetailsListItem-sc-1cjwtjz-1 hqJwsU"
            })
        for facility in rentalFacilities:
            self.facility.append(facility.text)

        # pprint(self.facility)

    def scrapingOverview(self, singlePageHtml):
        overviewDetails = singlePageHtml.find_all(
            'span', {
                "class": "styles__ListLabel-sc-15fxapi-10 dDvqlf",
            })
        for line in overviewDetails:
            detail = line.parent.text
            # print(detail)
            if detail.startswith("Available From:"):
                self.availableFrom = detail.split(":")[1]
            if detail.startswith("Furnished:"):
                self.furnished = detail.split(":")[1]

    def getPostalNumber(self):
        try:
            postalNumber = re.findall(r"Dublin \d+", self.address)[0]
            postalNumber = postalNumber.split(" ")[1]
            self.postalNumber = int(postalNumber)
        except Exception:
            self.postalNumber = "unknown"

    def toDict(self):
        return {
            "url": self.url,
            "address": self.address,
            "price": self.price,
            "available from": self.availableFrom,
            "postal": self.postalNumber,
            "bedrooms": self.bedrooms,
            "furnished": self.furnished,
            "facilities": self.facility,
            "Send email": self.sendEmailFlag,
        }

    def makeDecision(self):
        basePrice = 2000
        if "Dishwasher" in self.facility:
            basePrice += 100
        if self.postalNumber in [2, 8, 6, 4]:
            basePrice += 100
        if basePrice >= self.price:
            self.sendEmailFlag = True
        else:
            self.sendEmailFlag = False

    def sendEmail(self):
        browser = Browser('firefox')
        browser.visit('http://google.com')
        pass


##===== utils functions=====
def findNewestRentals(olderRentalSeach, newerRentals):
    lastCheckedEntryURLs = olderRentalSeach.URLs

    unprocessedRentals = []
    for item in newerRentals.fullList:
        if (item["url"] in lastCheckedEntryURLs):
            break
        unprocessedRentals.append(item)

    return unprocessedRentals
    pprint(unprocessedRentals)