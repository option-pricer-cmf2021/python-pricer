import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

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
    
class curve_discount_swap_points:
    """класс для построения кривой дисконтирования для рубля и кривой своп пойнтов для доллар рубля.
    """
    def __init__(self,current_data):
        self.sw_points_time,self.sw_points_value = None,None
        self.current_data = current_data
#         пока ничего не делаем с USD_RATE
        
    @staticmethod
    def discount_factor(data):
        return [[i,0.99] for i in data]
    
    @staticmethod
    def preparation_SW_data(SW_data):
        term = {"ON":pd.Timedelta("0 D").days,"W":pd.Timedelta("1 W").days,"M":pd.Timedelta("30 D").days,"Y":pd.Timedelta("1 Y").days}
        
        time = [term["ON"] if i=="ON" else int(i[:-1])*term[i[-1]]  for i in SW_data["Term"]]
        
        points = SW_data["SW POINTS"]
        return time,points

    def sw_points_inter(self,data):
        data_new = list(map(pd.to_datetime,data))
        data_new = [(i.date()-self.current_data).days for i in data_new]
        return [[data[i],Interpolator.interpolate(self.sw_points_time,self.sw_points_value,data_new[i])] for i in range(len(data_new))]