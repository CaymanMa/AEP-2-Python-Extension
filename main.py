import yfinance as yf
import pandas as pd

# Get the symbol for the stock in interest
ticker: str = input("Stock: ")

# Load the data from the stock
data = yf.Ticker(ticker).history(period="5y")


# Create a list of dates
changeDates = input(
    "Change Dates? By default data will be grabbed from 2021/01 to 2024/11. (Y/N): ")

years: list[str] = []
months: list[str] = []

match changeDates:
    case "N":
        years = ['2021', '2022', '2023', '2024']
        months = ['01', '03', '05', '07', '09', '11']

    case "Y":
        isInputtingYears = True
        while isInputtingYears:
            year = input("Input a year (Input 0 to stop): ")
            if year != "0":
                years.append(year)
            else:
                isInputtingYears = False

        isInputtingMonths = True

        while isInputtingMonths:
            month = input("Input a month (Input 0 to stop): ")
            if month != "0":
                if len(month) == 1:
                    months.append(f"0{month}")
                else:
                    months.append(month)

            else:
                isInputtingMonths = False


dates: list[list[str]] = []
for year in years:
    for month in months:
        dates.append([year, month])


# Some of these dates will be invalid, we'll have to find a version that is valid
def validate_date(date, day):
    currMonth = date[1]
    currYear = date[0]

    try:
        data.loc[[f'{currYear}-{currMonth}-{day} 00:00:00-5:00']]
        return [currYear, currMonth, day, 5]
    except:
        try:
            data.loc[[f'{currYear}-{currMonth}-{day} 00:00:00-4:00']]
            return [currYear, currMonth, day, 4]
        except:
            return validate_date(date, day+1)


# Create a list of Valid Dates
valid_dates = []
for date in dates:
    valid_dates.append(validate_date(date, 1))

# Create a list of dates to be displayed later
display_dates = []
for valid_date in valid_dates:
    display_dates.append(f'{valid_date[0]}/{valid_date[1]}')

# Grab the values from the data
dollar_values = []
for date in valid_dates:
    dollar_values.append(round(float(
        data.at[f'{date[0]}-{date[1]}-0{date[2]} 00:00:00-{date[3]}:00', 'High']), 2))


first_derivatives = []
for entry in range(len(dollar_values)):
    # Backwards
    if entry == 0:
        first_derivatives.append(round(dollar_values[1]-dollar_values[0], 2))

    # Central
    if entry != 0 and entry != len(dollar_values) - 1:
        first_derivatives.append(
            round((dollar_values[entry+1]-dollar_values[entry-1])/2, 2))

    # Forwards
    if entry == len(dollar_values) - 1:
        first_derivatives.append(round(dollar_values[-1]-dollar_values[-2], 2))

second_derivatives = []
for entry in range(len(first_derivatives)):
    # Backwards
    if entry == 0:
        second_derivatives.append(
            round(first_derivatives[1]-first_derivatives[0], 2))

    # Central
    if entry != 0 and entry != len(first_derivatives) - 1:
        second_derivatives.append(
            round((first_derivatives[entry+1]-first_derivatives[entry-1])/2, 2))

    # Forwards
    if entry == len(first_derivatives) - 1:
        second_derivatives.append(
            round(first_derivatives[-1]-first_derivatives[-2], 2))


pospos = []
posneg = []
negpos = []
negneg = []

for index in range(len(dollar_values)):

    if first_derivatives[index] > 0 and second_derivatives[index] > 0:
        pospos.append("X")
    else:
        pospos.append(' ')

    if first_derivatives[index] > 0 and second_derivatives[index] < 0:
        posneg.append("X")
    else:
        posneg.append(' ')

    if first_derivatives[index] < 0 and second_derivatives[index] > 0:
        negpos.append("X")
    else:
        negpos.append(' ')

    if first_derivatives[index] < 0 and second_derivatives[index] < 0:
        negneg.append("X")
    else:
        negneg.append(' ')

# Compile data to get it ready for a .csv file
newData = {
    "Date": display_dates,
    "Dollar Value": dollar_values,
    "First Derivative": first_derivatives,
    "Second Derivative": second_derivatives,
    "Increasing at an increasing rate": pospos,
    "Increasing at a decreasing rate": posneg,
    "Decreasing at an increasing rate": negpos,
    "Decreasing at a decreasing rate": negneg
}

df = pd.DataFrame(newData)

df.to_csv('result.csv')
