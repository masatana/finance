#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014, Takeshi Mizumoto
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of pandas-jpmarket nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import jsm
from pandas.core.datetools import to_datetime
import numpy as np
import pandas

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
    frames = np.vstack(frames).transpose()

    dates = [x.date for x in data]

    frames = pandas.DataFrame(frames, columns = props, index = dates)
    return frames

def _sanitize_dates(start, end):
    start = to_datetime(start)
    end = to_datetime(end)
    if start is None:
        start = dt.datetime(2010, 1, 1)
    if end is None:
        end = dt.datetime.today()
    return start, end

