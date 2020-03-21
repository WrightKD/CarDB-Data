from bs4 import BeautifulSoup
import pandas as pd

import urllib2
import argparse
import os
import datetime
import sys

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

def Datetime():
    return str(datetime.datetime.now()).replace(':','').replace('-','').replace('.','').replace(' ','')

def progressBar(value, endvalue, bar_length=20):

    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rDownloading : [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()

def main():
    
    pages = int(args.pages)

    for i in range(1,pages+1):
        getCarsOnPage(i)
        progressBar(i,pages)

    print('')

    table = pd.DataFrame(data={'Model' : _model, 'Price' : _price, 'Type' : _type, 'Year' : _year, 'Mileage' : _mileage, 'Gearbox' : _gearbox, 'Dealer' : _dealer, 'Suburb' : _suburb})
    table.drop_duplicates(inplace=True)

    if args.sort:
        table.sort_values(by=[args.sort], inplace=True)

    print(table)
    
    file = '\\cars_'+str(len(cars))+'_'+Datetime()+'.json'

    table.to_json(path_or_buf=os.getcwd()+file, orient='records',)


if __name__ == "__main__":
    main()
