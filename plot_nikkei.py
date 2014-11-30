#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from datetime import datetime
import jsm
import pandas.compat as compat
import pandas
import numpy
import jpmarket

if __name__ == "__main__":
    start = datetime(2014, 10, 1)

    f = jpmarket.dataReader(6952, "yahoojp", start)
    plt.title("{} from {} to {}".format(6952, start, datetime.today()))

    plt.fill_between(f.index, f["Low"], f["High"], color="b", alpha=0.2)

    f["Close"].plot()
    plt.savefig("./casio.png")

