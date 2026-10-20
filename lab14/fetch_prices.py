from pathlib import Path
import json,urllib.request,datetime,csv,calendar
p=Path(__file__).resolve().parent
(p/'sources').mkdir(exist_ok=True)
commit=json.load(urllib.request.urlopen('https://api.github.com/repos/CinderZhang/FIN43900-Fall2026/commits/main'))['sha']
for name in ('lab-14-portfolio-baselines.md','student-prework.md','student-handout.md','README.md'):
 url=f'https://raw.githubusercontent.com/CinderZhang/FIN43900-Fall2026/{commit}/lessons/week-09/{name}'
 (p/'sources'/name).write_bytes(urllib.request.urlopen(url).read())
(p/'sources'/'course_commit.txt').write_text(commit+'\n')
series={}; meta={}
for ticker in ('BIL','IEF','LQD','VT'):
 url=f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=10y&interval=1mo'
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 raw=urllib.request.urlopen(req,timeout=45).read()
 data=json.loads(raw)['chart']['result'][0]
 (p/'sources'/f'{ticker}_monthly.json').write_bytes(raw)
 obs={}
 for ts,value in zip(data['timestamp'],data['indicators']['adjclose'][0]['adjclose']):
  # Yahoo monthly bars are labeled by the start of the month in exchange time.
  d=datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).date()
  if datetime.date(2021,10,1)<=d<datetime.date(2026,10,1):
   if value is None or value<=0: raise ValueError(f'Missing/nonpositive {ticker} {d}')
   obs[d.isoformat()]=value
 if len(obs)!=60: raise ValueError(f'{ticker}: expected 60 completed monthly observations, got {len(obs)}')
 series[ticker]=obs
 meta[ticker]={'name':data['meta'].get('longName'),'source':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':len(obs)}
assert all(set(s)==set(series['BIL']) for s in series.values())
with (p/'prices.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['date',*series]);w.writerows([d,*[series[t][d] for t in series]] for d in sorted(series['BIL']))
(p/'sources'/'price_provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta,indent=2));print('Verified 60 aligned complete months: 2021-10 through 2026-09; no fill or interpolation.')
