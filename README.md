# AEP-2-Python-Extension
A small project containing a bit of a larger leap into exploring derivatives of functions. Know that using this project will create a .csv file in the directory it is ran in.
# Installation
## Prerequisites
- Python 3.x
- pip
- yfinance for scraping the data
- pandas for converting the data in a easily viewable file
- Something to view .csv files, there are easily accessible websites for this

## Steps for easy installation
This isn't a complex respository, you can simply download main.py and install the requirements via pip using
```bash
pip install yfinance
pip install pandas
```
in a command prompt.

These can later be uninstalled via
```bash
pip uninstall yfinance
pip uninstall pandas
```

Running main.py shouldn't pose any issues so long as Python 3.x is installed

# Usage
Running the file will prompt you with
```bash
Stock:
```
This is where you input the symbol of the stock you want to get a view of, say NVDA.

Then it will ask you if you want to change the dates. The default dates are the dates used in the original exploration of the document.
