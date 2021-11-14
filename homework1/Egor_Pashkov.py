# -*- coding: utf-8 -*-

class Interpolator:
    """Linear interpolator.
    """

    @staticmethod
    def interpolate(x_list: list, y_list: list, z: float):
        """Linear interpolate.
        Parameters
        __________
        x_list : list
            x values.
        y_list: list
            y values.
        z: float
            Interpolate in that point z.
        Returns
        _______
        float
            Interpolate value.
        Raises
        ______
        ValueError
            x_list must be sorted ASC.
        """
        if x_list != sorted(x_list):
            raise ValueError('x_list must be sorted ASC')
        for index, element in enumerate(x_list):
            if z <= element:
                delta = (z - x_list[index - 1]) / (x_list[index] - x_list[index - 1])
                answer = y_list[index - 1] + (y_list[index] - y_list[index - 1]) * delta
                break
        return answer

import pandas as pd
import numpy as np
import datetime

rub = pd.read_csv('/content/python-pricer/data/RUB swap points.csv')
usd = pd.read_csv('/content/python-pricer/data/USD rates.csv')
usd.loc[0,'Conv, adj'] = usd.loc[0,'Unnamed: 1']

today = datetime.date.today()

tenor_dict = {
    "ON": pd.Timedelta("0 D"),
    '1W': pd.Timedelta("1 W"),
    '2W': pd.Timedelta("2 W"),
    '1M': pd.Timedelta("30 D"),
    '2M': pd.Timedelta("60 D"),
    '3M': pd.Timedelta("90 D"),
    '6M': pd.Timedelta("180 D"),
    '9M': pd.Timedelta("270 D"),
    '12M': pd.Timedelta("1 Y"),
    '2Y': pd.Timedelta("2 Y"),
    '3Y': pd.Timedelta("3 Y"),
    '4Y': pd.Timedelta("4 Y"),
    '5Y': pd.Timedelta("5 Y")
}

rub['date'] = pd.to_datetime(rub['Term'].apply(lambda x: tenor_dict[x] + today))
rub['date_sec'] = rub['date'].apply(lambda x: x.timestamp())

rub['date_day'] = rub['Term'].apply(lambda x: tenor_dict[x].days)

rub

def swop_point(date='12/15/21'):
  date = datetime.datetime.strptime(date, '%m/%d/%y')
  #return np.interp(date.timestamp(), rub['date_sec'], rub['SW POINTS'])
  return Interpolator.interpolate(list(rub['date_sec']), list(rub['SW POINTS']), date.timestamp())

swop_point()

usd['StartDate'].apply(swop_point).plot()

temp = [1] * len(usd)
discount = pd.DataFrame(temp, index=usd['StartDate'])
discount