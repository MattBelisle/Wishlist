import requests
from xml.etree import ElementTree


def stringToFloat(str, default):
    try:
        num = float(str)
    except ValueError:
        num = default
    return num

def main(amount, currencyTo, currencyFrom):
    startingAmount=amount
    xmlFromBank = requests.get("http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
    tree = ElementTree.fromstring(xmlFromBank.content)
    tree = ElementTree.ElementTree(tree)
    root = tree.getroot()
    currencies = dict()
    for child in root:
        text = ElementTree.tostring(child)
        t = ElementTree.ElementTree(ElementTree.fromstring(text))
        text = text.decode('utf-8')
        while "currency" in text:
            ##data is in the form currency="xyz" so from c to first " is 10
            endOfCurrency = text.find("currency", 0) + 10
            typeOfCurrency = text[endOfCurrency:endOfCurrency + 3]
            ##data is in the form rate="num"\> so rate + 6 is start of rate
            endOfRate = text.find("rate", 0) + 6
            endOfLine = text.find(">")
            rate = text[endOfRate:endOfLine - 3]
            rate = stringToFloat(rate, 1.0)
            currencies[typeOfCurrency] = rate
            text = text[endOfLine + 1:]
    #From EUR bank so have to have special case if EUR is wanted....
    if currencyFrom == "EUR" and currencyTo == "EUR":
        exchange = 1
    elif currencyFrom == "EUR":
        exchange = currencies[currencyTo]
    elif currencyTo == "EUR":
        exchange = 1 / currencies[currencyFrom]
    else:
        exchange = currencies[currencyTo] / currencies[currencyFrom]
    exchange *= startingAmount
    print(startingAmount, currencyFrom, "can be exchanged for", "%.2f" % exchange, currencyTo)
    return exchange


