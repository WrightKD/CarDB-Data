from bs4 import BeautifulSoup
import pandas as pd

import urllib2
import argparse

parser = argparse.ArgumentParser(description='Dealership')
parser.add_argument('--pages', action="store", dest="pages", default=1)
parser.add_argument('--sort', action="store", dest="sort", default=None)
args = parser.parse_args()

cars = []

_image   = []
_price   = []
_model   = []
_type    = []
_year    = []
_mileage = []
_gearbox = []
_dealer  = []
_suburb  = []


def getCarsOnPage(page):
    page = urllib2.urlopen('https://www.autotrader.co.za/cars-for-sale?pagenumber='+str(page)+'&sortorder=Newest')
    soup = BeautifulSoup(page, features="html.parser")

    updateCarDetails(soup)


def updateCarDetails(warm_soup):

    for car in warm_soup.find_all('div', attrs={'class' : 'b-result-tile'}):
        cars.append(car)

    for car in cars:
        details = [x for x in car.stripped_strings]

        if len(details) >= 10:
            _image.append(car.a['href'])
            _price.append(details[0])
            _model.append(details[1])
            _type.append(details[2])
            _year.append(details[3])
            _mileage.append(details[4])
            _gearbox.append(details[5])
            _dealer.append(details[7])
            _suburb.append(details[8])

def main():
    
    for i in range(1,int(args.pages)+1):
        getCarsOnPage(i)

    table = pd.DataFrame(data={'Model' : _model, 'Price' : _price, 'Type' : _type, 'Year' : _year, 'Mileage' : _mileage, 'Gearbox' : _gearbox, 'Dealer' : _dealer, 'Suburb' : _suburb})

    if args.sort:
        table.sort_values(by=[args.sort], inplace=True)

    print(table)


if __name__ == "__main__":
    main()