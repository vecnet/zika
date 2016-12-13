# Copyright (C) 2016, University of Notre Dame
# All rights reserved
import pytz
import datetime
# (Django) tests are in website.tests.utils.test_time - will be picked up by TestLoader automatically


def unix_timestamp_to_datetime(unix_timestamp):
    """ Convert unit timestamp (number of seconds since the Epoch (1970/1/1 UTC) to timezone-aware datetime object
    Note we can use datetime.datetime.utcfromtimestamp(unix_timestamp).replace(tzinfo=pytz.utc) here
    However, it doesn't allow for negative unix timestamps (prior to 1970/1/1)

    :param unix_timestamp: Unix timestamp (float)
    :return: datetime object
    """
    epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)
    return epoch + datetime.timedelta(seconds=unix_timestamp)


def datetime_to_unix_timestamp(timestamp):
    """ Covert timezone-aware datetime object to Unix timestamp.
    Note that on Linux we can do timestamp.strftime("%s").
    However, this is not cross-platform and doesn't work on Windows.

    :param timestamp: datetime object
    :return: Number of seconds since 1970/1/1 UTC (float). On some platforms can be rounded, but usually
    is not exactly a whole number and contains milliseconds and even microseconds as decimal
    """
    epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)
    unix_timestamp = (timestamp - epoch).total_seconds()  # Float
    return unix_timestamp
