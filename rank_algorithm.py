__author__ = 'li'
# -*- coding: UTF-8 -*-
from datetime import datetime as dt
import datetime
from math import log


epoch = dt(1970, 1, 1)


def epoch_seconds(date):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


def score(ups, repost):
    return ups + repost


def index_score(ups, downs, repost):
    return ups + repost - downs


def hot(ups, downs, repost, date):
    """The hot formula. Should match the equivalent function in postgres."""
    realScore = score(ups, repost)
    s = index_score(ups, downs, repost)
    order = log(max(abs(realScore), 1), 2)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(sign * order + seconds / 90000, 7)


# 标准的mark，分数大于等于这个mark才算热帖
def standard_mark():
    order = log(max(abs(8), 1), 2)
    sign = 1
    seconds = epoch_seconds(dt.now() + datetime.timedelta(days=-1)) - 1134028003
    return round(sign * order + seconds / 90000, 7)




