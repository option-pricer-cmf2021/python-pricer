'''
Option-pricer-cmf2021/python-pricer
Version 1.0
Author: Belov Mikhail

'''

import pandas as pd
import numpy as np
from datetime import datetime
from src.interpolation import Interpolator
from scipy import interpolate

'''
First Step:
    Building USD discount curve from eurodollar futures
    [In case of curiosity]

'''
# Set the Valuation Date and DCF basis
Valuation_date = "10/30/21"
DCF = 360

# read USD rates.csv
USD_rates = pd.read_csv("../python-pricer/data/USD rates.csv")

# create vector "Instrument_Prices" with pairs of Instrument names and prices
Instrument_name = USD_rates.iloc[1:, 0].values
Future_prices = USD_rates.iloc[1:, 1].values
Instrument_Prices = np.vstack((Instrument_name, Future_prices)).T

# create vector "StartDate_EndDate" with pairs of StartDate and EndDate
StartDate = USD_rates.iloc[1:, 3].values
EndDate = USD_rates.iloc[1:, 4].values
StartDate_EndDate = np.vstack((StartDate, EndDate)).T

# find LIBOR rates in decimal form from eurodollar future prices
rates_LIBOR = [i for i in range(len(Instrument_Prices))]
for i in range(len(Instrument_Prices)):
    rates_LIBOR[i] = round((100.0 - Instrument_Prices[i][1])/100.0, 4)

# define function to calculate number of days between two dates in a year fraction
def years(date_1,date_2, DCF=DCF):
    '''
    :param date_1: Beginning date
    :param date_2: Final date
    :param DCF: Day count fraction (how many days in 1 year)
    :return: Calculation the total value
    '''
    return abs((datetime.strptime(date_2,"%m/%d/%y") - datetime.strptime(date_1,"%m/%d/%y"))).days / DCF

# find year fraction values of eurodollar futures
years_eurodollar = [i for i in range(len(StartDate_EndDate))]
for i in range(len(StartDate_EndDate)):
    years_eurodollar[i] = round(years(StartDate_EndDate[i][0], StartDate_EndDate[i][1]), 4)

# find year fraction values of eurodollar futures from Valuation date
years_valdate = [i for i in range(len(StartDate_EndDate))]
for i in range(len(StartDate_EndDate)):
    years_valdate[i] = round(years(Valuation_date, StartDate_EndDate[i][1]), 4)

def calculate_DF(LIBOR_rates, Eurodollar_years, Valuation_date = Valuation_date):
    '''
    :param LIBOR_rates: Array with LIBOR rates
    :param Eurodollar_years: Array with number of days between Start and End dates in year fraction
    :param Valuation_date: Date of calculation
    :return: Array DF_from_ValDate
    '''
    # These discount factors calculated between start and end dates of instruments
    DF_for_period = [i for i in range(len(LIBOR_rates))]
    for i in range(len(LIBOR_rates)):
        DF_for_period[i] = 1/(1+LIBOR_rates[i]*Eurodollar_years[i])

    # Find discount factors from Valuation Date
    DF_from_ValDate = [i for i in range(len(DF_for_period))]
    for i in range(len(DF_for_period)):
        DF_from_ValDate[i] = DF_for_period[i] * (1/(1+LIBOR_rates[i]*years(Valuation_date,StartDate_EndDate[i][1])))
    return DF_from_ValDate

# Find DF from Valuation Date
DF_array = calculate_DF(rates_LIBOR, years_eurodollar)

# Final Array for Step 1 Task
final_array_1 = np.vstack((EndDate, DF_array)).T
print(final_array_1)

# Interpolator.interpolate function usage
usage_interpolate = Interpolator.interpolate(years_valdate, DF_array, 1.00)

# Extrapolate function from scipy usage
usage_extrapolate = interpolate.interp1d(years_valdate, DF_array, fill_value="extrapolate")

'''
Second Step:
    Building RUB discount curve and swap points curve for USDRUB
    
'''
# read RUB swap points.csv
RUB_swap_points = pd.read_csv("../python-pricer/data/RUB swap points.csv")

# create vector Term_swap_points with pairs of Term in years (DCF=360) and Swap points
Term_in_years = [1/DCF, 7/DCF, 14/DCF, 30/DCF, 60/DCF, 0.25, 0.5, 0.75, 1, 2, 3, 4, 5]
Swap_points = RUB_swap_points.iloc[0:, 1].values
Term_swap_points = np.vstack((Term_in_years, Swap_points)).T

# create an array with USD DF from Valuation Date with given Terms
USD_DF_Terms = [i for i in range(len(Term_in_years))]
for i in range(len(Term_in_years)):
    USD_DF_Terms[i] = usage_extrapolate(Term_in_years[i])

# find new USD rates from new USD DF
USD_rates_new = [i for i in range(len(Term_in_years))]
for i in range(len(Term_in_years)):
    USD_rates_new[i] = ((1/USD_DF_Terms[i] - 1)/Term_in_years[i])

# calculate RUB rates adding swap points to USD rates new
RUB_rates = [i for i in range(len(Term_in_years))]
for i in range(len(Term_in_years)):
    RUB_rates[i] = USD_rates_new[i] + 10**(-6) * Swap_points[i]

# calculate RUB DF from RUB rates
RUB_DF = [i for i in range(len(Term_in_years))]
for i in range(len(Term_in_years)):
    RUB_DF[i] = 1/(1+RUB_rates[i]*Term_in_years[i])

# Final Array for Step 2 Task
final_array_2 = np.vstack((Term_in_years, RUB_DF)).T
print(final_array_2)




