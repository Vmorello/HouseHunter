import re

# ==================pulled from the rental Search class ======================

def getPrice(rentalHTML) -> int:
    try:
        priceHTML = rentalHTML.find(
            'h3',
            {"class": "TitleBlock__StyledCustomHeading-sc-1avkvav-5 blbeVq"})
        # pprint(priceHTML)
        price = priceHTML.text
    except AttributeError:
        priceHTML = rentalHTML.find(
            'p', {"class": "SubUnit__Title-sc-10x486s-5 feGTKf"})
        # pprint(priceHTML)
        price = priceHTML.text

    # pprint(priceHTML)
    costWithComma = re.findall(r'[0-9],[0-9]+|[0-9]+', price)
    cost = re.sub(r',', '', costWithComma[0])
    cost = int(cost)

    return cost

def getUrl( rentalHTML) -> str:

    endingURL = rentalHTML.get("href")
    fullURL = "https://www.daft.ie" + endingURL
    return fullURL

def getBedrooms( rentalHTML) -> int:
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

def getAddress( url) -> int:
    address = url.split("/")[4]
    address = re.sub(r'apartment|house|studio', '', address)
    address = re.sub(r'-', ' ', address)

    return address

