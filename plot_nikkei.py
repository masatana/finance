#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from datetime import datetime
import jsm
import pandas.compat as compat
import pandas
import numpy

def dataReader(name, data_source=None, start=None, end=None,
        retry_count=3, pause=0.001):
    return get_data_yahoojp(symbols=name, start=start, end=end,
                            adjust_price=False, chunksize=25,
                            retry_count=retry_count, pause=pause)

def get_data_yahoojp(symbols=None, start=None, end=None, retry_count=3,
                     pause=0.001, adjust_price=False, ret_index=False,
                     chunksize=25):
    q = jsm.Quotes() 

    if not isinstance(symbols, list):
        return data2frame(q.get_historical_prices(
                          symbols, start_date=start, end_date=end))

    for i, s in enumerate(symbols):
        try:
            symbols[i] = int(s)
        except:
            raise exceptions.ValueError("symbols must be an integer")

    prices = []
    for symbol in symbols:
        prices.append(
            data2frame(q.get_historical_prices(
                symbol, start_date=start, end_date=end))
        )
    return prices

def data2frame(data):
    props = ["Open", "High", "Low", "Close", "Volume"]
    frames = []

    for prop in props:
        frames.append([getattr(x, prop.lower()) for x in data])

    props.append("Adj Close")
    frames.append([x._adj_close for x in data])
    frames = numpy.vstack(frames).transpose()

    dates = [x.date for x in data]

    frames = pandas.DataFrame(frames, columns = props, index = dates)
    return frames

def _sanitize_dates(start, end):
    from pandas.core.datetools import to_datetime
    start = to_datetime(start)
    end = to_datetime(end)
    if start is None:
        start = dt.datetime(2010, 1, 1)
    if end is None:
        end = dt.datetime.today()
    return start, end

if __name__ == "__main__":
    start = datetime(2014, 10, 1)

    f = dataReader(6952, "yahoojp", start)
    plt.title("{} from {} to {}".format(6952, start, datetime.today()))

    plt.fill_between(f.index, f["Low"], f["High"], color="b", alpha=0.2)

    f["Close"].plot()
    plt.savefig("./nikkei.png")

