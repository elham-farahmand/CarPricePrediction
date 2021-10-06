from bs4 import BeautifulSoup
import requests
import mysql.connector
import csv
from sklearn import tree


# Input section
car_name = input('Insert the car name and model withot any spaces (For example, hyundaiSonata): ')
car_year = int(input('Insert the car production year (For example, 2015): '))
car_miles = int(input('Insert mileage of the car (For example, 70000): '))

# Scraping section
def get_all(url, car_name):
    res = requests.get(url + car_name)
    soup = BeautifulSoup(res.text, 'html.parser')

page = 1
price = []
mileage = []
year = []
name = []
while page != 2:
    url = f"https://www.truecar.com/used-cars-for-sale/listings/{car_name}/location-beverly-hills-ca/?page={page}"
    response = requests.get(url)
    res = requests.get(url + car_name)
    soup = BeautifulSoup(res.text, 'html.parser')
    for div in soup.find_all('div', attrs = {'data-test':'vehicleListingPriceAmount'}):
        price.append(div.get_text(strip=True))
    for div in soup.find_all('div', attrs = {'data-test':'vehicleMileage'}):
        mileage.append(div.get_text(strip=True))
    for span in soup.find_all('span', attrs = {'class':'vehicle-card-year font-size-1'}):
        year.append(span.get_text(strip=True))
    for span in soup.find_all('span', attrs = {'class':'vehicle-header-make-model text-truncate'}):
        name.append(span.get_text(strip=True))
    page = page + 1

# Making the scraped data clear
mileage_list = []
price_list = []
for item in mileage:
    this = item.replace(',','').replace('miles','').replace('les','')
    mileage_list.append(this)

for item in price:
    this = item.replace(',','').replace('$','')
    price_list.append(this)


# These are some data for testing the program. If you want to use this, you should comment web scraping section.
#mileage = ['88,787miles', '84,208miles', '62,314miles', '88,427miles', '73,604miles', '125,675miles', '68,935miles', '119,409miles', '36,718miles', '36,001miles', '40,958milesles', '80,070miles', '126,000miles', '40,799miles', '98,712miles', '40,983miles', '26,621miles', '87,251miles', '29,878miles', '40,710miles', '32,108miles', '38,838miles']
#price = ['$22,100', '$35,000', '$12,005', '$30,000', '$5,000', '$17,657', '$8,500', '$120,409', '$30,450', '$6,780', '$8,900', '$8,750', '$12,300', '$15,400', '$20,220', '$450,000', '$12,000', '$25,600', '$14,900', '$50,630', '$11,500', '$23,840']
#year = ['2015', '2020', '2019', '2013', '2017', '2013', '2015', '2013', '2018', '2018', '2018', '2013', '2018', '2019', '2018', '2018', '2015', '2016', '2020', '2013', '2018', '2020', '2016', '2016', '2020', '2015', '2020', '2018', '2013', '2018', '2020', '2018', '2018']
#name = ['HyundaiGenesis Coupe', 'HyundaiVeloster', 'HyundaiSonata', 'HyundaiSonata', 'HyundaiSonata', 'HyundaiEquus', 'HyundaiSonata', 'HyundaiSonata', 'HyundaiSonata', 'HyundaiElantra', 'HyundaiSonata', 'HyundaiGenesis', 'HyundaiSanta Fe Sport', 'HyundaiElantra', 'HyundaiSonata', 'HyundaiTucson', 'HyundaiSonata', 'HyundaiSonata', 'HyundaiSanta Fe', 'HyundaiElantra', 'HyundaiSonata', 'HyundaiElantra', 'HyundaiSonata', 'HyundaiElantra', 'HyundaiSanta Fe', 'HyundaiGenesis', 'HyundaiTucson', 'HyundaiSonata', 'HyundaiElantra', 'HyundaiSonata', 'HyundaiTucson', 'HyundaiSonata', 'HyundaiElantra']


# Insert data into the database. Use your own database name, table name, user, and password.
dbname = 'items'
tablename = 'cars'
cnx = mysql.connector.connect(user = 'root', password = '123456', host = '127.0.0.1', database = dbname)
cursor = cnx.cursor()

for x, y, z, u in zip(name, year, mileage_list, price_list):
    cursor.execute('Begin INSERT INTO %s VALUES (\'%s\',\'%i\',\'%i\',\'%i\')' % (tablename, x, int(y), int(z), int(u)))
    
cnx.commit() 

# Machine learning section
cursor.execute('SELECT * FROM cars WHERE name in (\'%s\')' % (car_name))
lines = cursor.fetchall()

x = []
y = []
for line in lines:
    x.append(line[1:3])
    y.append(line[3])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

new_data = [[car_year, car_miles]]
answer = clf.predict(new_data)
print('The price of the property you are looking for is: $', answer[0])

cnx.close()