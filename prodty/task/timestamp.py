from datetime import datetime, timedelta
import re

from dateparser.search import search_dates


def recognize(text):
    """
    Recognizes timestamp in text and returns it.
    Only first timestamp is recognized due to logic
    of prodty app. Of course there is no problems to
    extend this func with some lines of code to make
    it returning all timestamps
    """
    date = rec_date(text)
    hours, minutes = rec_time(text)

    return date + timedelta(hours=hours, minutes=minutes)


def rec_date(text):
    """ Recognize date """
    res = search_dates(text)
    date = None

    if res is not None:
        res = res[0][1]
        date = datetime(res.year, res.month, res.day)

    if not date:
        tmp = datetime.now()
        date = datetime(tmp.year, tmp.month, tmp.day)

    return date


def rec_time(text):
    """ Recognize time """
    pattern = r'(^|\s)\d{1,2}:\d{2}($|\s)'
    res = re.search(pattern, text)
    if res:
        hour, minute = res.group().split(':')
        return int(hour), int(minute)
    else:
        return 18, 0


while True:
    test = input()
    res = recognize(test)
    if res:
        print(res.strftime('%c'))
    else:
        print('-_-')

