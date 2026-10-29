"""Deterministic unit tests; no live requests or expected-answer fixtures in app."""
import unittest
from unittest.mock import patch, Mock
from datetime import date
import requests
from asof_app import (DataError, parse_csv, latest, compare, validate_id,
                      request_csv, download_vintage, download_current)


def frame(rows, sid='X', vintage=None):
    column = sid if vintage is None else f'{sid}_{vintage:%Y%m%d}'
    return parse_csv(f'observation_date,{column}\n' + rows, sid, vintage)


class AuditTests(unittest.TestCase):
    def setUp(self):
        download_vintage.clear()
        download_current.clear()

    def test_parse_sort(self):
        self.assertEqual(latest(frame('2020-02-01,2\n2020-01-01,1\n')), ('2020-02-01', 2))

    def test_missing(self):
        f = frame('2020-01-01,1\n2020-01-02,.\n')
        self.assertEqual(int(f.value.isna().sum()), 1)
        self.assertEqual(latest(f), ('2020-01-01', 1))

    def test_empty(self):
        for text in ['', 'observation_date,X\n', 'observation_date,X\n2020-01-01,.\n']:
            with self.subTest(text=text), self.assertRaises(DataError):
                parse_csv(text, 'X')

    def test_invalid_ids(self):
        for sid in ['', '../X', 'X&id=BAA', 'A B']:
            with self.subTest(sid=sid), self.assertRaises(DataError):
                validate_id(sid)
        self.assertEqual(validate_id(' payems '), 'PAYEMS')

    def test_cutoff(self):
        f = frame('2020-01-01,1\n2020-02-01,2\n')
        self.assertEqual(latest(f, date(2020, 1, 15)), ('2020-01-01', 1))
        with self.assertRaises(DataError):
            latest(f, date(2019, 1, 1))

    def test_revisions_and_new(self):
        old = frame('2020-01-01,1\n2020-02-01,2\n')
        now = frame('2020-01-01,1\n2020-02-01,3\n2020-03-01,4\n')
        result = compare(now, old)
        self.assertEqual((result['revised'], result['new_after_last_known'], result['overlap']), (1, 1, 2))

    def test_frequencies(self):
        for dates in [('2020-01-01', '2020-02-01'), ('2020-01-02', '2020-01-09'),
                      ('2020-01-02', '2020-01-03')]:
            with self.subTest(dates=dates):
                old = frame(f'{dates[0]},1\n')
                now = frame(f'{dates[0]},1\n{dates[1]},2\n')
                self.assertEqual(compare(now, old)['new_after_last_known'], 1)

    def test_tolerance(self):
        self.assertEqual(compare(frame('2020-01-01,1.000000001\n'),
                                 frame('2020-01-01,1\n'))['revised'], 0)

    def test_filled_missing_not_revision(self):
        old = frame('2020-01-01,.\n2020-02-01,2\n')
        now = frame('2020-01-01,1\n2020-02-01,2\n')
        result = compare(now, old)
        self.assertEqual((result['revised'], result['filled_earlier_dates'],
                          result['new_after_last_known']), (0, 1, 0))

    @patch('asof_app.requests.get')
    def test_http_error(self, get):
        get.return_value.raise_for_status.side_effect = requests.HTTPError('404')
        with self.assertRaises(DataError):
            download_current('BADID')

    @patch('asof_app.requests.get', side_effect=requests.Timeout('timeout'))
    def test_timeout(self, get):
        with self.assertRaises(DataError):
            download_vintage('X', date(2020, 2, 1))
        self.assertEqual(get.call_count, 1)

    @patch('asof_app.requests.get')
    def test_no_current_substitution(self, get):
        url = 'https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=X&vintage_date=2020-02-01'
        get.return_value = Mock(url=url, text='observation_date,X\n2020-01-01,1\n')
        with self.assertRaises(DataError):
            download_vintage('X', date(2020, 2, 1))
        self.assertEqual(get.call_count, 1)
        self.assertIn('alfred', get.call_args.args[0])

    @patch('asof_app.requests.get')
    def test_redirect_rejected(self, get):
        get.return_value = Mock(url='https://fred.stlouisfed.org/graph/fredgraph.csv?id=X',
                                text='observation_date,X\n2020-01-01,1\n')
        with self.assertRaises(DataError):
            download_vintage('X', date(2020, 2, 1))

    @patch('asof_app.requests.get')
    def test_historical_url_and_parse(self, get):
        url = 'https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=X&vintage_date=2020-02-01'
        get.return_value = Mock(url=url, text='observation_date,X_20200201\n2020-01-01,1\n')
        self.assertEqual(latest(download_vintage('x', date(2020, 2, 1))), ('2020-01-01', 1))
        self.assertEqual(get.call_args.args[0], url)

    def test_unavailable_vintage(self):
        with self.assertRaises(DataError):
            parse_csv('<html>Not available</html>', 'X', date(2020, 2, 1))

    def test_future_leak(self):
        with self.assertRaises(DataError):
            frame('2020-03-01,1\n', vintage=date(2020, 2, 1))

    def test_malformed(self):
        for rows in ['2020-01-01,bad\n', 'bad,1\n', '2020-01-01,1\n2020-01-01,2\n', '2020-01-01,inf\n']:
            with self.subTest(rows=rows), self.assertRaises(DataError):
                frame(rows)


if __name__ == '__main__':
    unittest.main(verbosity=2)
