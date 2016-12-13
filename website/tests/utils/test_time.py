# All rights reserved
from django.test.testcases import TestCase
from website.utils.time import unix_timestamp_to_datetime, datetime_to_unix_timestamp
import datetime
import pytz


class TimeTest(TestCase):
    def test_smoke_test_1(self):
        self.assertEqual(
            unix_timestamp_to_datetime(datetime_to_unix_timestamp(datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC))),
            datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC),
        )

    def test_smoke_test_2(self):
        timestamp = datetime.datetime(2012, 3, 5, 12, 45, 11, 912000, tzinfo=pytz.UTC)
        self.assertEqual(
            unix_timestamp_to_datetime(datetime_to_unix_timestamp(timestamp)),
            timestamp,
        )

    def test_smoke_test_min_year(self):
        timestamp = datetime.datetime(datetime.MINYEAR, 1, 1, tzinfo=pytz.UTC)
        self.assertEqual(
            unix_timestamp_to_datetime(datetime_to_unix_timestamp(timestamp)),
            timestamp,
        )

    def test_smoke_test_max_year(self):
        # This may fail due to floating point error. But it worked so far.
        timestamp = datetime.datetime(datetime.MAXYEAR, 12, 31, 23, 59, 59, tzinfo=pytz.UTC)
        self.assertEqual(
            unix_timestamp_to_datetime(datetime_to_unix_timestamp(timestamp)),
            timestamp,
        )

    def test_smoke_test_3(self):
        self.assertEqual(
            datetime_to_unix_timestamp(unix_timestamp_to_datetime(1000)),
            1000,
        )

    def test_smoke_test_4(self):
        self.assertEqual(
            datetime_to_unix_timestamp(unix_timestamp_to_datetime(1000.80)),
            1000.80,
        )

    def test_unix_timestamp_to_datetime_base(self):
        self.assertEqual(
            unix_timestamp_to_datetime(0),
            datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)
        )

    def test_unix_timestamp_to_datetime_allballs_fail(self):
        # Note that year 0 is not supported by python datetime.datetime
        # So datetime.datetime(0, 0, 0, 0, 0, 0, tzinfo=pytz.UTC) should raise ValueError: year is out of range
        self.assertRaises(
            ValueError,
            datetime.datetime, 0, 0, 0, 0, 0, 0, tzinfo=pytz.UTC
        )

    def test_unix_timestamp_to_datetime_1(self):
        self.assertEqual(
            unix_timestamp_to_datetime(1481340116),
            datetime.datetime(2016, 12, 10, 3, 21, 56, tzinfo=pytz.UTC)
        )

    def test_unix_timestamp_to_datetime_2(self):
        self.assertEqual(
            unix_timestamp_to_datetime(1481340116.0),
            datetime.datetime(2016, 12, 10, 3, 21, 56, tzinfo=pytz.UTC)
        )

    def test_unix_timestamp_to_datetime_3(self):
        self.assertEqual(
            unix_timestamp_to_datetime(1481340116.5),
            datetime.datetime(2016, 12, 10, 3, 21, 56, 500000, tzinfo=pytz.UTC)
        )

    def test_unix_timestamp_to_datetime_4(self):
        self.assertEqual(
            unix_timestamp_to_datetime(-1000000),
            datetime.datetime(1969, 12, 20, 10, 13, 20, tzinfo=pytz.UTC)
        )

    def test_datetime_to_unix_timestamp_base(self):
        self.assertEqual(
            datetime_to_unix_timestamp(datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)),
            0,
        )

    def test_datetime_to_unix_timestamp_1(self):
        self.assertEqual(
            datetime_to_unix_timestamp(datetime.datetime(2016, 12, 10, 3, 21, 56, tzinfo=pytz.UTC)),
            1481340116,
        )

    def test_datetime_to_unix_timestamp_2(self):
        self.assertEqual(
            datetime_to_unix_timestamp(datetime.datetime(2016, 12, 10, 3, 21, 56, tzinfo=pytz.UTC)),
            1481340116.0
        )

    def test_datetime_to_unix_timestamp_3(self):
        self.assertEqual(
            datetime_to_unix_timestamp(datetime.datetime(2016, 12, 10, 3, 21, 56, 500000, tzinfo=pytz.UTC)),
            1481340116.5,
        )

    def test_datetime_to_unix_timestamp_4(self):
        self.assertEqual(
            datetime_to_unix_timestamp(datetime.datetime(1969, 12, 20, 10, 13, 20, tzinfo=pytz.UTC)),
            -1000000,
        )
