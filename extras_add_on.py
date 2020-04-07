from bs4 import BeautifulSoup


with open('C:\\Grad Projects\\Car Dealership\\extra.html', "rb") as html:
        soup = BeautifulSoup(html, features="html.parser")

rows = soup.findAll("tr")

def formatSqlInsert(Name, Description):
    return 'INSERT INTO Extras (Name, Description) VALUES (' + "'{}'".format(Name) + ',' + "'{}'".format(Description) + ');'

with open("InsertExtras.sql", "w") as sql:
    for i in range(0, len(rows)):
        tds = rows[i].findAll('td')
        sql.write(formatSqlInsert(tds[0].text, tds[1].text) + '\n')


