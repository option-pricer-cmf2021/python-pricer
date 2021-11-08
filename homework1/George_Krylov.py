from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Interpolation(object):
    """
    Class for calculating linear interpolation

    Functions:
        interpolate_simple(self)
    """

    def __init__(self, x_array, y_array, z_array):
        """
        Constructor of a interpolation class object for
        calculating linear interpolation
        Returns
        -------
        output : Interpolation object

        Parameters
        ----------
        x_array: list
            x values
        y_array: list
            y values
        z: float
            z value
        """
        self.x = x_array
        self.y = y_array
        self.z = z_array

    def interpolate_simple(self):
        """
        Function for calculating linear interpolation

        Returns
        -------
        output : func value in z
            k = f(z)
        """
        k = []
        self.z = [
            int((datetime.strptime(x, "%d.%m.%Y") - datetime.today()).days)
            for x in self.z
        ]
        # type(self.z[0])
        for u in self.z:
            for i in range(len(self.x) - 1):
                if u > self.x[i] and u <= self.x[i + 1]:
                    k.append(
                        self.y[i]
                        + (self.y[i + 1] - self.y[i])
                        / (self.x[i + 1] - self.x[i])
                        * (u - self.x[i])
                    )
        return k


def datefun(x):
    date_after = None
    if "M" in x:
        date_after = datetime.today() + relativedelta(months=int(x[:-1]))
    elif "Y" in x:
        date_after = datetime.today() + relativedelta(years=int(x[:-1]))
    elif "W" in x:
        date_after = datetime.today() + relativedelta(weeks=int(x[:-1]))
    return (date_after - datetime.today() + timedelta(days=1)).days


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("../data/RUB swap points.csv")
    df = df[["Term", "SW POINTS"]]
    df = df.iloc[1:]
    df["days"] = df["Term"].apply(lambda x: datefun(x))
    res = Interpolation(
        list(df["days"]),
        list(df["SW POINTS"]),
        ["10.12.2021", "10.12.2022", "10.12.2023", "10.12.2024"],
    ).interpolate_simple()
    print(res)
