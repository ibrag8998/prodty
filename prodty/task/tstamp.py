from datetime import datetime, timedelta
import re

from dateparser.search import search_dates


def tstamp_to_dt(tstamp):
    today = datetime.today().date()
    tomorrow = (today + timedelta(days=1))

    dt = datetime.fromtimestamp(tstamp)

    date = dt.date()
    time = dt.strftime('%-H:%M')

    if date == today:
        res = f'Today {time}'
    elif date == tomorrow:
        res = f'Tomorrow {time}'
    else:
        res = f'{dt.strftime("%d.%m")} {time}'

    return res


def recognize(text):
    """
    Recognizes timestamp in text and returns it.
    Only first timestamp is recognized due to logic
    of prodty app. Of course there is no problems to
    extend this func with some lines of code to make
    it returning all timestamps
    """
    date = rec_date(text)
    hrs, mins = rec_time(text)

    if date.date() == datetime.today().date():
        hrs, mins = adapt_time(hrs, mins)

    res = date + timedelta(hours=hrs, minutes=mins)

    return int(res.timestamp())


def adapt_time(hrs, mins):
    now = datetime.now()

    if now.hour > hrs:
        hrs += 24

    elif now.hour == hrs and now.minute > mins:
        hrs += 1

    return hrs, mins


def rec_date(text):
    """ Recognize date """
    res = search_dates(text)
    now = datetime.now()
    date = None

    if res:
        res = res[0][1]
        if res > now:
            date = datetime(res.year, res.month, res.day)

    if not date:
        date = datetime(now.year, now.month, now.day)

    return date


def rec_time(text):
    """ Recognize time """
    pattern = r'(^|\s)\d{1,2}:\d{2}($|\s)'
    res = re.search(pattern, text)
    hr, min_ = None, None

    if res:
        hr, min_ = map(int, res.group().split(':'))
    else:
        hr, min_ = 18, 0

    return hr, min_

