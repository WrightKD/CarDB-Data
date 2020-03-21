# CarDB-Data

Run the python file to pull cars for mock data

### Usage

Requires [Python 2.7 or greater](https://www.python.org/) to run.

Install [bs4]() and [pandas]()
```sh
pip install bs4 pandas
```
Run CarDB_Data.py with or without any arguments.
```sh
python CarDB_Data.py
```
![Output](https://raw.githubusercontent.com/WrightKD/CarDB-Data/master/output.png)

#### Arguments
Sort - Sorts table by column name

```sh
python CarDB_Data.py --sort [column]
```

pages - the number of pages to extract vehicles from ( 1 page ~ 11 vehicles).Default is one page.

```sh
python CarDB_Data.py --pages [int]
```



