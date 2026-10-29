"""FIN 43900 Lab 17: live point-in-time audit; no API key required."""
from datetime import date
from io import StringIO
import re
from urllib.parse import urlparse, parse_qs

import numpy as np
import pandas as pd
import requests
import streamlit as st

SERIES = {
    'BAA': "Moody's Seasoned Baa Corporate Bond Yield (monthly)",
    'FEDFUNDS': 'Effective Federal Funds Rate (monthly)',
    'DGS10': '10-Year Treasury Constant Maturity Rate (daily)',
    'MORTGAGE30US': '30-Year Fixed Rate Mortgage Average (weekly)',
}


class DataError(ValueError):
    """A source failed or did not prove the requested data identity."""


def validate_id(series_id):
    series_id = series_id.strip().upper()
    if not re.fullmatch(r'[A-Z][A-Z0-9_]{0,79}', series_id):
        raise DataError('Use a single FRED series ID containing letters, digits or underscores.')
    return series_id


def parse_csv(text, series_id, vintage=None):
    """Require the requested column, including ALFRED's vintage suffix."""
    series_id = validate_id(series_id)
    expected = series_id if vintage is None else f'{series_id}_{vintage:%Y%m%d}'
    try:
        frame = pd.read_csv(StringIO(text), na_values=['.'], keep_default_na=True)
        if list(frame.columns) not in [['observation_date', expected], ['DATE', expected]]:
            raise DataError(f'Unexpected CSV columns; expected date and {expected}.')
        frame.columns = ['date', 'value']
        frame['date'] = pd.to_datetime(frame['date'], errors='raise')
        frame['value'] = pd.to_numeric(frame['value'], errors='raise')
        if frame['date'].isna().any() or frame['date'].duplicated().any():
            raise DataError('Missing or duplicate observation dates.')
        if not np.isfinite(frame['value'].dropna()).all():
            raise DataError('Nonfinite observations.')
        frame = frame.sort_values('date').set_index('date')
        if vintage is not None and (frame.index > pd.Timestamp(vintage)).any():
            raise DataError('Historical response contains dates after the requested cutoff.')
        if frame['value'].dropna().empty:
            raise DataError('No nonmissing observations available for this request.')
        return frame
    except (ValueError, pd.errors.ParserError) as exc:
        raise DataError(f'Invalid or unavailable CSV: {exc}') from exc


def request_csv(url, series_id, vintage=None):
    try:
        response = requests.get(url, timeout=(10, 45), allow_redirects=True)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise DataError(f'Download failed: {exc}') from exc
    final = urlparse(response.url)
    host = 'fred.stlouisfed.org' if vintage is None else 'alfred.stlouisfed.org'
    path = '/graph/fredgraph.csv' if vintage is None else '/graph/alfredgraph.csv'
    query = parse_qs(final.query)
    if final.scheme != 'https' or final.hostname != host or final.path != path:
        raise DataError('Redirect did not preserve the official CSV endpoint.')
    if query.get('id') != [series_id] or (vintage is not None and
            query.get('vintage_date') != [vintage.isoformat()]):
        raise DataError('Redirect changed the series or historical cutoff.')
    frame = parse_csv(response.text, series_id, vintage)
    frame.attrs.update(url=response.url, downloaded_on=date.today().isoformat(),
                       raw_csv=response.text)
    return frame


@st.cache_data(ttl=3600, show_spinner=False)
def download_current(series_id):
    series_id = validate_id(series_id)
    url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}'
    return request_csv(url, series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_vintage(series_id, decision_date):
    """Download only the explicitly requested ALFRED vintage; never fall back."""
    series_id = validate_id(series_id)
    decision_date = date.fromisoformat(str(decision_date))
    if decision_date > date.today():
        raise DataError('A future historical cutoff cannot be verified.')
    url = (f'https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}'
           f'&vintage_date={decision_date.isoformat()}')
    return request_csv(url, series_id, decision_date)


def latest(frame, cutoff=None):
    values = frame['value'].dropna().sort_index()
    if cutoff is not None:
        values = values.loc[values.index <= pd.Timestamp(cutoff)]
    if values.empty:
        raise DataError('No observations at this cutoff.')
    return values.index[-1].date().isoformat(), float(values.iloc[-1])


def compare(current, historical):
    """Full-history counts, independent of chart start; missing cells are not values."""
    now = current['value'].dropna()
    then = historical['value'].dropna()
    old_date, old_value = latest(historical)
    new_date, new_value = latest(current)
    overlap = now.index.intersection(then.index)
    revised = ~np.isclose(now.loc[overlap], then.loc[overlap], rtol=1e-9, atol=1e-8)
    return dict(historical_date=old_date, historical_value=old_value,
                current_date=new_date, current_value=new_value,
                new_after_last_known=int((now.index > pd.Timestamp(old_date)).sum()),
                revised=int(revised.sum()), overlap=int(len(overlap)),
                newly_available_dates=int(len(now.index.difference(then.index))),
                filled_earlier_dates=int(((~now.index.isin(then.index)) &
                                         (now.index <= pd.Timestamp(old_date))).sum()))


def main():
    st.set_page_config(page_title='Point-in-Time Rates Audit', layout='wide')
    st.title('Point-in-Time Audit: What Was Knowable?')
    st.markdown('Data from [FRED](https://fred.stlouisfed.org/) and '
                '[ALFRED](https://alfred.stlouisfed.org/), Federal Reserve Bank of St. Louis, '
                'downloaded today (actual dates shown below); built with AI help, '
                'a learning demonstration, not investment advice.')
    selected = st.sidebar.multiselect('Series', list(SERIES), default=list(SERIES),
                                     format_func=lambda s: f'{s} — {SERIES[s]}')
    extra = st.sidebar.text_input('Additional FRED IDs (comma or space separated)', '')
    start = st.sidebar.date_input('Chart start date', date(2020, 1, 1),
                                 min_value=date(1776, 1, 1), max_value=date.today())
    cutoff = st.sidebar.date_input('As known on', date.today(),
                                  min_value=date(1776, 1, 1), max_value=date.today())
    if st.sidebar.button('Refresh downloads and compare'):
        download_current.clear()
        download_vintage.clear()
    st.caption('Each chart retains its native observation frequency. A month label is not '
               'a publication date. Counts use the complete downloaded histories. '
               'Date-level vintages do not prove availability before an intraday trade.')
    rows = []
    for series_id in dict.fromkeys(selected + re.split(r'[,\s]+', extra.strip())):
        if not series_id:
            continue
        st.subheader(f'{series_id} — {SERIES.get(series_id.upper(), "Additional series")}')
        current = None
        try:
            current = download_current(series_id)
            st.line_chart(current.loc[current.index >= pd.Timestamp(start), ['value']])
            st.caption(f'Current source downloaded {current.attrs["downloaded_on"]}: '
                       f'{current.attrs["url"]}')
        except DataError as exc:
            st.error(f'{series_id}: current data unavailable: {exc}')
        try:
            historical = download_vintage(series_id, cutoff)
            old_date, old_value = latest(historical, cutoff)
            st.write(f'Last observation known on {cutoff}: {old_date} = {old_value:g}')
            st.caption(f'Vintage source downloaded {historical.attrs["downloaded_on"]}: '
                       f'{historical.attrs["url"]}')
            if current is not None:
                result = compare(current, historical)
                rows.append({'Series': f'https://fred.stlouisfed.org/series/{validate_id(series_id)}',
                             **result})
        except DataError as exc:
            st.error(f'{series_id}: historical data unavailable: {exc}')
    st.subheader('Current versus historical vintage')
    st.caption('new_after_last_known counts valid observations later than the last known '
               'observation date; revised counts changed values only on matching dates. '
               'Earlier filled missing dates are reported separately.')
    if rows:
        st.dataframe(pd.DataFrame(rows), hide_index=True, column_config={
            'Series': st.column_config.LinkColumn('Series / FRED page',
                                                 display_text=r'.*/series/(.*)')})
    else:
        st.info('Select a valid series with available current and historical data.')


if __name__ == '__main__':
    main()
