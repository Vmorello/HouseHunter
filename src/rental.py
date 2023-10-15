import os
import requests
import re
import json

from pprint import pprint
from datetime import datetime
from bs4 import BeautifulSoup

from .html_util import *


class RentalSearch:
    def __init__(self, entries=None):
        if entries == None:
            self.allRentals = []
            return
        self.allRentals = entries.copy()
        #print(self.allRentals)

    @property
    def report(self):
        return self.allRentals
    


    @property
    def URLs(self):
        return [rental["url"] for rental in self.allRentals]
    
    def reportOnPostal(self, postal):
        return [rental for rental in self.report if rental["postal_code"] == postal]

    def getRentalsDaft(self, daftUrl, postal_code="NA") -> None:
        daftWebsite = requests.get(daftUrl, timeout=10)

        rentalSearchPage = BeautifulSoup(daftWebsite.text, "html5lib")

        def findRentalListings(href):
            return href and re.compile("/for-rent/").search(href)

        linksInPage = rentalSearchPage.find_all(href=findRentalListings)



        for rentalHTML in linksInPage:

            # print(rentalHTML.prettify())
            try:
                price = getPrice(rentalHTML)
                url = getUrl(rentalHTML)
                bedrooms = getBedrooms(rentalHTML)
                address = getAddress(url)

                rental = {
                    "url": url,
                    "address": address,
                    "price": price,
                    "bedrooms": bedrooms,
                    "postal_code":postal_code,
                    "first_detected": str(datetime.utcnow())

                }
                self.allRentals.append(rental)
            except IndexError as e:
                pass

    def getRentalsDaftDublinPostal(self, postal_code:int)-> None:
        self.getRentalsDaft(f"https://www.daft.ie/property-for-rent/dublin-{postal_code}-dublin?sort=publishDateDesc", postal_code)

    def append_unproccesed(self, report:list)->None:
        for rental in report:
            self.allRentals.append(rental)

    
    def saveJson(self, name):
        print("going to save a json")
        if (not os.path.exists("archive/")):
            print("making archive folder")
            os.mkdir("archive/")

        with open(f'archive/{name}_{datetime.utcnow()}.json',mode='w') as json_file:
            json.dump(self.allRentals, json_file)



class Rental:
    def __init__(self, input: dict):

        self.url = input["url"]
        self.address = input["address"]
        self.price = input["price"]
        self.bedrooms = input["bedrooms"]
        self.postal_code = input["postal_code"]


    def getDetailedInfo(self):
        daftWebsite = requests.get(self.url)

        singlePageHtml = BeautifulSoup(daftWebsite.text, "html5lib")

        self.scrapingFacilities(singlePageHtml)
        self.scrapingOverview(singlePageHtml)

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

    def toDict(self):
        return {
            "url": self.url,
            "address": self.address,
            "price": self.price,
            "available from": self.availableFrom,
            "postal": self.postal_code,
            "bedrooms": self.bedrooms,
            "furnished": self.furnished,
            "facilities": self.facility,
        }
    
    def toStr(self):
        return f"{self.price} - {self.url}"

    def toText(self):
        return f"\
         D{self.postal_code}  beds:{self.bedrooms}\n\
         ${self.price}  DW?{'Dishwasher' in self.furnished}\n\
        {self.url}\
    "


##===== utils functions=====
def findNewestRentals(master_rental_reporter, newerRentals):
    lastCheckedEntryURLs = master_rental_reporter.URLs

    unprocessedRentals = []
    for item in newerRentals.fullList:
        if (item["url"] in lastCheckedEntryURLs):
            break
        unprocessedRentals.append(item)

    return unprocessedRentals
    pprint(unprocessedRentals)

def find_delta_rentals(master_rental_report:list, new_rentals_report:list) -> list:

    processed_urls =[rental["url"] for rental in master_rental_report ]
    unprocessed_rentals =[new_rental for new_rental in new_rentals_report if new_rental["url"] not in processed_urls]

    return unprocessed_rentals
