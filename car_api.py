from bs4 import BeautifulSoup
import urllib2

page = urllib2.urlopen('https://www.autotrader.co.za/cars-for-sale?sortorder=Newest')
soup = BeautifulSoup(page, features="html.parser")

for car in soup.find_all('div', attrs={'class' : 'b-result-tile'}):
    print("__________________________________________________________________")
    print(car)
    print("__________________________________________________________________")

