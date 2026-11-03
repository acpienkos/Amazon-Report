import urllib.request, pathlib
root=pathlib.Path('lab18/sources')
urls={'lab18.md':'https://raw.githubusercontent.com/CinderZhang/FIN43900-Fall2026/main/lessons/week-11/lab-18-legend-investor-as-skill.md','warren_buffett.md':'https://raw.githubusercontent.com/CinderZhang/FAskills/main/financial-researcher/experts/warren_buffett.md','company_tickers.json':'https://www.sec.gov/files/company_tickers.json','COST.json':'https://data.sec.gov/api/xbrl/companyfacts/CIK0000909832.json','JPM.json':'https://data.sec.gov/api/xbrl/companyfacts/CIK0000019617.json'}
for name,url in urls.items():
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Andrew Pienkos apienkos@purdue.edu FIN43900 learning project','Accept-Encoding':'identity'})
  data=urllib.request.urlopen(req,timeout=45).read(); (root/name).write_bytes(data); print(name,len(data))
 except Exception as e: print(name,type(e).__name__,str(e))
