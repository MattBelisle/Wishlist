##Goes to my in stock trades wishlist and exports it to an excel spreadsheet
import CurrencyExchange
import requests as r
from bs4 import BeautifulSoup
import csv
def main():
    with open('Comics.csv','w') as csvfile:
        fieldnames = ['Title', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        request = r.get( "https://www.instocktrades.com/wishlists/7bffe522902943d5bbb18c9b571bf9")
        clean = BeautifulSoup(request.text, "lxml")
        count=0
        sum=0
        for row in clean.find_all("tr",{"class": "cartlistrow"}):
            ## [1] as there are 2 <a> tags per row and the second always has the title name
            comic = row.find_all("a")[1].text
            price = row.find("span").text
            if('$'in price):
                sum += float(price[1:])
            print(comic + " " + price)
            writer.writerow({'Title': comic, 'Price': price})
            count += 1
        print(sum)
        writer.writerow({'Title': 'Price USD', 'Price': sum})
        writer.writerow({'Title': 'Price CAD', 'Price': '%.2f' % (CurrencyExchange.main(sum,'CAD','USD'))})
        writer.writerow({'Title': 'Count', 'Price': count})



if __name__ == "__main__":
    main()






