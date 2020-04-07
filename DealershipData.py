from bs4 import BeautifulSoup
import pandas as pd

import subprocess

import argparse
import os
import datetime
import sys
import urllib
import urllib.request
import random

from VinGenerator import vin

import base64

colours = ['Aluminum','Beige','Black','Blue','Brown','Bronze','Claret','Copper','Cream','Gold',
            'Green', 'Maroon', 'Metallic', 'Navy', 'Orange', 'Pink', 'Purple', 'Red', 'Rose',
            'Rust', 'Silver', 'Tan', 'Turquoise', 'White', 'Yellow']

fuel_types = ['Petrol','Diesel']

parser = argparse.ArgumentParser(description='Dealership')
parser.add_argument('--pages', action="store", dest="pages", default=1)
parser.add_argument('--sort', action="store", dest="sort", default=None)
parser.add_argument('--server', action="store", dest="server", default="KENNETHWR\SQLEXPRESS")
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
_vin     = []
_manufacturer = []
_colour = []
_previous_owners = []
_automatic_transmission = []
_top_speed = []
_engine_capacity = []
_wheel_size = []
_fuel_types = []
_horsepower = []
_service_history = []


_vehicle_id = []
_vehicle_images = []

def getCarsOnPage(page):
    page = urllib.request.urlopen('https://www.autotrader.co.za/cars-for-sale?pagenumber='+str(page)+'&sortorder=Newest')
    soup = BeautifulSoup(page, features="html.parser")

    updateCarDetails(soup)


def updateCarDetails(warm_soup):

    count = 0

    for car in warm_soup.find_all('div', attrs={'class' : 'b-result-tile'}):
        cars.append(car)

    for car in cars:
        details = [x for x in car.stripped_strings]
        count += 1
        if len(details) >= 10:
            #_image.append(car.a['href'])

            VehicleInformation(car.a['href'], count)

            _image.append(count)
            _price.append(details[0])
            _model.append(details[1]) 
            _manufacturer.append(details[1].split()[0])
            #_manufacturer.append(random.randrange(1, 25))
            _type.append(details[2])
            _year.append(details[3])
            _mileage.append(cleanMileage(details[4]))
            _dealer.append(details[7])
            _suburb.append(details[8])
            _previous_owners.append(random.randrange(1, 4))
            _automatic_transmission.append(isAuto(details[5]))
            _colour.append(random.choice(colours))
            _top_speed.append(random.randrange(100, 201))
            _engine_capacity.append(round(random.uniform(1.0, 18.0),1))
            _wheel_size.append(random.randrange(18, 36))
            _fuel_types.append(random.choice(fuel_types))
            _horsepower.append(random.randrange(1000, 2000))
            _service_history.append('Full Service History')
            _vin.append(vin.getRandomVin())


def VehicleInformation(url,index):

    page = urllib.request.urlopen('https://www.autotrader.co.za/' + url)
    soup = BeautifulSoup(page, features="html.parser")

    imagesList = soup.find("ul", {"class": "e-thumbs-list"}).findAll("li")

    _vehicle_id.append(index)
    
    urllib.request.urlretrieve(imagesList[0].span.img['src'], "image.jpg")
    

    with open("image.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())

    _vehicle_images.append(encoded_image)


def isAuto(transmission):
    if transmission == 'Manual':
        return 0
    else:
        return 1

def cleanMileage(string): 
    return string.replace(" ", "").replace("km", "").replace('\u00a0', "")

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

    Manufacturer = list(set(_manufacturer))
    tableManufacturer = pd.DataFrame(data={'Name' : Manufacturer, 'Email' : [x+'@company.co.za' for x in Manufacturer], 'Phone_Number' : ['+27121234568']*len(Manufacturer) })

    for i in range(0,len(_manufacturer)):
        index = Manufacturer.index(_manufacturer[i]) + 1
        _manufacturer[i] = index

    tableVehicle_images = pd.DataFrame(data={'Vehicle_Id' : _vehicle_id, 'Image' : _vehicle_images})

    tableVehicles = pd.DataFrame(data={'Model' : _model, 'Price' : _price, 'Type' : _type, 'Year' : _year, 'Mileage' : _mileage, 'Dealer' : _dealer, 'Suburb' : _suburb,
                               'Colour' : _colour, 'Engine_Capacity' : _engine_capacity, 'Wheel_Size' : _wheel_size, 'Fuel_Type' : _fuel_types, 'Top_Speed' : _top_speed,
                                'Previous_Owners' : _previous_owners, 'Service_History' : _service_history, 'Horsepower' : _horsepower, 'Vehicle_Vin' : _vin , 'Automatic_Transmission' : _automatic_transmission,
                                'Manufacturer_Id' : _manufacturer, 'Image_Id' : _image})

    tableVehicles.drop_duplicates(inplace=True)

    if args.sort:
        tableVehicles.sort_values(by=[args.sort], inplace=True)

    print(tableVehicles.head())
    print(tableManufacturer.head())
    print(tableVehicle_images.head())

    tableVehicles.to_json(path_or_buf=os.getcwd()+'\\Vehicles.json', orient='records')
    tableManufacturer.to_json(path_or_buf=os.getcwd()+'\\Manufacturers.json', orient='records')
    tableVehicle_images.to_json(path_or_buf=os.getcwd()+'\\VehicleImages.json', orient='records')
   
    sqlCreate = os.getcwd()+'\\UploadVehiclesProc.sql'

    process = subprocess.run(['sqlcmd','-S',args.server,'-i',sqlCreate], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    print(output)

    sqlExec = "EXEC [Dealership].[dbo].[UploadManufacturers] " + "'{}'".format(os.getcwd()+'\Manufacturers.json')

    print('Run the below command: ')
    print('sqlcmd -S ' +'"{}"'.format(args.server)+ ' -E ' + '-Q '+ '"{}"'.format(sqlExec))

    sqlExec = "EXEC [Dealership].[dbo].[UploadVehicles] " + "'{}'".format(os.getcwd()+'\Vehicles.json')

    print('Run the below command: ')
    print('sqlcmd -S ' +'"{}"'.format(args.server)+ ' -E ' + '-Q '+ '"{}"'.format(sqlExec))

    sqlExec = "EXEC [Dealership].[dbo].[UploadVehicle_Images] " + "'{}'".format(os.getcwd()+'\VehicleImages.json')

    print('Run the below command: ')
    print('sqlcmd -S ' +'"{}"'.format(args.server)+ ' -E ' + '-Q '+ '"{}"'.format(sqlExec))
    

if __name__ == "__main__":
    main()