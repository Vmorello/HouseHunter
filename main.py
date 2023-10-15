import time
import requests

from src.rental import *
from src.folder_util import findLastest, loadJsonFile


from datetime import datetime
from pprint import pprint


url = "https://api.green-api.com/waInstance7103860888/sendMessage/1ac3fe52fbd747e4b38cabff2c1f84fe9e59ced3620b40dcb3"
chatId = "120363181599538393@g.us"


def scrapeDublinDaft():

    search_results = RentalSearch()

    postal_code_disired = [1,2,4,6,7,8]
    for postal_code in postal_code_disired:
        search_results.getRentalsDaftDublinPostal(postal_code)

    # pprint(search_results.report)
    
    return search_results



if __name__ == "__main__":
    try: 
        # startLoop()
        headers = { 'Content-Type': 'application/json'}

        master_rental_reporter = scrapeDublinDaft()

        while (True):
            print(f"-------- starting a run at {datetime.now()} ---------")

            newRentals = scrapeDublinDaft()

            unprocessedRentals = find_delta_rentals(master_rental_reporter.report, newRentals.report)

            master_rental_reporter.append_unproccesed(unprocessedRentals)

            post_processed_rentals = []
            for newRental in unprocessedRentals:
                rental = Rental(newRental)
                rental.getDetailedInfo()
                post_processed_rentals.append(rental.toStr())
                # pprint(rental.toDict())
            
            if post_processed_rentals:
                text_message = " ".join(post_processed_rentals)
                print(text_message)
                payload = f"""{{\r\n\t"chatId": "{chatId}",\r\n\t"message": "{text_message}"\r\n}}"""
                response = requests.request("POST", url, headers=headers, data = payload)
                # print(response.text.encode('utf8'))

            time.sleep(300)
    except BaseException:
        print('Interrupted & printing report')
        print(f"we found {len(master_rental_reporter.report)-120} rentals")
        master_rental_reporter.saveJson("dublin_center")

