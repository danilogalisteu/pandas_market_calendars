
import datetime
import pandas as pd
from pandas.util.testing import assert_index_equal

import pandas_exchange_calendars as pec
from .test_exchange_calendar import FakeCalendar


def test_date_range_daily():

    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))

    # If closed='right' and force_close False for daily then the result is empty
    expected = pd.DatetimeIndex([], tz='UTC')
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    actual = pec.date_range(schedule, '1D', force_close=False, closed='right')

    assert_index_equal(actual, expected)

    # New years is holiday
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2015-12-31 12:00', '2016-01-04 12:00', '2016-01-05 12:00', '2016-01-06 12:00']])
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    actual = pec.date_range(schedule, '1D')

    assert_index_equal(actual, expected)

    # July 3 is early close
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2012-07-02 12:00', '2012-07-03 11:30', '2012-07-04 12:00']])
    schedule = cal.schedule('2012-07-02', '2012-07-04')
    actual = pec.date_range(schedule, '1D')

    assert_index_equal(actual, expected)

    # Dec 14, 2016 is adhoc early close
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2016-12-13 12:00', '2016-12-14 11:40', '2016-12-15 12:00']])
    schedule = cal.schedule('2016-12-13', '2016-12-15')
    actual = pec.date_range(schedule, '1D')

    assert_index_equal(actual, expected)

    # July 3 is late open
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2012-07-02 09:00', '2012-07-03 11:15', '2012-07-04 09:00']])
    schedule = cal.schedule('2012-07-02', '2012-07-04')
    actual = pec.date_range(schedule, '1D', force_close=False, closed=None)

    assert_index_equal(actual, expected)

    # Dec 13, 2016 is adhoc late open
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2016-12-13 11:20', '2016-12-13 12:00', '2016-12-14 09:00', '2016-12-14 11:40',
                                  '2016-12-15 09:00', '2016-12-15 12:00']])
    schedule = cal.schedule('2016-12-13', '2016-12-15')
    actual = pec.date_range(schedule, '1D', force_close=True, closed=None)

    assert_index_equal(actual, expected)


def test_date_range_hour():

    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(10, 30))

    # New Years Eve and weekend skipped
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2015-12-31 10:00', '2015-12-31 10:30',
                                  '2016-01-04 10:00', '2016-01-04 10:30',
                                  '2016-01-05 10:00', '2016-01-05 10:30',
                                  '2016-01-06 10:00', '2016-01-06 10:30']])
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    actual = pec.date_range(schedule, '1H', force_close=True)

    assert_index_equal(actual, expected)

    # If force_close False for then result is missing close if not on even increment
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2015-12-31 10:00', '2016-01-04 10:00', '2016-01-05 10:00', '2016-01-06 10:00']])
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    actual = pec.date_range(schedule, '1H', force_close=False)

    assert_index_equal(actual, expected)

    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))
    # July 3 is late open and early close
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2012-07-02 10:00', '2012-07-02 11:00', '2012-07-02 12:00',
                                  '2012-07-03 11:30',
                                  '2012-07-04 10:00', '2012-07-04 11:00', '2012-07-04 12:00']])
    schedule = cal.schedule('2012-07-02', '2012-07-04')
    actual = pec.date_range(schedule, '1H')

    assert_index_equal(actual, expected)

    # Dec 14, 2016 is adhoc early close
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2016-12-14 10:00', '2016-12-14 11:00', '2016-12-14 11:40',
                                  '2016-12-15 10:00', '2016-12-15 11:00', '2016-12-15 12:00']])
    schedule = cal.schedule('2016-12-14', '2016-12-15')
    actual = pec.date_range(schedule, '1H')

    assert_index_equal(actual, expected)

    # Dec 13, 2016 is adhoc late open, include the open with closed=True
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2016-12-13 11:20', '2016-12-13 12:00',
                                  '2016-12-14 09:00', '2016-12-14 10:00', '2016-12-14 11:00', '2016-12-14 12:00']])
    schedule = cal.schedule('2016-12-13', '2016-12-14')
    actual = pec.date_range(schedule, '1H', closed=None)

    assert_index_equal(actual, expected)


def test_date_range_minute():

    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(10, 30))

    # New Years Eve and weekend skipped
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2015-12-31 10:00', '2015-12-31 10:30',
                                  '2016-01-04 10:00', '2016-01-04 10:30',
                                  '2016-01-05 10:00', '2016-01-05 10:30',
                                  '2016-01-06 10:00', '2016-01-06 10:30']])
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    actual = pec.date_range(schedule, '1min', force_close=True)

    assert_index_equal(actual, expected)

    # If force_close False for then result is missing close if not on even increment
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2015-12-31 10:00', '2016-01-04 10:00', '2016-01-05 10:00', '2016-01-06 10:00']])
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    actual = pec.date_range(schedule, '1min', force_close=False)

    assert_index_equal(actual, expected)

    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))
    # July 3 is late open and early close
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2012-07-02 10:00', '2012-07-02 11:00', '2012-07-02 12:00',
                                  '2012-07-03 11:30',
                                  '2012-07-04 10:00', '2012-07-04 11:00', '2012-07-04 12:00']])
    schedule = cal.schedule('2012-07-02', '2012-07-04')
    actual = pec.date_range(schedule, '1min')

    assert_index_equal(actual, expected)

    # Dec 14, 2016 is adhoc early close
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2016-12-14 10:00', '2016-12-14 11:00', '2016-12-14 11:40',
                                  '2016-12-15 10:00', '2016-12-15 11:00', '2016-12-15 12:00']])
    schedule = cal.schedule('2016-12-14', '2016-12-15')
    actual = pec.date_range(schedule, '1min')

    assert_index_equal(actual, expected)

    # Dec 13, 2016 is adhoc late open, include the open with closed=True
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2016-12-13 11:20', '2016-12-13 12:00',
                                  '2016-12-14 09:00', '2016-12-14 10:00', '2016-12-14 11:00', '2016-12-14 12:00']])
    schedule = cal.schedule('2016-12-13', '2016-12-14')
    actual = pec.date_range(schedule, '1min', closed=None)

    assert_index_equal(actual, expected)

